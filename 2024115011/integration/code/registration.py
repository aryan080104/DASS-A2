"""Registration module for StreetRace Manager."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CrewMember:
    """Represents a registered crew member with an initial role."""

    member_id: str
    name: str
    role: str


class RegistrationModule:
    """Handles registration and lookup of crew members."""

    def __init__(self):
        self._members: dict[str, CrewMember] = {}

    def register_member(self, member_id: str, name: str, role: str) -> CrewMember:
        """Register a new crew member and return the created member object."""
        normalized_id = member_id.strip().upper()
        normalized_name = name.strip()
        normalized_role = role.strip().lower()

        if not normalized_id:
            raise ValueError("Member ID is required.")
        if not normalized_name:
            raise ValueError("Member name is required.")
        if not normalized_role:
            raise ValueError("Member role is required.")
        if normalized_id in self._members:
            raise ValueError(f"Member ID '{normalized_id}' is already registered.")

        member = CrewMember(
            member_id=normalized_id,
            name=normalized_name,
            role=normalized_role,
        )
        self._members[normalized_id] = member
        return member

    def is_registered(self, member_id: str) -> bool:
        """Return True if the given member ID already exists."""
        normalized_id = member_id.strip().upper()
        return normalized_id in self._members

    def get_member(self, member_id: str) -> CrewMember:
        """Return a registered member by ID."""
        normalized_id = member_id.strip().upper()
        if normalized_id not in self._members:
            raise KeyError(f"No member found with ID '{normalized_id}'.")
        return self._members[normalized_id]

    def list_members(self) -> list[CrewMember]:
        """Return all registered members."""
        return list(self._members.values())
