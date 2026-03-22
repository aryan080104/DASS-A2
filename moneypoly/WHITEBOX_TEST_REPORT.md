# MoneyPoly White-Box Testing Report

## Scope
This report documents iterative white-box testing and fixes for the MoneyPoly codebase.
Each iteration fixes exactly one error and records:
- Why the test case is needed
- What failed
- What was changed
- How it was verified

---

## Iteration 1: Fix dice range bug (`Dice.roll()`)

### Why this test case is needed
Dice are core to movement. If a die cannot roll `6`, branch behavior (movement distance, landing tiles, jail streak flow) becomes biased.

### Error found
In `Dice.roll()`, both dice used `random.randint(1, 5)`, so value `6` was impossible.

### White-box test case
- Execute many rolls and assert:
  - `die1` and `die2` are each in `[1, 6]`
  - total is in `[2, 12]`
- This checks variable state boundaries and edge values.

### Fix applied
Updated `Dice.roll()` to use `random.randint(1, 6)` for both dice.

### Verification
- Added automated test: `test_dice_roll_uses_full_six_sided_range`.
- Test passes locally.
