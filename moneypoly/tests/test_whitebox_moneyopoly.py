import sys
import unittest
from pathlib import Path

# Make package importable when tests run from repository root.
PROJECT_SRC = Path(__file__).resolve().parents[1] / "moneypoly"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from moneypoly.dice import Dice  # noqa: E402
from moneypoly.player import Player  # noqa: E402


class TestMoneyPolyWhiteBox(unittest.TestCase):
    def test_dice_roll_uses_full_six_sided_range(self):
        """Branch/state test: every die value must stay inside [1, 6]."""
        dice = Dice()

        for _ in range(500):
            total = dice.roll()
            self.assertGreaterEqual(dice.die1, 1)
            self.assertLessEqual(dice.die1, 6)
            self.assertGreaterEqual(dice.die2, 1)
            self.assertLessEqual(dice.die2, 6)
            self.assertGreaterEqual(total, 2)
            self.assertLessEqual(total, 12)

    def test_player_move_collects_salary_when_passing_or_landing_go(self):
        """Branch test: salary branch should trigger whenever Go is crossed."""
        player = Player("A", balance=1000)

        player.position = 39
        player.move(1)
        self.assertEqual(player.position, 0)
        self.assertEqual(player.balance, 1200)

        player.position = 38
        player.move(3)
        self.assertEqual(player.position, 1)
        self.assertEqual(player.balance, 1400)


if __name__ == "__main__":
    unittest.main()
