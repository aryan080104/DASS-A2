"""Inventory module for StreetRace Manager."""

from dataclasses import dataclass


@dataclass
class Car:
    """Represents a race car entry in inventory."""

    car_id: str
    model: str
    condition: str = "ready"


class InventoryModule:
    """Tracks cars, spare parts, tools, and cash balance."""

    def __init__(self, starting_cash: int = 0):
        if starting_cash < 0:
            raise ValueError("Starting cash cannot be negative.")
        self._cash_balance = starting_cash
        self._cars: dict[str, Car] = {}
        self._spare_parts: dict[str, int] = {}
        self._tools: dict[str, int] = {}

    def get_cash_balance(self) -> int:
        """Return current cash balance."""
        return self._cash_balance

    def add_cash(self, amount: int) -> int:
        """Increase cash balance and return the new value."""
        if amount < 0:
            raise ValueError("Cash amount must be non-negative.")
        self._cash_balance += amount
        return self._cash_balance

    def spend_cash(self, amount: int) -> int:
        """Decrease cash balance and return the new value."""
        if amount < 0:
            raise ValueError("Cash amount must be non-negative.")
        if amount > self._cash_balance:
            raise ValueError("Insufficient cash balance.")
        self._cash_balance -= amount
        return self._cash_balance

    def add_car(self, car_id: str, model: str) -> Car:
        """Add a car to inventory."""
        normalized_id = car_id.strip().upper()
        normalized_model = model.strip()
        if not normalized_id:
            raise ValueError("Car ID is required.")
        if not normalized_model:
            raise ValueError("Car model is required.")
        if normalized_id in self._cars:
            raise ValueError(f"Car '{normalized_id}' already exists.")

        car = Car(normalized_id, normalized_model, condition="ready")
        self._cars[normalized_id] = car
        return car

    def mark_car_condition(self, car_id: str, condition: str) -> Car:
        """Update condition for a car (ready/damaged/repairing)."""
        normalized_id = car_id.strip().upper()
        normalized_condition = condition.strip().lower()
        if normalized_condition not in {"ready", "damaged", "repairing"}:
            raise ValueError("Invalid car condition.")
        if normalized_id not in self._cars:
            raise KeyError(f"Car '{normalized_id}' not found.")

        self._cars[normalized_id].condition = normalized_condition
        return self._cars[normalized_id]

    def get_car(self, car_id: str) -> Car:
        """Return car by ID."""
        normalized_id = car_id.strip().upper()
        if normalized_id not in self._cars:
            raise KeyError(f"Car '{normalized_id}' not found.")
        return self._cars[normalized_id]

    def list_cars(self) -> list[Car]:
        """Return all cars in inventory."""
        return list(self._cars.values())

    def add_spare_part(self, part_name: str, quantity: int = 1) -> int:
        """Increase spare part count and return new quantity."""
        normalized_name = part_name.strip().lower()
        if not normalized_name:
            raise ValueError("Part name is required.")
        if quantity <= 0:
            raise ValueError("Part quantity must be greater than zero.")
        self._spare_parts[normalized_name] = self._spare_parts.get(normalized_name, 0) + quantity
        return self._spare_parts[normalized_name]

    def use_spare_part(self, part_name: str, quantity: int = 1) -> int:
        """Use spare part quantity and return remaining quantity."""
        normalized_name = part_name.strip().lower()
        if quantity <= 0:
            raise ValueError("Part quantity must be greater than zero.")
        current = self._spare_parts.get(normalized_name, 0)
        if quantity > current:
            raise ValueError("Insufficient spare parts in inventory.")
        remaining = current - quantity
        self._spare_parts[normalized_name] = remaining
        return remaining

    def get_spare_part_qty(self, part_name: str) -> int:
        """Return spare part quantity for given part."""
        normalized_name = part_name.strip().lower()
        return self._spare_parts.get(normalized_name, 0)

    def add_tool(self, tool_name: str, quantity: int = 1) -> int:
        """Increase tool count and return new quantity."""
        normalized_name = tool_name.strip().lower()
        if not normalized_name:
            raise ValueError("Tool name is required.")
        if quantity <= 0:
            raise ValueError("Tool quantity must be greater than zero.")
        self._tools[normalized_name] = self._tools.get(normalized_name, 0) + quantity
        return self._tools[normalized_name]

    def get_tool_qty(self, tool_name: str) -> int:
        """Return tool quantity for given tool."""
        normalized_name = tool_name.strip().lower()
        return self._tools.get(normalized_name, 0)
