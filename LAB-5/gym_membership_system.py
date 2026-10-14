
"""Fitness gym membership registration and renewal module."""

import hashlib
import os
import secrets

members = {
    "M01": {
        "name": "Alex",
        "plan": "Gold",
        "months_left": 6,
        "fee": 600.0,
    },
    "M02": {
        "name": "Brooke",
        "plan": "Silver",
        "months_left": 1,
        "fee": 350.0,
    },
    "M03": {
        "name": "Chris",
        "plan": "Platinum",
        "months_left": 12,
        "fee": 1000.0,
    },
}


def register_member(m_id, name, plan, months, member_log=None):
    """Register a new gym member."""
    if member_log is None:
        member_log = []

    if m_id in members or months <= 0:
        return False

    members[m_id] = {
        "name": name,
        "plan": plan,
        "months_left": months,
        "fee": 50.0 * months,
    }

    member_log.append(f"Registered {m_id} for {months} months")
    return True


def cancel_membership(m_id):
    """Cancel a member's gym membership."""
    try:
        del members[m_id]
    except KeyError:
        pass


def check_membership_status(m_id):
    """Return whether a member has an active membership."""
    if members.get(m_id) is None:
        return False

    return members[m_id]["months_left"] > 0


def calculate_renewal_rate(m_id, discount_expr):
    """Calculate a renewal rate using an approved discount multiplier."""
    fee = members[m_id]["fee"]

    allowed_multipliers = {
        "base_fee * 0.85": 0.85,
        "base_fee * 0.90": 0.90,
        "base_fee * 0.95": 0.95,
        "base_fee": 1.0,
    }

    if discount_expr not in allowed_multipliers:
        raise ValueError("Unsupported discount expression")

    return fee * allowed_multipliers[discount_expr]


def generate_member_hash(m_id):
    """Generate a SHA-256 hash for a member identifier."""
    return hashlib.sha256(m_id.encode()).hexdigest()


def generate_locker_pin():
    """Generate a cryptographically secure locker PIN."""
    return secrets.randbelow(9000) + 1000


def export_member_roster(filename="gym_roster.txt"):
    """Export the member roster to a text file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(members))

    print(f"Roster exported to: {filename}")


def get_active_summary(member_records):
    """Count members with active memberships."""
    return sum(
        details["months_left"] > 0
        for details in member_records.values()
    )


def main():
    """Run the gym membership demonstration."""
    gym_api_secret = os.environ.get("GYM_API_SECRET")

    register_member("M04", "Diana", "Gold", 3)
    cancel_membership("M02")

    print("Is M01 active:", check_membership_status("M01"))
    print(
        "Renewal Fee:",
        calculate_renewal_rate("M01", "base_fee * 0.85"),
    )
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())

    export_member_roster()

    print("Active count:", get_active_summary(members))
    print("Portal secret configured:", bool(gym_api_secret))


if __name__ == "__main__":
    main()
