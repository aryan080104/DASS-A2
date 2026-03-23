"""Tests for StreetRace registration module."""

import unittest

from streetrace_manager.registration import RegistrationModule


class TestRegistrationModule(unittest.TestCase):
    """Validate registration module behavior."""

    def setUp(self):
        self.registration = RegistrationModule()

    def test_register_member_success(self):
        member = self.registration.register_member("d01", "Rico", "Driver")

        self.assertEqual(member.member_id, "D01")
        self.assertEqual(member.name, "Rico")
        self.assertEqual(member.role, "driver")
        self.assertTrue(self.registration.is_registered("D01"))

    def test_register_duplicate_member_id_raises_error(self):
        self.registration.register_member("d01", "Rico", "Driver")

        with self.assertRaises(ValueError):
            self.registration.register_member("D01", "Maya", "Mechanic")

    def test_get_unregistered_member_raises_error(self):
        with self.assertRaises(KeyError):
            self.registration.get_member("UNKNOWN")


if __name__ == "__main__":
    unittest.main()
