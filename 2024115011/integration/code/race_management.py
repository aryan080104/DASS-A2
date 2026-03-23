"""Race Management module for StreetRace Manager."""

from dataclasses import dataclass, field

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.inventory import InventoryModule
from streetrace_manager.registration import RegistrationModule


@dataclass
class RaceEntry:
    """Represents one driver+car entry in a race."""

    member_id: str
    car_id: str


@dataclass
class Race:
    """Represents a race with registered entries."""

    race_id: str
    title: str
    entries: list[RaceEntry] = field(default_factory=list)
    completed: bool = False


class RaceManagementModule:
    """Creates races and validates race entry rules across modules."""

    def __init__(
        self,
        registration_module: RegistrationModule,
        crew_module: CrewManagementModule,
        inventory_module: InventoryModule,
    ):
        self.registration = registration_module
        self.crew = crew_module
        self.inventory = inventory_module
        self._races: dict[str, Race] = {}

    def create_race(self, race_id: str, title: str) -> Race:
        """Create and store a new race."""
        normalized_id = race_id.strip().upper()
        normalized_title = title.strip()
        if not normalized_id:
            raise ValueError("Race ID is required.")
        if not normalized_title:
            raise ValueError("Race title is required.")
        if normalized_id in self._races:
            raise ValueError(f"Race '{normalized_id}' already exists.")

        race = Race(normalized_id, normalized_title)
        self._races[normalized_id] = race
        return race

    def enter_race(self, race_id: str, member_id: str, car_id: str) -> RaceEntry:
        """Enter a crew member and car into a race after validation."""
        normalized_race_id = race_id.strip().upper()
        normalized_member_id = member_id.strip().upper()
        normalized_car_id = car_id.strip().upper()

        if normalized_race_id not in self._races:
            raise KeyError(f"Race '{normalized_race_id}' not found.")
        race = self._races[normalized_race_id]
        if race.completed:
            raise ValueError("Cannot enter a completed race.")

        if not self.registration.is_registered(normalized_member_id):
            raise ValueError("Member must be registered before entering a race.")

        profile = self.crew.get_profile(normalized_member_id)
        if profile.role != "driver":
            raise ValueError("Only crew members with role 'driver' may enter races.")

        car = self.inventory.get_car(normalized_car_id)
        if car.condition != "ready":
            raise ValueError("Only cars in 'ready' condition may enter races.")

        for existing in race.entries:
            if existing.member_id == normalized_member_id:
                raise ValueError("Driver already entered in this race.")
            if existing.car_id == normalized_car_id:
                raise ValueError("Car already used in this race.")

        entry = RaceEntry(normalized_member_id, normalized_car_id)
        race.entries.append(entry)
        return entry

    def get_race(self, race_id: str) -> Race:
        """Return a race by ID."""
        normalized_race_id = race_id.strip().upper()
        if normalized_race_id not in self._races:
            raise KeyError(f"Race '{normalized_race_id}' not found.")
        return self._races[normalized_race_id]

    def list_races(self) -> list[Race]:
        """Return all races."""
        return list(self._races.values())
