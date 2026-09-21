# Context

What sitewalk is, why it exists, and what "good" looks like.

**Project code:** `sw`

## The product, in one paragraph

Give `sitewalk` a web address or a directory of built files, and it returns a structural map of
the site: every page it can find, what each page exposes to a machine, how the pages connect to
each other, and where the gaps are. It reports the shape of a site that is already built.

## Why it exists

The evidence is one audit. On 2026-09-21 the `agent-eligibility` check was run against
`findmynextbite.food` and reported "no JSON, XML or API surface was linked from the home page" —
while that site's sitemap lists 26 URLs and it publishes a public `/api/discovery` endpoint. The
check was not wrong; it reads one page. **Nothing in this workspace can currently tell you how a
site functions beyond its front door.**

That matters most at the moment before a deploy, when the question is "did this change break
anything about how the site presents itself to machines", and nothing answers it.

## Outcomes

1. **A structural map good enough to gate a deploy.** `sitewalk --dir build/` runs offline
   against built files, so it can block a release without touching the network.
2. **A public tool others can run.** No dependency, a documented install, tests that run without
   special hardware.

## The claim boundary

`sitewalk` reports **what is observable in the output the server returns**. It fetches HTML and
reads it. It does not execute JavaScript, so it cannot see anything a browser would render after
load, and it says so rather than implying a page is empty.

It does **not** predict whether an agent will find, trust or recommend a site, and it does not
measure ranking, citations or traffic. Those are observations about the world, and this tool
observes a site.

## What we are deliberately not doing

- **No JavaScript execution.** It would add a browser engine, and the point is to see what a
  non-executing client sees.
- **No external APIs and no accounts.** Standard library only, like the rest of the toolkit.
- **No crawling outside the site's own origin.** A tool that follows a link off-site is a tool
  that can be pointed at someone else's server.
- **No PII.** It reads published pages; it does not collect anything about a person.

## What we reuse rather than rebuild

Nothing. This is deliberately independent of `agent-eligibility`: that tool gives a rubric
verdict on a supplier's front door, this one maps a site's structure. Sharing a rubric would
couple two different jobs. The one interface between projects is the plan file, which `siteplan`
produces and `sitewalk --plan` consumes.

## Success, and what would stop us

- **Passes** when `sitewalk` has caught a real regression in a project's release path, and at
  least two projects run it.
- **Fails** if it only ever reports what a sitemap already says, or if nobody runs it twice.
- **Scope cap:** if the first working version is not usable against a real site within the first
  session, stop and cut the page inventory down rather than adding features.
