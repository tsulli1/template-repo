"""Utilities for scoring procrastination-related phrases.

This module provides a simple helper that looks for any occurrence of
pre-defined procrastination phrases in an input string.  The list of
phrases is shared with a DMN (Decision Management Network) policy that
assigns additional scoring when procrastination intent is detected.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List

# Patterns that should trigger additional scoring for procrastination intent.
#
# Historically these strings contained leading spaces (e.g. ``" tomorrow"``)
# to avoid matching other words.  That approach broke detection for inputs
# that started with the phrase or were preceded by punctuation, so the
# patterns are now written without those literal spaces.
PROCRAST_PHRASES: List[str] = [
    r"procrastinat(ing|e|ion)",
    r"tomorrow",
    r"later",
    r"idk",
    r"not now",
]


@dataclass
class ProcrastinationMatch:
    """Represents the result of scanning text for procrastination signals."""

    phrase: str
    pattern: str
    span: tuple[int, int]


def find_procrastination_phrases(
    text: str, patterns: Iterable[str] | None = None
) -> List[ProcrastinationMatch]:
    """Return matches for procrastination phrases in ``text``.

    Parameters
    ----------
    text:
        The text that should be scanned for procrastination intent.
    patterns:
        Optional custom iterable of regex patterns.  When omitted the global
        :data:`PROCRAST_PHRASES` list is used.
    """

    compiled_patterns = [
        re.compile(pattern, flags=re.IGNORECASE) for pattern in patterns or PROCRAST_PHRASES
    ]

    matches: List[ProcrastinationMatch] = []
    for pattern, compiled in zip(patterns or PROCRAST_PHRASES, compiled_patterns):
        for match in compiled.finditer(text):
            matches.append(
                ProcrastinationMatch(
                    phrase=text[match.start() : match.end()],
                    pattern=pattern,
                    span=match.span(),
                )
            )
    return matches


def score_procrastination(text: str) -> int:
    """Return a simple score equal to the number of procrastination matches.

    The DMN policy consumes this score to determine whether to escalate or
    route the request differently.  This helper mimics the production logic so
    the matching behaviour can be verified in tests.
    """

    return len(find_procrastination_phrases(text))


__all__ = [
    "PROCRAST_PHRASES",
    "ProcrastinationMatch",
    "find_procrastination_phrases",
    "score_procrastination",
]
