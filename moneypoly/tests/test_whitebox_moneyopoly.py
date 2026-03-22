import sys
import unittest
from pathlib import Path

# Make package importable when tests run from repository root.
PROJECT_SRC = Path(__file__).resolve().parents[1] / "moneypoly"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from moneypoly.dice import Dice  # noqa: E402
from moneypoly.player import Player  # noqa: E402
from moneypoly.property import Property, PropertyGroup  # noqa: E402
from moneypoly.game import Game  # noqa: E402


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

    def test_property_group_requires_all_tiles_for_monopoly_state(self):
        """Branch/state test: partial ownership must not count as full group ownership."""
        owner = Player("Owner")
        other = Player("Other")
        group = PropertyGroup("Brown", "brown")
        p1 = Property("Mediterranean", 1, 60, 2, group)
        p2 = Property("Baltic", 3, 60, 4, group)

        p1.owner = owner
        p2.owner = other
        self.assertFalse(group.all_owned_by(owner))

        p2.owner = owner
        self.assertTrue(group.all_owned_by(owner))

    def test_pay_rent_transfers_money_to_owner(self):
        """Branch/state test: rent must decrease payer and increase owner."""
        game = Game(["P1", "P2"])
        payer = game.players[0]
        owner = game.players[1]
        prop = game.board.properties[0]
        prop.owner = owner

        payer_start = payer.balance
        owner_start = owner.balance
        rent = prop.get_rent()

        game.pay_rent(payer, prop)

        self.assertEqual(payer.balance, payer_start - rent)
        self.assertEqual(owner.balance, owner_start + rent)

    def test_buy_property_allows_exact_balance(self):
        """Edge case: player with balance == price should be able to buy."""
        game = Game(["P1", "P2"])
        buyer = game.players[0]
        prop = game.board.properties[0]
        buyer.balance = prop.price

        bought = game.buy_property(buyer, prop)

        self.assertTrue(bought)
        self.assertEqual(buyer.balance, 0)
        self.assertIs(prop.owner, buyer)
        self.assertIn(prop, buyer.properties)

    def test_jail_voluntary_fine_deducts_player_balance(self):
        """Branch test: choosing to pay jail fine must reduce player cash."""
        game = Game(["P1", "P2"])
        player = game.players[0]
        player.in_jail = True
        player.jail_turns = 0

        start_balance = player.balance

        from moneypoly import ui as ui_module  # local import to patch safely

        old_confirm = ui_module.confirm
        old_roll = game.dice.roll
        old_move_and_resolve = game._move_and_resolve

        try:
            ui_module.confirm = lambda _prompt: True
            game.dice.roll = lambda: 1
            game._move_and_resolve = lambda _player, _steps: None
            game._handle_jail_turn(player)
        finally:
            ui_module.confirm = old_confirm
            game.dice.roll = old_roll
            game._move_and_resolve = old_move_and_resolve

        self.assertEqual(player.balance, start_balance - 50)
        self.assertFalse(player.in_jail)


if __name__ == "__main__":
    unittest.main()
