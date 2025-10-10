import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from dmn_security_lab import PROCRAST_PHRASES, check_for_procrastination


def test_tomorrow_triggers_policy():
    result = check_for_procrastination("Tomorrow I'll do it")
    assert result.matched
    assert any(pattern == result.pattern for pattern in PROCRAST_PHRASES)


def test_not_now_triggers_policy():
    result = check_for_procrastination("Not now, maybe later")
    assert result.matched
    assert any(pattern == result.pattern for pattern in PROCRAST_PHRASES)


def test_regexes_have_no_leading_space():
    assert all(not pattern.startswith(" ") for pattern in PROCRAST_PHRASES)
