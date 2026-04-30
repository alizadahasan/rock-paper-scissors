import unittest

import project


class DetermineWinnerTests(unittest.TestCase):
    def setUp(self):
        project.user_score = 0
        project.computer_score = 0

    def test_tie_does_not_change_scores(self):
        self.assertEqual(project.determine_winner("rock", "rock"), "It's a tie!")
        self.assertEqual(project.user_score, 0)
        self.assertEqual(project.computer_score, 0)

    def test_user_win_increments_user_score(self):
        self.assertEqual(project.determine_winner("paper", "rock"), "You win!")
        self.assertEqual(project.user_score, 1)
        self.assertEqual(project.computer_score, 0)

    def test_computer_win_increments_computer_score(self):
        self.assertEqual(project.determine_winner("scissors", "rock"), "You lose!")
        self.assertEqual(project.user_score, 0)
        self.assertEqual(project.computer_score, 1)


if __name__ == "__main__":
    unittest.main()
