"""Tests for StreetRace results module."""

import unittest

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.inventory import InventoryModule
from streetrace_manager.race_management import RaceManagementModule
from streetrace_manager.registration import RegistrationModule
from streetrace_manager.results import ResultsModule


class TestResultsModule(unittest.TestCase):
    """Validate race result recording and integration effects."""

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

        self.registration.register_member("d01", "Rico", "driver")
        self.registration.register_member("d02", "Lena", "driver")
        self.crew.assign_role("d01", "driver")
        self.crew.assign_role("d02", "driver")

        self.inventory.add_car("c01", "Skyline")
        self.inventory.add_car("c02", "Supra")

        self.race_mgmt.create_race("r101", "Harbor Run")
        self.race_mgmt.enter_race("r101", "d01", "c01")
        self.race_mgmt.enter_race("r101", "d02", "c02")

    def test_record_result_updates_points_and_cash(self):
        starting_cash = self.inventory.get_cash_balance()

        result = self.results.record_race_result("r101", ["d02", "d01"], 500)

        self.assertEqual(result.race_id, "R101")
        self.assertEqual(self.results.get_driver_points("d02"), 10)
        self.assertEqual(self.results.get_driver_points("d01"), 6)
        self.assertEqual(self.inventory.get_cash_balance(), starting_cash + 500)
        self.assertTrue(self.race_mgmt.get_race("r101").completed)

    def test_record_result_rejects_driver_not_in_race(self):
        with self.assertRaises(ValueError):
            self.results.record_race_result("r101", ["x99"], 100)

    def test_record_result_cannot_be_recorded_twice(self):
        self.results.record_race_result("r101", ["d01", "d02"], 300)

        with self.assertRaises(ValueError):
            self.results.record_race_result("r101", ["d01", "d02"], 300)


if __name__ == "__main__":
    unittest.main()
