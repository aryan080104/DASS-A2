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

Run tests:

```bash
python -m unittest tests/test_registration_module.py tests/test_crew_management_module.py -v
```
