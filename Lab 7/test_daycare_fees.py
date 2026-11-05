"""Hypothesis fuzz tests for the daycare fee functions."""

from hypothesis import given, strategies as st

from daycare_fees import parse_enrolment, hours_average, payable_fee


@given(st.text() | st.none())
def test_parse_enrolment_no_crash(value):
    """The parser should handle arbitrary text and None without crashing."""
    try:
        parse_enrolment(value)
    except Exception as exc:
        assert False, f"parse_enrolment crashed with: {exc}"


@given(st.text() | st.none())
def test_hours_average_no_crash(value):
    """The average function should handle arbitrary text and None safely."""
    try:
        hours_average(value)
    except Exception as exc:
        assert False, f"hours_average crashed with: {exc}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(value):
    """The fee calculator should handle arbitrary text and None safely."""
    try:
        payable_fee(value)
    except Exception as exc:
        assert False, f"payable_fee crashed with: {exc}"
