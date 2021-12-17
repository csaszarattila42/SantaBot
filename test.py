import unittest
import karma_routine


class KarmaRoutineTest(unittest.TestCase):
    def test_load_action_types_skips_field_names(self):
        actions_dict = karma_routine.load_action_types("karma.csv")
        with self.assertRaises(KeyError):
            print(actions_dict["action"])

    def test_load_action_types_actually_loads(self):
        actions_dict = karma_routine.load_action_types("karma.csv")
        self.assertEqual(actions_dict["gave money to a charity"], 1)
        self.assertEqual(actions_dict["listened to their partner"], 1)
        self.assertEqual(actions_dict["lied to a friend"], -1)
        self.assertEqual(actions_dict["got too drunk"], -1)

    def test_load_person_profiles_have_names(self):
        profiles_list = karma_routine.load_person_profiles("profiles.csv")
        self.assertIn("name", profiles_list[0].keys())
        self.assertIn("name", profiles_list[5].keys())
        self.assertIn("name", profiles_list[30].keys())

    def test_load_person_profiles_have_actions(self):
        profiles_list = karma_routine.load_person_profiles("profiles.csv")
        self.assertIn("actions", profiles_list[8].keys())
        self.assertIn("actions", profiles_list[40].keys())
        self.assertIn("actions", profiles_list[22].keys())

    def test_load_person_profiles_person1(self):
        profiles_list = karma_routine.load_person_profiles("profiles.csv")
        self.assertEqual(profiles_list[3], {"name":"Noah Jones"\
            ,"actions":["smoked in a restaurant toilet",\
                "loves their family","cut the line","stole money"\
                ,"doesn't respect their parents","donated money to Wikipedia"\
                ,"listened to their partner","is always late","used renewable energies"\
                ,"swears a lot","got too drunk","didn't silence the cellphone in a cinema"\
                ,"gave money to a charity","threw garbage on the street","helped a stranger"]
            ,"ideal present categories":["decoration","travel"]\
            })

    def test_calc_karma(self):
        profiles = [
            {"name": "Cucc", "actions": ["planted a tree", "stole money"]},
            {"name": "Valami", "actions": ["helped a friend", "planted a tree"]}
        ]
        actions = {
            "planted a tree": 1,
            "stole money": -1,
            "helped a friend": 1
        }
        processed = karma_routine.calculate_karma(actions, profiles)

        self.assertEqual(processed[0]["karma"], 0)
        self.assertEqual(processed[1]["karma"], 2)


if __name__ == '__main__':
    unittest.main()
