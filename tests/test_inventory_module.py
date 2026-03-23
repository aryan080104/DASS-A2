"""Tests for StreetRace inventory module."""

import unittest

from streetrace_manager.inventory import InventoryModule


class TestInventoryModule(unittest.TestCase):
    """Validate inventory operations and constraints."""

    def setUp(self):
        self.inventory = InventoryModule(starting_cash=1000)

    def test_add_and_spend_cash(self):
        self.assertEqual(self.inventory.add_cash(250), 1250)
        self.assertEqual(self.inventory.spend_cash(200), 1050)

    def test_spend_cash_cannot_exceed_balance(self):
        with self.assertRaises(ValueError):
            self.inventory.spend_cash(5000)

    def test_add_car_and_update_condition(self):
        car = self.inventory.add_car("r1", "Nissan Skyline")
        self.assertEqual(car.car_id, "R1")
        self.assertEqual(car.condition, "ready")

        updated = self.inventory.mark_car_condition("R1", "damaged")
        self.assertEqual(updated.condition, "damaged")

    def test_spare_part_add_and_use(self):
        self.assertEqual(self.inventory.add_spare_part("turbo", 3), 3)
        self.assertEqual(self.inventory.use_spare_part("turbo", 2), 1)
        self.assertEqual(self.inventory.get_spare_part_qty("turbo"), 1)


if __name__ == "__main__":
    unittest.main()
