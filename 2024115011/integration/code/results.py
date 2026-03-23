"""Results module for StreetRace Manager."""

from dataclasses import dataclass

from streetrace_manager.inventory import InventoryModule
from streetrace_manager.race_management import RaceManagementModule


@dataclass
class RaceResult:
    """Represents one race completion record."""

    race_id: str
    placements: list[str]
    prize_awarded: int


class ResultsModule:
    """Records race outcomes, rankings, and prize money effects."""

    def __init__(self, race_module: RaceManagementModule, inventory_module: InventoryModule):
        self.race_module = race_module
        self.inventory = inventory_module
        self._driver_points: dict[str, int] = {}
        self._history: list[RaceResult] = []

    def record_race_result(self, race_id: str, placements: list[str], prize_money: int) -> RaceResult:
        """Record a race result, update rankings, and update cash balance."""
        normalized_race_id = race_id.strip().upper()
        race = self.race_module.get_race(normalized_race_id)

        if race.completed:
            raise ValueError("Race result has already been recorded.")
        if prize_money < 0:
            raise ValueError("Prize money must be non-negative.")
        if not placements:
            raise ValueError("Placements cannot be empty.")

        entered_drivers = {entry.member_id for entry in race.entries}
        normalized_placements = [member_id.strip().upper() for member_id in placements]

        for member_id in normalized_placements:
            if member_id not in entered_drivers:
                raise ValueError(f"Driver '{member_id}' was not entered in race '{normalized_race_id}'.")

        for points, member_id in zip([10, 6, 3], normalized_placements):
            self._driver_points[member_id] = self._driver_points.get(member_id, 0) + points

        self.inventory.add_cash(prize_money)
        race.completed = True

        result = RaceResult(
            race_id=normalized_race_id,
            placements=normalized_placements,
            prize_awarded=prize_money,
        )
        self._history.append(result)
        return result

    def get_driver_points(self, member_id: str) -> int:
        """Return total ranking points for a driver."""
        normalized_member_id = member_id.strip().upper()
        return self._driver_points.get(normalized_member_id, 0)

    def get_leaderboard(self) -> list[tuple[str, int]]:
        """Return sorted leaderboard as (member_id, points)."""
        return sorted(self._driver_points.items(), key=lambda item: item[1], reverse=True)

    def list_results(self) -> list[RaceResult]:
        """Return all recorded race results."""
        return list(self._history)
