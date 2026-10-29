
import pytest

from daycare_fees import (
    extra_hours_fee,
    enrolment_allowed,
    pickup_status,
)


# 1. Tests for extra_hours_fee()

def test_within_included_hours():
    assert extra_hours_fee("toddler", 20, False) == 0


def test_exactly_included_hours():
    assert extra_hours_fee("infant", 20, False) == 0


def test_extra_hours_infant():
    assert extra_hours_fee("infant", 21, False) == 14


def test_extra_hours_toddler():
    assert extra_hours_fee("toddler", 26, False) == 9


def test_extra_hours_preschool():
    assert extra_hours_fee("preschool", 31, False) == 9


def test_sibling_discount_for_toddler():
    assert extra_hours_fee("toddler", 26, True) == 0


def test_sibling_discount_for_preschool():
    assert extra_hours_fee("preschool", 36, True) == 9


def test_sibling_does_not_change_infant_hours():
    assert extra_hours_fee("infant", 21, True) == 14


def test_more_than_20_extra_hours_infant():
    assert extra_hours_fee("infant", 41, False) == 462


def test_more_than_20_extra_hours_toddler():
    assert extra_hours_fee("toddler", 46, False) == 294


def test_more_than_20_extra_hours_preschool():
    assert extra_hours_fee("preschool", 51, False) == 294


def test_unknown_age_group():
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee("teenager", 30, False)


def test_negative_hours():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("toddler", -1, False)


# 2. Tests for enrolment_allowed()

def test_enrolment_allowed():
    assert enrolment_allowed(24, 2, False) is True


def test_enrolment_denied_when_immunisation_pending_and_too_young():
    assert enrolment_allowed(11, 5, True) is False


def test_enrolment_allowed_when_immunisation_pending_and_old_enough():
    assert enrolment_allowed(12, 0, True) is True


def test_enrolment_denied_below_six_months():
    assert enrolment_allowed(5, 5, False) is False


def test_enrolment_allowed_at_six_months():
    assert enrolment_allowed(6, 1, False) is True


def test_enrolment_denied_when_no_vacancies():
    assert enrolment_allowed(24, 0, False) is False


def test_enrolment_allowed_with_one_vacancy():
    assert enrolment_allowed(24, 1, False) is True


# 3. Tests for pickup_status()

def test_pickup_on_time_regular_non_friday():
    assert pickup_status(10, False, False) == "on_time"


def test_pickup_late_regular_non_friday():
    assert pickup_status(9, False, False) == "late"


def test_pickup_overdue_regular_non_friday():
    assert pickup_status(-6, False, False) == "overdue"


def test_pickup_on_time_aftercare():
    assert pickup_status(20, True, False) == "on_time"


def test_pickup_late_aftercare():
    assert pickup_status(19, True, False) == "late"


def test_pickup_overdue_aftercare():
    assert pickup_status(4, True, False) == "overdue"


def test_pickup_on_time_friday():
    assert pickup_status(20, False, True) == "on_time"


def test_pickup_late_friday():
    assert pickup_status(19, False, True) == "late"


def test_pickup_overdue_friday():
    assert pickup_status(4, False, True) == "overdue"


def test_pickup_on_time_friday_aftercare():
    assert pickup_status(30, True, True) == "on_time"


def test_pickup_late_friday_aftercare():
    assert pickup_status(29, True, True) == "late"


def test_pickup_overdue_friday_aftercare():
    assert pickup_status(14, True, True) == "overdue"
