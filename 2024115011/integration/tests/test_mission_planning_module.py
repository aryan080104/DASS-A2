"""Tests for StreetRace mission planning module."""

import unittest

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.inventory import InventoryModule
from streetrace_manager.mission_planning import MissionPlanningModule
from streetrace_manager.registration import RegistrationModule


class TestMissionPlanningModule(unittest.TestCase):
    """Validate mission assignment and role-based start checks."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(starting_cash=500)
        self.missions = MissionPlanningModule(self.crew, self.inventory)

        self.registration.register_member("d01", "Rico", "driver")
        self.registration.register_member("m01", "Maya", "mechanic")
        self.crew.assign_role("d01", "driver")
        self.crew.assign_role("m01", "mechanic")

        self.missions.create_mission("m100", "delivery", ["driver", "mechanic"])

    def test_assign_mission_with_required_roles(self):
        mission = self.missions.assign_mission("M100", ["D01", "M01"])

        self.assertEqual(mission.status, "assigned")
        self.assertTrue(self.missions.can_start_mission("M100"))

    def test_assign_mission_fails_when_role_missing(self):
        with self.assertRaises(ValueError):
            self.missions.assign_mission("M100", ["D01"])

    def test_start_mission_requires_valid_assignment(self):
        self.missions.assign_mission("M100", ["D01", "M01"])
        started = self.missions.start_mission("M100")

        self.assertEqual(started.status, "active")

    def test_start_mission_fails_when_not_assignable(self):
        with self.assertRaises(ValueError):
            self.missions.start_mission("M100")


if __name__ == "__main__":
    unittest.main()
