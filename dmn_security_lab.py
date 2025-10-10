import re
from dataclasses import dataclass
from typing import List

PROCRAST_PHRASES: List[str] = [
    r"procrastinat(?:ing|e|ion)",
    r"tomorrow",
    r"later",
    r"idk",
    r"not now",
]


@dataclass
class DMNCheckResult:
    matched: bool
    pattern: str | None = None


def check_for_procrastination(text: str) -> DMNCheckResult:
    """Return whether the supplied text triggers the procrastination policy."""
    for pattern in PROCRAST_PHRASES:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return DMNCheckResult(True, pattern)
    return DMNCheckResult(False, None)
