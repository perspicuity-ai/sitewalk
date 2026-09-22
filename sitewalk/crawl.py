"""The crawl: discover URLs, fetch a bounded number of them, and observe the site.

One loop serves both sources. It discovers URLs from ``robots.txt``, from ``sitemap.xml``, and
from the internal links of pages it has already read; it never fetches outside the submitted
origin; and it never exceeds ``max_pages``. What it could not reach — a page cap, a redirection
off the origin, a ``robots.txt`` disallow — is recorded rather than dropped, because a gate that
quietly checked less than it claims is worse than no gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from . import sitemap
from .facts import ABSENT, DERIVED, PRESENT, Page, PageFact, Skip, Surface
from .pages import facts_from
from .sources import PageSource
from urllib.parse import urlsplit, urlunsplit

from .urls import SURFACE_PATHS, normalise, origin_of, relative_path, same_origin

#: Paths that are fetched as pages even though they are also surfaces.
_PAGE_EXCEPTIONS = frozenset(SURFACE_PATHS)


@dataclass
class CrawlResult:
    """Everything one crawl observed, before it is turned into a report."""

    target: str
    origin: str
    #: The origin the build claims to be, when the caller declared one. Empty means the canonical
    #: host check cannot run: there is nothing to judge a host against.
    declared_origin: str = ""
    #: What the site judgements are relative to, stated in the report so a reader knows.
    judged_against: str = ""
    #: The origin the sitemap's URLs were read against, when it differs from the walked origin.
    sitemap_named_origin: str = ""
    pages: list[PageFact] = field(default_factory=list)
    surfaces: dict[str, Surface] = field(default_factory=dict)
    sitemap_urls: list[str] = field(default_factory=list)
    sitemap_errors: list[str] = field(default_factory=list)
    skipped: list[Skip] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    refused: list[str] = field(default_factory=list)
    source_kind: str = ""
    source_label: str = ""
    user_agent: str = ""
    requests_made: int = 0
    truncated_pages: int = 0
    link_checked: int = 0
    cap_reached: bool = False
    started_at: str = ""
    finished_at: str = ""


def _remap(url: str, from_origin: str, to_origin: str) -> str:
    """Rewrite a URL from the origin a build claims to be onto the origin it is walked as.

    The path is the same in a build directory: the sitemap says ``https://example.com/about/`` and
    the file is ``about/index.html``, reached by walking ``https://localhost/about/``.
    """
    parts = urlsplit(url)
    path = urlunsplit(("", "", parts.path or "/", parts.query, ""))
    return f"{to_origin}{path}"


def _robots_skip(url: str, rule) -> Skip:
    """A skip caused by a ``robots.txt`` rule, carrying the line that caused it."""
    return Skip(
        url=url,
        reason="robots.txt disallows this path for our user agent",
        rule=rule.source_line,
    )


def _stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _surface(name: str, url: str, page: Page) -> Surface:
    body_bytes = len(page.body.encode("utf-8", errors="replace")) if page.body is not None else 0
    return Surface(
        name=name,
        state=PRESENT if page.ok else ABSENT,
        url=url,
        status=page.status,
        content_type=page.content_type,
        bytes=body_bytes,
        error=page.error,
    )


def crawl(
    source: PageSource,
    target: str,
    *,
    max_pages: int = 50,
    max_sitemaps: int = sitemap.MAX_SITEMAP_DEPTH,
    declared_origin: str = "",
) -> CrawlResult:
    """Discover and read a site, bounded at every step.

    ``target`` is the submitted URL for the HTTP source and the synthetic origin for the local
    one. It decides what counts as internal, so it is never inferred from a page's own links.
    """
    origin = origin_of(target)
    result = CrawlResult(
        target=target,
        origin=origin,
        declared_origin=declared_origin,
        judged_against=declared_origin or origin,
        source_kind=getattr(source, "kind", ""),
        source_label=getattr(source, "label", ""),
        user_agent=getattr(source, "user_agent", ""),
        started_at=_stamp(),
    )
    cache: dict[str, Page] = {}

    def read(url: str) -> Page:
        """Fetch through the crawl's own cache, counting only the requests actually made."""
        key = normalise(url)
        if key in cache:
            return cache[key]
        page = source.fetch(key)
        result.requests_made += 1
        cache[key] = page
        return page

    # 1. The optional surfaces, read first so a missing robots.txt or sitemap.xml is known even
    #    when nothing links to them. This also seeds the cache, so a surface is not re-requested
    #    when the crawl reaches it.
    surface_pages: dict[str, Page] = {}
    for name in SURFACE_PATHS:
        url = normalise(f"{origin}/{name}")
        page = read(url)
        surface_pages[name] = page
        result.surfaces[name] = _surface(name, url, page)

    # 2. Discovery from the sitemap, and from any sitemap that robots.txt names.
    discovered: list[str] = []
    sitemap_queue: list[tuple[str, int]] = []
    # The sitemap of a build names the site's own URLs, which are on the origin the build claims to
    # be -- not on the synthetic origin a directory is walked as. When the caller declares that
    # origin, the sitemap is read against it; when not, the synthetic origin is all there is.
    sitemap_origin = declared_origin or origin
    sitemap_page = surface_pages.get("sitemap.xml")
    if sitemap_page is not None and sitemap_page.ok and sitemap_page.body:
        sitemap_queue.append((normalise(f"{origin}/sitemap.xml"), 0))
    robots_page = surface_pages.get("robots.txt")
    robots_sitemaps: list[str] = []
    disallowed: list[str] = []
    if robots_page is not None and robots_page.ok and robots_page.body:
        robots_sitemaps, disallowed = sitemap.parse_robots(robots_page.body)
    for candidate in robots_sitemaps:
        if same_origin(candidate, sitemap_origin):
            # Remapped onto the walked origin, so it is the same queue entry as the top-level
            # sitemap rather than a second pass over the same file.
            sitemap_queue.append(
                (normalise(_remap(candidate, sitemap_origin, origin)), 0)
            )
        elif same_origin(candidate, origin):
            sitemap_queue.append((normalise(candidate), 0))
        else:
            result.notes.append(
                "robots.txt names a sitemap off the submitted origin, which was not fetched: "
                f"{candidate}"
            )

    seen_sitemaps: set[str] = set()
    while sitemap_queue and len(seen_sitemaps) <= max_sitemaps:
        sitemap_url, depth = sitemap_queue.pop(0)
        if sitemap_url in seen_sitemaps or depth > max_sitemaps:
            continue
        seen_sitemaps.add(sitemap_url)
        page = read(sitemap_url)
        if sitemap_url not in (normalise(f"{origin}/sitemap.xml"),):
            result.surfaces[sitemap_url] = _surface(relative_path(sitemap_url), sitemap_url, page)
        if not page.ok or not page.body:
            if page.status and not page.ok:
                result.sitemap_errors.append(f"{relative_path(sitemap_url)} returned {page.status}")
            elif page.error:
                result.sitemap_errors.append(f"{relative_path(sitemap_url)}: {page.error}")
            continue
        parsed = sitemap.parse_sitemap(page.body)
        for message in parsed.errors:
            result.sitemap_errors.append(f"{relative_path(sitemap_url)}: {message}")
        for url in parsed.urls:
            if same_origin(url, sitemap_origin):
                # Named for the declared origin: map it onto the origin being walked so the crawl
                # can read the file that serves it, and record that the site itself named it.
                discovered.append(normalise(_remap(url, sitemap_origin, origin)))
                result.sitemap_named_origin = sitemap_origin
            elif same_origin(url, origin):
                discovered.append(normalise(url))
            else:
                result.notes.append(
                    f"the sitemap names a URL off the site: {url} (not on {sitemap_origin})"
                )
        for nested in parsed.nested:
            if same_origin(nested, sitemap_origin):
                sitemap_queue.append(
                    (normalise(_remap(nested, sitemap_origin, origin)), depth + 1)
                )
            elif same_origin(nested, origin):
                sitemap_queue.append((normalise(nested), depth + 1))
            else:
                result.notes.append(f"the sitemap index names a sitemap off the origin: {nested}")

    result.sitemap_urls = list(dict.fromkeys(discovered))
    in_sitemap = set(result.sitemap_urls)

    # 3. The home page is always first: it is what the user submitted, and its links are the
    #    second discovery source.
    home = normalise(f"{origin}/")
    queue: list[str] = [home]
    for url in discovered:
        if url not in queue:
            queue.append(url)
    fetched: set[str] = set()

    while queue and len(fetched) < max_pages:
        url = queue.pop(0)
        if url in fetched:
            continue
        fetched.add(url)
        rule = sitemap.is_disallowed(relative_path(url), disallowed)
        if relative_path(url) not in _PAGE_EXCEPTIONS and rule is not None:
            result.skipped.append(_robots_skip(url, rule))
            continue
        page = read(url)
        if page.truncated:
            result.truncated_pages += 1
        fact = facts_from(page, in_sitemap=url in in_sitemap, note=page.note)
        # ``page.url`` is the URL that was asked for; ``redirect_to`` says where it ended up,
        # whether that was a redirect the crawl followed or one it refused to follow.
        fact.redirect_to = page.redirect_to
        result.pages.append(fact)
        if page.ok and fact.is_html:
            for link in fact.internal_targets:
                if link not in fetched and link not in queue:
                    queue.append(link)

    if queue:
        result.cap_reached = True
        result.notes.append(
            f"stopped at the {max_pages}-page cap with {len(queue)} URL(s) still queued; "
            "raise --max-pages to see them"
        )

    # 4. A bounded check of internal links the crawl did not otherwise reach. There is no
    #    separate link-check bound: ``max_pages`` is the single bound on what this run reads, and
    #    a link to a page the crawl already fetched is answered from that page rather than
    #    requested again. What is left over is named in the notes above.
    targets: list[str] = []
    for fact in result.pages:
        if not fact.is_html:
            continue
        for link in fact.internal_targets:
            if link not in fetched and link not in targets:
                targets.append(link)
    for url in targets:
        if len(fetched) >= max_pages:
            # ``max_pages`` bounds the report, not just the crawl loop: a link check must not
            # push the run past the bound the caller set.
            result.notes.append(
                f"the {max_pages}-page bound was reached, so "
                f"{len(targets) - result.link_checked} internal link target(s) were left "
                "unchecked; raise --max-pages to check them"
            )
            break
        if relative_path(url) in _PAGE_EXCEPTIONS:
            result.skipped.append(Skip(url=url, reason="a surface, already read as a surface"))
            continue
        rule = sitemap.is_disallowed(relative_path(url), disallowed)
        if rule is not None:
            result.skipped.append(_robots_skip(url, rule))
            continue
        page = read(url)
        fetched.add(url)
        result.link_checked += 1
        fact = facts_from(page, in_sitemap=url in in_sitemap, note=page.note)
        fact.note = "; ".join(
            filter(None, [fact.note, "reached by the link check, not crawled as a page"])
        )
        result.pages.append(fact)
    # 5. json-ld is not a URL and cannot be fetched: it is established from the pages already
    #    read. Recorded as a derived surface so a plan requiring it gets a real verdict, and so a
    #    reader can tell "derived" from "fetched and empty".
    carrying = [fact.url for fact in result.pages if fact.json_ld_types]
    read = [fact.url for fact in result.pages if fact.is_html]
    # The format requires the page to be named either way: markup found, or the pages read when it
    # was not. A verdict without them is the claim this rule exists to prevent.
    named = carrying or read
    result.surfaces["json-ld"] = Surface(
        name="json-ld",
        state=DERIVED,
        established=bool(carrying),
        pages=tuple(named),
        note=(
            f"derived from the JSON-LD @type values of the pages read: "
            f"{len(carrying)} of {len(result.pages)} carry one"
        ),
    )

    result.refused = list(getattr(source, "refusals", ()))
    result.finished_at = _stamp()
    return result
