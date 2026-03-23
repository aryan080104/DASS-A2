# StreetRace Manager – Integration Testing Report

## 2.1 Call Graph

### Hand-drawn call graph requirement
For submission, draw the call graph by hand and attach a clear image in this report section.

Suggested image filename to add to repo:
- streetrace_manager/call-graph-handdrawn.jpg

After adding image, include it like:
- `![Hand-drawn Call Graph](call-graph-handdrawn.jpg)`

### Function nodes to include
Use one node per function:

- `RegistrationModule.register_member()`
- `RegistrationModule.is_registered()`
- `RegistrationModule.get_member()`
- `CrewManagementModule.assign_role()`
- `CrewManagementModule.get_profile()`
- `InventoryModule.add_car()`
- `InventoryModule.get_car()`
- `InventoryModule.add_cash()`
- `InventoryModule.mark_car_condition()`
- `InventoryModule.use_spare_part()`
- `RaceManagementModule.create_race()`
- `RaceManagementModule.enter_race()`
- `RaceManagementModule.get_race()`
- `ResultsModule.record_race_result()`
- `ResultsModule.get_driver_points()`
- `MissionPlanningModule.create_mission()`
- `MissionPlanningModule.assign_mission()`
- `MissionPlanningModule.can_start_mission()`
- `MissionPlanningModule.start_mission()`
- `MaintenanceModule.repair_car()`
- `SponsorshipModule.create_contract()`
- `SponsorshipModule.evaluate_contract()`

### Cross-module call edges to show
Draw arrows for these calls:

1. `RaceManagementModule.enter_race()` → `RegistrationModule.is_registered()`
2. `RaceManagementModule.enter_race()` → `CrewManagementModule.get_profile()`
3. `RaceManagementModule.enter_race()` → `InventoryModule.get_car()`
4. `ResultsModule.record_race_result()` → `RaceManagementModule.get_race()`
5. `ResultsModule.record_race_result()` → `InventoryModule.add_cash()`
6. `MissionPlanningModule.assign_mission()` → `CrewManagementModule.get_profile()`
7. `MissionPlanningModule.can_start_mission()` → `CrewManagementModule.get_profile()`
8. `MaintenanceModule.repair_car()` → `CrewManagementModule.get_profile()`
9. `MaintenanceModule.repair_car()` → `InventoryModule.get_car()`
10. `MaintenanceModule.repair_car()` → `InventoryModule.use_spare_part()`
11. `MaintenanceModule.repair_car()` → `InventoryModule.mark_car_condition()`
12. `SponsorshipModule.evaluate_contract()` → `ResultsModule.get_driver_points()`
13. `SponsorshipModule.evaluate_contract()` → `InventoryModule.add_cash()`

---

## 2.2 Integration Test Design

All integration tests were implemented in:
- [tests/test_integration_streetrace.py](../tests/test_integration_streetrace.py)

### IT-01 Register driver then enter race
- **Scenario:** Register a driver, assign `driver` role, add ready car, and enter race.
- **Modules involved:** Registration, Crew Management, Inventory, Race Management.
- **Expected result:** Race entry succeeds.
- **Actual result:** Passed.
- **Errors found/fixed:** None in this flow after module implementation.
- **Why needed (simple):** Confirms core data flow from registration to race entry works end-to-end.

### IT-02 Enter race without registered driver
- **Scenario:** Try to enter race using unknown member ID.
- **Modules involved:** Race Management, Registration.
- **Expected result:** Entry is rejected with validation error.
- **Actual result:** Passed (error raised as expected).
- **Errors found/fixed:** None.
- **Why needed (simple):** Stops invalid race participants from bypassing registration.

### IT-03 Complete race updates results and inventory cash
- **Scenario:** Record race placements and prize money.
- **Modules involved:** Race Management, Results, Inventory.
- **Expected result:** Driver points update and inventory cash increases by prize amount.
- **Actual result:** Passed.
- **Errors found/fixed:** None.
- **Why needed (simple):** Verifies money and ranking updates are connected correctly.

### IT-04 Mission assignment validates required roles
- **Scenario:** Mission requires `driver` + `mechanic`, but only driver is assigned.
- **Modules involved:** Mission Planning, Crew Management.
- **Expected result:** Assignment fails with role availability error.
- **Actual result:** Passed (error raised as expected).
- **Errors found/fixed:** None.
- **Why needed (simple):** Ensures mission safety/business rules are enforced.

### IT-05 Damaged car repair requires mechanic and parts
- **Scenario:** Repair a damaged car with mechanic role and one spare part.
- **Modules involved:** Maintenance, Crew Management, Inventory.
- **Expected result:** Repair succeeds, part count decreases, car becomes `ready`.
- **Actual result:** Passed.
- **Errors found/fixed:** None.
- **Why needed (simple):** Confirms repair operations consume resources and update car state correctly.

### IT-06 Sponsorship payout after points threshold
- **Scenario:** Driver earns enough points; evaluate contract payout.
- **Modules involved:** Results, Sponsorship, Inventory.
- **Expected result:** Contract marked paid and inventory cash increases exactly once.
- **Actual result:** Passed.
- **Errors found/fixed:** None.
- **Why needed (simple):** Verifies delayed financial flow based on race performance.

---

## Integration Test Execution Summary

- File run: [tests/test_integration_streetrace.py](../tests/test_integration_streetrace.py)
- Total integration test cases: 6
- Passed: 6
- Failed: 0

Notes:
- Core required integration scenarios from assignment are covered.
- Additional integration paths include maintenance and sponsorship modules.
