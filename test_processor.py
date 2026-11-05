"""Updated Hypothesis fuzz tests for the assigned daycare-fees application.

The lab handout calls this file test_processor.py. The assigned repository's
application module is named daycare_fees.py, so these tests import the
three functions from that module.
"""

from hypothesis import given, strategies as st

from daycare_fees import parse_enrolment, hours_average, payable_fee


@given(st.text() | st.none())
def test_parse_enrolment_no_crash(value):
    try:
        parse_enrolment(value)
    except Exception as exc:
        assert False, f"parse_enrolment crashed with: {exc}"


@given(st.text() | st.none())
def test_hours_average_no_crash(value):
    try:
        hours_average(value)
    except Exception as exc:
        assert False, f"hours_average crashed with: {exc}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(value):
    try:
        payable_fee(value)
    except Exception as exc:
        assert False, f"payable_fee crashed with: {exc}"
