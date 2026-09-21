"""sitewalk — a structural map of a site that is already built.

Public entry points, so a caller does not have to know the module layout:

    >>> from sitewalk import FileSource, crawl, analyse, to_dict

Nothing in this package executes JavaScript, fetches outside the submitted origin, or claims
anything about ranking, citations or traffic. See the claim boundary in ``report.BOUNDARY``.
"""

from __future__ import annotations

from .crawl import CrawlResult, crawl
from .facts import ERROR, INFO, Finding, Page, PageFact, SiteReport, Surface
from .fetch import USER_AGENT, VERSION
from .findings import analyse
from .plan import PlanCheck, check_plan, load_plan
from .report import BOUNDARY, exit_code, to_dict, to_json, to_text
from .sources import FileSource, LiveSource, PageSource

__version__ = VERSION

__all__ = [
    "BOUNDARY",
    "ERROR",
    "INFO",
    "USER_AGENT",
    "VERSION",
    "CrawlResult",
    "FileSource",
    "Finding",
    "LiveSource",
    "Page",
    "PageFact",
    "PageSource",
    "PlanCheck",
    "SiteReport",
    "Surface",
    "__version__",
    "analyse",
    "check_plan",
    "crawl",
    "exit_code",
    "load_plan",
    "to_dict",
    "to_json",
    "to_text",
]
