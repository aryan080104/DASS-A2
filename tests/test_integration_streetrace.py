"""Cross-module integration tests for StreetRace Manager."""

import unittest

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.inventory import InventoryModule
from streetrace_manager.maintenance import MaintenanceModule
from streetrace_manager.mission_planning import MissionPlanningModule
from streetrace_manager.race_management import RaceManagementModule
from streetrace_manager.registration import RegistrationModule
from streetrace_manager.results import ResultsModule
from streetrace_manager.sponsorship import SponsorshipModule


class TestStreetRaceIntegration(unittest.TestCase):
    """Validate key integration flows across all modules."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(starting_cash=1000)
        self.race = RaceManagementModule(self.registration, self.crew, self.inventory)
        self.results = ResultsModule(self.race, self.inventory)
        self.missions = MissionPlanningModule(self.crew, self.inventory)
        self.maintenance = MaintenanceModule(self.crew, self.inventory)
        self.sponsorship = SponsorshipModule(self.results, self.inventory)

    def test_register_driver_then_enter_race_success(self):
        """Registered driver with ready car should be accepted into race."""
        self.registration.register_member("d01", "Rico", "driver")
        self.crew.assign_role("d01", "driver")
        self.inventory.add_car("c01", "Skyline")
        self.race.create_race("r500", "Dock Sprint")

        entry = self.race.enter_race("r500", "d01", "c01")

        self.assertEqual(entry.member_id, "D01")
        self.assertEqual(entry.car_id, "C01")
        self.assertEqual(len(self.race.get_race("r500").entries), 1)

    def test_enter_race_without_registered_driver_fails(self):
        """Race entry must fail for an unregistered member."""
        self.inventory.add_car("c01", "Skyline")
        self.race.create_race("r501", "Tunnel Clash")

        with self.assertRaises(ValueError):
            self.race.enter_race("r501", "d99", "c01")

    def test_complete_race_updates_results_rankings_and_cash(self):
        """Recording results should update points and prize money in inventory."""
        self.registration.register_member("d01", "Rico", "driver")
        self.registration.register_member("d02", "Lena", "driver")
        self.crew.assign_role("d01", "driver")
        self.crew.assign_role("d02", "driver")

        self.inventory.add_car("c01", "Skyline")
        self.inventory.add_car("c02", "Supra")

        self.race.create_race("r502", "Airport Dash")
        self.race.enter_race("r502", "d01", "c01")
        self.race.enter_race("r502", "d02", "c02")

        starting_cash = self.inventory.get_cash_balance()
        self.results.record_race_result("r502", ["d02", "d01"], 400)

        self.assertEqual(self.results.get_driver_points("d02"), 10)
        self.assertEqual(self.results.get_driver_points("d01"), 6)
        self.assertEqual(self.inventory.get_cash_balance(), starting_cash + 400)

    def test_assign_mission_validates_required_roles(self):
        """Mission assignment should fail when required role is unavailable."""
        self.registration.register_member("d01", "Rico", "driver")
        self.crew.assign_role("d01", "driver")

        self.missions.create_mission("m500", "rescue", ["driver", "mechanic"])

        with self.assertRaises(ValueError):
            self.missions.assign_mission("m500", ["d01"])

    def test_damaged_car_repair_flow_requires_mechanic_and_parts(self):
        """Damaged car repair should require mechanic role and consume inventory parts."""
        self.registration.register_member("m01", "Maya", "mechanic")
        self.crew.assign_role("m01", "mechanic")
        self.inventory.add_car("c99", "Evo")
        self.inventory.mark_car_condition("c99", "damaged")
        self.inventory.add_spare_part("engine_kit", 1)

        repair = self.maintenance.repair_car("c99", "m01", "engine_kit")

        self.assertEqual(repair.car_id, "C99")
        self.assertEqual(self.inventory.get_car("c99").condition, "ready")
        self.assertEqual(self.inventory.get_spare_part_qty("engine_kit"), 0)

    def test_sponsorship_payout_after_results_threshold(self):
        """Sponsor payout should flow into inventory only after points target is met."""
        self.registration.register_member("d01", "Rico", "driver")
        self.registration.register_member("d02", "Lena", "driver")
        self.crew.assign_role("d01", "driver")
        self.crew.assign_role("d02", "driver")
        self.inventory.add_car("c01", "Skyline")
        self.inventory.add_car("c02", "Supra")

        self.race.create_race("r503", "Bridge Run")
        self.race.enter_race("r503", "d01", "c01")
        self.race.enter_race("r503", "d02", "c02")
        self.results.record_race_result("r503", ["d01", "d02"], 200)

        self.sponsorship.create_contract("s500", "NitroCorp", "d01", 10, 300)
        start_cash = self.inventory.get_cash_balance()
        contract = self.sponsorship.evaluate_contract("s500")

        self.assertTrue(contract.paid)
        self.assertEqual(self.inventory.get_cash_balance(), start_cash + 300)


if __name__ == "__main__":
    unittest.main()
