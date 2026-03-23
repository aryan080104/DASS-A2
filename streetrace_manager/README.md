# StreetRace Manager (Part 2)

## Module 1: Registration

Implemented features:
- Register crew members with `member_id`, `name`, and `role`
- Prevent duplicate member IDs
- Check registration status
- Fetch a registered member
- List all registered members

## Module 2: Crew Management

Implemented features:
- Assign role to a registered member
- Reject role assignment if member is unregistered
- Validate role against allowed role list
- Track and update skill level (1-10)
- List crew profiles by role

## Module 3: Inventory

Implemented features:
- Track cash balance (add and spend with validation)
- Track cars and update car condition (`ready`, `damaged`, `repairing`)
- Track spare parts quantity (add/use)
- Track tools quantity

## Module 4: Race Management

Implemented features:
- Create races
- Enter driver+car into races with integration checks
- Enforce business rules:
	- Member must be registered
	- Member role must be `driver`
	- Car must exist and be in `ready` condition
	- No duplicate driver/car entries in same race

## Module 5: Results

Implemented features:
- Record race outcomes using placement order
- Update driver ranking points (1st=10, 2nd=6, 3rd=3)
- Mark race as completed after recording result
- Update inventory cash balance with prize money
- Keep race result history and leaderboard

## Module 6: Mission Planning

Implemented features:
- Create missions with required role sets
- Assign crew members to missions
- Validate required roles before assignment
- Prevent mission start if required roles are unavailable
- Track mission status (`planned` → `assigned` → `active`)

## Module 7 (Extra): Maintenance

Implemented features:
- Repair damaged cars
- Require mechanic role for repair actions
- Consume spare parts during repair
- Update repaired car condition back to `ready`
- Keep repair history records

Run tests:

```bash
python -m unittest tests/test_registration_module.py tests/test_crew_management_module.py tests/test_inventory_module.py tests/test_race_management_module.py tests/test_results_module.py tests/test_mission_planning_module.py tests/test_maintenance_module.py -v
```
