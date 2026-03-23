"""Tests for StreetRace maintenance module."""

import unittest

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.inventory import InventoryModule
from streetrace_manager.maintenance import MaintenanceModule
from streetrace_manager.registration import RegistrationModule


class TestMaintenanceModule(unittest.TestCase):
    """Validate repair workflow integration across modules."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(starting_cash=1000)
        self.maintenance = MaintenanceModule(self.crew, self.inventory)

        self.registration.register_member("m01", "Maya", "mechanic")
        self.registration.register_member("d01", "Rico", "driver")
        self.crew.assign_role("m01", "mechanic")
        self.crew.assign_role("d01", "driver")

        self.inventory.add_car("c01", "Skyline")
        self.inventory.mark_car_condition("c01", "damaged")
        self.inventory.add_spare_part("turbo", 2)

    def test_repair_damaged_car_with_mechanic_and_part(self):
        record = self.maintenance.repair_car("c01", "m01", "turbo")

        self.assertEqual(record.car_id, "C01")
        self.assertEqual(record.mechanic_id, "M01")
        self.assertEqual(self.inventory.get_car("c01").condition, "ready")
        self.assertEqual(self.inventory.get_spare_part_qty("turbo"), 1)

    def test_repair_fails_for_non_mechanic(self):
        with self.assertRaises(ValueError):
            self.maintenance.repair_car("c01", "d01", "turbo")

    def test_repair_fails_when_car_not_damaged(self):
        self.inventory.mark_car_condition("c01", "ready")

        with self.assertRaises(ValueError):
            self.maintenance.repair_car("c01", "m01", "turbo")


if __name__ == "__main__":
    unittest.main()
