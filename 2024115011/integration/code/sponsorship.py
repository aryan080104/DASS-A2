"""Sponsorship module (extra) for StreetRace Manager."""

from dataclasses import dataclass

from streetrace_manager.inventory import InventoryModule
from streetrace_manager.results import ResultsModule


@dataclass
class SponsorshipContract:
    """Represents one sponsor contract tied to a driver target."""

    contract_id: str
    sponsor_name: str
    target_driver_id: str
    min_points: int
    payout: int
    paid: bool = False


class SponsorshipModule:
    """Manages sponsor contracts and payout flow into inventory cash."""

    def __init__(self, results_module: ResultsModule, inventory_module: InventoryModule):
        self.results = results_module
        self.inventory = inventory_module
        self._contracts: dict[str, SponsorshipContract] = {}

    def create_contract(
        self,
        contract_id: str,
        sponsor_name: str,
        target_driver_id: str,
        min_points: int,
        payout: int,
    ) -> SponsorshipContract:
        """Create a sponsorship contract for a target driver."""
        normalized_id = contract_id.strip().upper()
        normalized_sponsor = sponsor_name.strip()
        normalized_driver = target_driver_id.strip().upper()

        if not normalized_id:
            raise ValueError("Contract ID is required.")
        if not normalized_sponsor:
            raise ValueError("Sponsor name is required.")
        if not normalized_driver:
            raise ValueError("Target driver ID is required.")
        if min_points < 0:
            raise ValueError("Minimum points cannot be negative.")
        if payout <= 0:
            raise ValueError("Payout must be greater than zero.")
        if normalized_id in self._contracts:
            raise ValueError(f"Contract '{normalized_id}' already exists.")

        contract = SponsorshipContract(
            contract_id=normalized_id,
            sponsor_name=normalized_sponsor,
            target_driver_id=normalized_driver,
            min_points=min_points,
            payout=payout,
        )
        self._contracts[normalized_id] = contract
        return contract

    def evaluate_contract(self, contract_id: str) -> SponsorshipContract:
        """Pay contract if target driver's points meet threshold."""
        normalized_id = contract_id.strip().upper()
        contract = self.get_contract(normalized_id)

        if contract.paid:
            return contract

        driver_points = self.results.get_driver_points(contract.target_driver_id)
        if driver_points >= contract.min_points:
            self.inventory.add_cash(contract.payout)
            contract.paid = True
        return contract

    def get_contract(self, contract_id: str) -> SponsorshipContract:
        """Return sponsorship contract by ID."""
        normalized_id = contract_id.strip().upper()
        if normalized_id not in self._contracts:
            raise KeyError(f"Contract '{normalized_id}' not found.")
        return self._contracts[normalized_id]

    def list_contracts(self) -> list[SponsorshipContract]:
        """Return all sponsorship contracts."""
        return list(self._contracts.values())
