"""A refusal or a failure.

The distinction matters in the output: a *refusal* names a rule that was applied, and is
something the tool decided not to do. A *failure* is something that did not work. Both stop
the operation, but only a refusal is evidence that the guard ran.
"""

from __future__ import annotations


class SitewalkError(Exception):
    """Base class for every error this package raises deliberately."""


class GuardError(SitewalkError):
    """A request was refused before it was made, or after connecting.

    The guard is the only thing that raises this, and the message names the rule.
    """


class FetchError(SitewalkError):
    """A request was permitted but did not complete."""


class PlanError(SitewalkError):
    """A plan file could not be read or could not be understood at all.

    A plan that is readable but violated is a *finding*, not this.
    """
