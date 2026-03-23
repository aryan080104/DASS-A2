"""Mission Planning module for StreetRace Manager."""

from dataclasses import dataclass

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.inventory import InventoryModule


@dataclass
class Mission:
    """Represents a mission definition and assignment state."""

    mission_id: str
    mission_type: str
    required_roles: list[str]
    assigned_members: list[str]
    status: str


class MissionPlanningModule:
    """Assigns missions and validates role availability across modules."""

    def __init__(self, crew_module: CrewManagementModule, inventory_module: InventoryModule):
        self.crew = crew_module
        self.inventory = inventory_module
        self._missions: dict[str, Mission] = {}

    def create_mission(self, mission_id: str, mission_type: str, required_roles: list[str]) -> Mission:
        """Create a mission with required crew roles."""
        normalized_id = mission_id.strip().upper()
        normalized_type = mission_type.strip().lower()
        roles = [r.strip().lower() for r in required_roles if r.strip()]

        if not normalized_id:
            raise ValueError("Mission ID is required.")
        if not normalized_type:
            raise ValueError("Mission type is required.")
        if not roles:
            raise ValueError("Mission requires at least one role.")
        if normalized_id in self._missions:
            raise ValueError(f"Mission '{normalized_id}' already exists.")

        mission = Mission(
            mission_id=normalized_id,
            mission_type=normalized_type,
            required_roles=roles,
            assigned_members=[],
            status="planned",
        )
        self._missions[normalized_id] = mission
        return mission

    def assign_mission(self, mission_id: str, member_ids: list[str]) -> Mission:
        """Assign members to a mission if all required roles are satisfied."""
        normalized_id = mission_id.strip().upper()
        if normalized_id not in self._missions:
            raise KeyError(f"Mission '{normalized_id}' not found.")

        mission = self._missions[normalized_id]
        normalized_members = [member_id.strip().upper() for member_id in member_ids]
        role_pool: list[str] = []

        for member_id in normalized_members:
            profile = self.crew.get_profile(member_id)
            role_pool.append(profile.role)

        for needed_role in mission.required_roles:
            if needed_role not in role_pool:
                raise ValueError(f"Required role '{needed_role}' is unavailable.")

        mission.assigned_members = normalized_members
        mission.status = "assigned"
        return mission

    def can_start_mission(self, mission_id: str) -> bool:
        """Return True when a mission has all required roles assigned."""
        normalized_id = mission_id.strip().upper()
        mission = self.get_mission(normalized_id)
        if mission.status != "assigned":
            return False

        role_pool: list[str] = []
        for member_id in mission.assigned_members:
            profile = self.crew.get_profile(member_id)
            role_pool.append(profile.role)

        for needed_role in mission.required_roles:
            if needed_role not in role_pool:
                return False
        return True

    def start_mission(self, mission_id: str) -> Mission:
        """Start mission only if required roles are available."""
        normalized_id = mission_id.strip().upper()
        mission = self.get_mission(normalized_id)
        if not self.can_start_mission(normalized_id):
            raise ValueError("Mission cannot start because required roles are unavailable.")
        mission.status = "active"
        return mission

    def get_mission(self, mission_id: str) -> Mission:
        """Return mission by ID."""
        normalized_id = mission_id.strip().upper()
        if normalized_id not in self._missions:
            raise KeyError(f"Mission '{normalized_id}' not found.")
        return self._missions[normalized_id]

    def list_missions(self) -> list[Mission]:
        """Return all missions."""
        return list(self._missions.values())
