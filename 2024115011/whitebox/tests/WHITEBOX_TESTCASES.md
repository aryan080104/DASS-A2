# White-Box Test Cases (MoneyPoly)

This document contains the complete white-box test design for MoneyPoly, aligned with Assignment 2 requirements:
- all key decision branches,
- important variable states,
- and relevant edge cases.

Source test file: [whitebox/tests/test_whitebox_moneyopoly.py](whitebox/tests/test_whitebox_moneyopoly.py)

---

## 1) Detailed Test Cases

### WB-TC-01: Dice roll stays within valid range
- **Mapped function/test**: `Dice.roll()` / `test_dice_roll_uses_full_six_sided_range`
- **Scenario**: Validate all random outcomes are legal for two six-sided dice
- **Input / Setup**: Create `Dice()`, call `roll()` 500 times
- **Expected Output**:
  - `die1 ∈ [1,6]`
  - `die2 ∈ [1,6]`
  - `total ∈ [2,12]`
- **Actual Output**: All assertions pass
- **Justification**: Prevents illegal movement values and validates random branch boundaries

### WB-TC-02: Salary is credited when passing/landing on Go
- **Mapped function/test**: `Player.move()` / `test_player_move_collects_salary_when_passing_or_landing_go`
- **Scenario**: Go-crossing logic at board boundary
- **Input / Setup**:
  - case A: start `39`, move `1`
  - case B: start `38`, move `3`
- **Expected Output**:
  - case A -> position `0`, `+200` balance
  - case B -> position `1`, `+200` balance
- **Actual Output**: Both paths pass
- **Justification**: Covers wraparound branch and reward branch at edge of board length

### WB-TC-03: Monopoly state requires full group ownership
- **Mapped function/test**: `PropertyGroup.all_owned_by()` / `test_property_group_requires_all_tiles_for_monopoly_state`
- **Scenario**: Partial ownership vs complete ownership in same color group
- **Input / Setup**:
  - Two properties in one group
  - ownership split across two players, then changed to one player
- **Expected Output**:
  - split ownership => `False`
  - full ownership => `True`
- **Actual Output**: Both assertions pass
- **Justification**: Validates decision path controlling monopoly-dependent behavior (e.g., rent scaling)

### WB-TC-04: Rent payment transfers money correctly
- **Mapped function/test**: `Game.pay_rent()` / `test_pay_rent_transfers_money_to_owner`
- **Scenario**: Player lands on owned property
- **Input / Setup**:
  - Two-player game
  - Assign property owner
  - Trigger rent payment
- **Expected Output**:
  - payer balance decreases by rent
  - owner balance increases by same rent
- **Actual Output**: Transfer validated
- **Justification**: Confirms core financial data-flow and state transition between objects

### WB-TC-05: Purchase allowed when balance equals property price
- **Mapped function/test**: `Game.buy_property()` / `test_buy_property_allows_exact_balance`
- **Scenario**: Equality boundary in affordability check
- **Input / Setup**:
  - buyer balance set exactly to property price
  - execute buy
- **Expected Output**:
  - purchase success (`True`)
  - buyer balance becomes `0`
  - owner set correctly
  - property added to buyer assets
- **Actual Output**: All checks pass
- **Justification**: Covers boundary value (`balance == price`) that often fails with strict `>` comparisons

### WB-TC-06: Jail fine branch releases player and deducts fine
- **Mapped function/test**: `Game._handle_jail_turn()` / `test_jail_voluntary_fine_deducts_player_balance`
- **Scenario**: Player chooses to pay jail fine
- **Input / Setup**:
  - force jail state
  - patch user confirmation to `True`
  - isolate side effects (dice/movement)
- **Expected Output**:
  - balance decreases by `50`
  - `in_jail` becomes `False`
- **Actual Output**: Both conditions pass
- **Justification**: Covers decision branch in jail flow and verifies correct state unlock

### WB-TC-07: Winner selection returns maximum net worth
- **Mapped function/test**: `Game.find_winner()` / `test_find_winner_returns_highest_net_worth`
- **Scenario**: Multiple players with distinct final balances
- **Input / Setup**: balances = `[100, 300, 200]`
- **Expected Output**: player with `300` returned
- **Actual Output**: Correct winner returned
- **Justification**: Verifies comparison branch and avoids wrong aggregate/ordering logic

### WB-TC-08: Loan issuance updates bank and player states
- **Mapped function/test**: `Bank.give_loan()` / `test_bank_loan_reduces_bank_balance_and_increases_player_balance`
- **Scenario**: Loan transaction
- **Input / Setup**:
  - initial bank balance
  - player balance + loan `75`
- **Expected Output**:
  - bank decreases by `75`
  - player increases by `75`
- **Actual Output**: Transaction state updates pass
- **Justification**: Confirms invariant for opposite-side money movement

### WB-TC-09: Invalid numeric input falls back to default
- **Mapped function/test**: `ui.safe_int_input()` / `test_safe_int_input_returns_default_on_invalid_text`
- **Scenario**: Non-numeric CLI input
- **Input / Setup**:
  - mock input as `"not-a-number"`
  - default = `99`
- **Expected Output**: return `99`
- **Actual Output**: returns `99`
- **Justification**: Covers exception/error-handling branch for robust CLI behavior

---

## 2) Branch and State Coverage Mapping

### Branches covered
1. Dice boundaries and total range decision paths
2. Salary credit branch on Go crossing
3. Monopoly true/false ownership branch
4. Rent transfer branch (payer/owner updates)
5. Property affordability boundary branch
6. Jail decision branch (pay fine path)
7. Winner selection branch (max-value path)
8. Input parsing valid/invalid branch

### Key variable states validated
- `player.balance` transitions (increase/decrease/zero boundary)
- `player.position` wraparound (`39 -> 0`)
- `player.in_jail` state transition (`True -> False`)
- `property.owner` assignment and ownership consistency
- `bank.balance` consistency after loan
- dice state variables `die1`, `die2`

### Edge cases covered
- exact boundary balance (`balance == price`)
- board boundary crossing near max index
- invalid text input for integer parser
- repeated randomized executions for dice boundary confidence

---

## 3) Errors / Logical Issues Found by White-Box Tests

Based on current white-box suite execution intent, the following defect categories are specifically targeted:
- incorrect boundary handling (Go, affordability, dice limits)
- inconsistent state transitions (jail release, ownership)
- money-flow mismatches (rent, loan transactions)
- input validation fallback behavior

Current test implementation serves as regression protection for these logic areas.

---

## 4) Execution Reference

- **Run command**:
  - `cd whitebox/tests`
  - `pytest test_whitebox_moneyopoly.py -v`
- **Test file**: [whitebox/tests/test_whitebox_moneyopoly.py](whitebox/tests/test_whitebox_moneyopoly.py)
- **Total white-box test cases**: **9**

This file is the complete white-box test case list for submission.
