"""Tests for StreetRace sponsorship module."""

import unittest

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.inventory import InventoryModule
from streetrace_manager.race_management import RaceManagementModule
from streetrace_manager.registration import RegistrationModule
from streetrace_manager.results import ResultsModule
from streetrace_manager.sponsorship import SponsorshipModule


class TestSponsorshipModule(unittest.TestCase):
    """Validate sponsorship contract payout integration."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(starting_cash=1000)
        self.race_mgmt = RaceManagementModule(
            self.registration,
            self.crew,
            self.inventory,
        )
        self.results = ResultsModule(self.race_mgmt, self.inventory)
        self.sponsorship = SponsorshipModule(self.results, self.inventory)

        self.registration.register_member("d01", "Rico", "driver")
        self.registration.register_member("d02", "Lena", "driver")
        self.crew.assign_role("d01", "driver")
        self.crew.assign_role("d02", "driver")

        self.inventory.add_car("c01", "Skyline")
        self.inventory.add_car("c02", "Supra")

        self.race_mgmt.create_race("r301", "Ring Rush")
        self.race_mgmt.enter_race("r301", "d01", "c01")
        self.race_mgmt.enter_race("r301", "d02", "c02")

    def test_contract_pays_when_target_points_reached(self):
        self.results.record_race_result("r301", ["d01", "d02"], 200)
        self.sponsorship.create_contract("s01", "NitroCorp", "d01", 10, 300)

        start_cash = self.inventory.get_cash_balance()
        contract = self.sponsorship.evaluate_contract("s01")

        self.assertTrue(contract.paid)
        self.assertEqual(self.inventory.get_cash_balance(), start_cash + 300)

    def test_contract_not_paid_when_points_below_threshold(self):
        self.results.record_race_result("r301", ["d02", "d01"], 200)
        self.sponsorship.create_contract("s02", "TrackFuel", "d01", 20, 300)

        start_cash = self.inventory.get_cash_balance()
        contract = self.sponsorship.evaluate_contract("s02")

        self.assertFalse(contract.paid)
        self.assertEqual(self.inventory.get_cash_balance(), start_cash)

    def test_contract_pays_only_once(self):
        self.results.record_race_result("r301", ["d01", "d02"], 200)
        self.sponsorship.create_contract("s03", "BoostLabs", "d01", 10, 150)

        self.sponsorship.evaluate_contract("s03")
        cash_after_first = self.inventory.get_cash_balance()
        self.sponsorship.evaluate_contract("s03")

        self.assertEqual(self.inventory.get_cash_balance(), cash_after_first)


if __name__ == "__main__":
    unittest.main()
