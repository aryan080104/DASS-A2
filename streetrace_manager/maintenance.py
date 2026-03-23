"""Maintenance module (extra) for StreetRace Manager."""

from dataclasses import dataclass

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.inventory import InventoryModule


@dataclass
class RepairRecord:
    """Represents a repair action on a damaged car."""

    car_id: str
    mechanic_id: str
    part_used: str


class MaintenanceModule:
    """Handles car repair workflow using crew and inventory data."""

    def __init__(self, crew_module: CrewManagementModule, inventory_module: InventoryModule):
        self.crew = crew_module
        self.inventory = inventory_module
        self._history: list[RepairRecord] = []

    def repair_car(self, car_id: str, mechanic_id: str, part_name: str) -> RepairRecord:
        """Repair a damaged car if mechanic role and spare parts are available."""
        normalized_car_id = car_id.strip().upper()
        normalized_mechanic_id = mechanic_id.strip().upper()
        normalized_part = part_name.strip().lower()

        profile = self.crew.get_profile(normalized_mechanic_id)
        if profile.role != "mechanic":
            raise ValueError("Only crew members with role 'mechanic' can repair cars.")

        car = self.inventory.get_car(normalized_car_id)
        if car.condition != "damaged":
            raise ValueError("Only damaged cars can be repaired.")

        self.inventory.use_spare_part(normalized_part, 1)
        self.inventory.mark_car_condition(normalized_car_id, "ready")

        record = RepairRecord(
            car_id=normalized_car_id,
            mechanic_id=normalized_mechanic_id,
            part_used=normalized_part,
        )
        self._history.append(record)
        return record

    def list_repairs(self) -> list[RepairRecord]:
        """Return all repair records."""
        return list(self._history)
