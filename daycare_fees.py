"""Hardened daycare fee functions for SE Lab 7 fuzz testing.

Invalid inputs are handled safely using documented fallback values:
- parse_enrolment: ("Unknown", 0.0)
- hours_average: 0.0
- payable_fee: 0.0
"""

import math


def parse_enrolment(text):
    """Parse an 'age_group:hours' string safely."""
    try:
        if not isinstance(text, str) or text.count(":") != 1:
            return "Unknown", 0.0

        age_group, hours_text = text.split(":")
        age_group = age_group.strip()
        hours = float(hours_text.strip())

        if not age_group or not math.isfinite(hours) or hours < 0:
            return "Unknown", 0.0

        return age_group.title(), hours
    except (ValueError, TypeError, AttributeError):
        return "Unknown", 0.0


def hours_average(hours_csv):
    """Return the arithmetic mean of comma-separated non-negative hours."""
    try:
        if not isinstance(hours_csv, str) or not hours_csv.strip():
            return 0.0

        values = [float(item.strip()) for item in hours_csv.split(",")]

        if (
            not values
            or any(not math.isfinite(value) or value < 0 for value in values)
        ):
            return 0.0

        return sum(values) / len(values)
    except (ValueError, TypeError, AttributeError, ZeroDivisionError):
        return 0.0


def payable_fee(text):
    """Calculate fee including 18% tax, less a non-negative discount."""
    try:
        if not isinstance(text, str) or text.count("|") != 1:
            return 0.0

        fee_text, discount_text = text.split("|")
        fee = float(fee_text.strip())
        discount = float(discount_text.strip())

        if (
            not math.isfinite(fee)
            or not math.isfinite(discount)
            or fee < 0
            or discount < 0
        ):
            return 0.0

        return max(fee * 1.18 - discount, 0.0)
    except (ValueError, TypeError, AttributeError):
        return 0.0


def main():
    print("==== Running parse_enrolment ====")
    user_input = input("Enter age group:hours (e.g. toddler:25): ")
    result = parse_enrolment(user_input)
    print("Age Group and Hours:", result)

    print("\n==== Running hours_average ====")
    user_input = input("Enter weekly hours as CSV (e.g. 20,25,30): ")
    result = hours_average(user_input)
    print("Average Hours:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 3000|250): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()
