"""Tests for StreetRace race management module."""

import unittest

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.inventory import InventoryModule
from streetrace_manager.race_management import RaceManagementModule
from streetrace_manager.registration import RegistrationModule


class TestRaceManagementModule(unittest.TestCase):
    """Validate race creation and race entry integration rules."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(starting_cash=2000)
        self.race_mgmt = RaceManagementModule(
            self.registration,
            self.crew,
            self.inventory,
        )

        self.race_mgmt.create_race("r100", "Downtown Sprint")
        self.registration.register_member("d01", "Rico", "driver")
        self.crew.assign_role("d01", "driver")
        self.inventory.add_car("c01", "Nissan Skyline")

    def test_enter_race_with_registered_driver_and_ready_car(self):
        entry = self.race_mgmt.enter_race("R100", "D01", "C01")

        self.assertEqual(entry.member_id, "D01")
        self.assertEqual(entry.car_id, "C01")
        self.assertEqual(len(self.race_mgmt.get_race("R100").entries), 1)

    def test_enter_race_requires_registered_member(self):
        with self.assertRaises(ValueError):
            self.race_mgmt.enter_race("R100", "X99", "C01")

    def test_enter_race_requires_driver_role(self):
        self.registration.register_member("m01", "Maya", "mechanic")
        self.crew.assign_role("m01", "mechanic")

        with self.assertRaises(ValueError):
            self.race_mgmt.enter_race("R100", "M01", "C01")

    def test_enter_race_rejects_damaged_car(self):
        self.inventory.mark_car_condition("C01", "damaged")

        with self.assertRaises(ValueError):
            self.race_mgmt.enter_race("R100", "D01", "C01")


if __name__ == "__main__":
    unittest.main()
