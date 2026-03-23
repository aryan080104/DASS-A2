"""Tests for StreetRace crew management module."""

import unittest

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.registration import RegistrationModule


class TestCrewManagementModule(unittest.TestCase):
    """Validate role assignment and skill management behavior."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.registration.register_member("d01", "Rico", "driver")

    def test_assign_role_for_registered_member(self):
        profile = self.crew.assign_role("D01", "driver")

        self.assertEqual(profile.member_id, "D01")
        self.assertEqual(profile.role, "driver")
        self.assertEqual(profile.skill_level, 1)

    def test_assign_role_requires_registration(self):
        with self.assertRaises(ValueError):
            self.crew.assign_role("X99", "mechanic")

    def test_update_skill_in_valid_range(self):
        self.crew.assign_role("D01", "driver")
        profile = self.crew.update_skill("D01", 8)

        self.assertEqual(profile.skill_level, 8)

    def test_update_skill_out_of_range_raises_error(self):
        self.crew.assign_role("D01", "driver")

        with self.assertRaises(ValueError):
            self.crew.update_skill("D01", 11)


if __name__ == "__main__":
    unittest.main()
