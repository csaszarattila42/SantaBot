import unittest
import karma_routine


class KarmaRoutineTest(unittest.TestCase):
    def load_action_types_skips_field_names(self):
        actions_dict = karma_routine.load_action_types("karma.csv")
        with self.assertRaises(KeyError):
            print(actions_dict["action"])

    def load_action_types_actually_loads(self):
        actions_dict = karma_routine.load_action_types("karma.cvs")
        self.assertEqual(actions_dict["gave money to a charity"], "nice")
        self.assertEqual(actions_dict["listened to their partner"], "nice")
        self.assertEqual(actions_dict["lied to a friend"], "naughty")
        self.assertEqual(actions_dict["got too drunk"], "naughty")


if __name__ == '__main__':
    unittest.main()
