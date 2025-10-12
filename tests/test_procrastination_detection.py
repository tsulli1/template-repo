import pytest

from dmn_security_lab import PROCRAST_PHRASES, find_procrastination_phrases, score_procrastination


def _matches(text: str):
    return [match.phrase for match in find_procrastination_phrases(text)]


def test_tomorrow_phrase_matches_without_leading_space():
    text = "Tomorrow I'll do it"
    matches = _matches(text)

    assert score_procrastination(text) > 0
    assert any(match.lower().startswith("tomorrow") for match in matches)


def test_not_now_detected_at_start_of_string():
    text = "Not now"
    matches = _matches(text)

    assert score_procrastination(text) > 0
    assert any(match.lower().startswith("not now") for match in matches)


def test_patterns_have_no_leading_spaces():
    offending = [pattern for pattern in PROCRAST_PHRASES if pattern.startswith(" ")]
    assert offending == []


def test_punctuation_preceding_idk_is_detected():
    text = "Fine... idk"
    matches = _matches(text)

    assert score_procrastination(text) > 0
    assert any("idk" in match.lower() for match in matches)
