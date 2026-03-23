"""Crew Management module for StreetRace Manager."""

from dataclasses import dataclass

from streetrace_manager.registration import RegistrationModule


@dataclass
class CrewProfile:
    """Represents role and skill level for a registered crew member."""

    member_id: str
    role: str
    skill_level: int


class CrewManagementModule:
    """Manages crew roles and skill levels for registered members."""

    VALID_ROLES = {"driver", "mechanic", "strategist", "scout"}

    def __init__(self, registration_module: RegistrationModule):
        self.registration = registration_module
        self._profiles: dict[str, CrewProfile] = {}

    def assign_role(self, member_id: str, role: str) -> CrewProfile:
        """Assign or update a role for a registered member."""
        normalized_id = member_id.strip().upper()
        normalized_role = role.strip().lower()

        if not self.registration.is_registered(normalized_id):
            raise ValueError(f"Member '{normalized_id}' must be registered first.")
        if normalized_role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{normalized_role}'.")

        profile = self._profiles.get(normalized_id)
        if profile is None:
            profile = CrewProfile(normalized_id, normalized_role, skill_level=1)
            self._profiles[normalized_id] = profile
        else:
            profile.role = normalized_role
        return profile

    def update_skill(self, member_id: str, skill_level: int) -> CrewProfile:
        """Set skill level (1-10) for a registered member profile."""
        normalized_id = member_id.strip().upper()
        if not self.registration.is_registered(normalized_id):
            raise ValueError(f"Member '{normalized_id}' must be registered first.")
        if not 1 <= skill_level <= 10:
            raise ValueError("Skill level must be between 1 and 10.")

        profile = self._profiles.get(normalized_id)
        if profile is None:
            registered_member = self.registration.get_member(normalized_id)
            profile = CrewProfile(normalized_id, registered_member.role, skill_level)
            self._profiles[normalized_id] = profile
        else:
            profile.skill_level = skill_level
        return profile

    def get_profile(self, member_id: str) -> CrewProfile:
        """Return profile for a member."""
        normalized_id = member_id.strip().upper()
        if normalized_id not in self._profiles:
            raise KeyError(f"No profile found for member '{normalized_id}'.")
        return self._profiles[normalized_id]

    def list_by_role(self, role: str) -> list[CrewProfile]:
        """Return all profiles that match the requested role."""
        normalized_role = role.strip().lower()
        return [p for p in self._profiles.values() if p.role == normalized_role]
