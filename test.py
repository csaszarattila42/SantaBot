import unittest
import math
import karma_routine
import ideal_present_routine
import delivery_routine


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
        temp_maxDiff = self.maxDiff
        self.maxDiff = None
        self.assertEqual(profiles_list[3], {
            "name": "Noah Jones",
            "actions": "smoked in a restaurant toilet,loves their family,"
            "cut the line,stole money,doesn't respect their parents,"
            "donated money to Wikipedia,listened to their partner,is always late,"
            "used renewable energies,swears a lot,got too drunk,"
            "didn't silence the cellphone in a cinema,gave money to a charity,"
            "threw garbage on the street,helped a stranger",
            "ideal present categories": "decoration,travel"
        })
        self.maxDiff = temp_maxDiff

    def test_calc_karma(self):
        profiles = [
            {"name": "Cucc", "actions": "planted a tree, stole money"},
            {"name": "Valami", "actions": "helped a friend, planted a tree"}
        ]
        actions = {
            "planted a tree": 1,
            "stole money": -1,
            "helped a friend": 1
        }
        processed = karma_routine.calculate_karma(actions, profiles)

        self.assertEqual(processed[0]["karma"], 0)
        self.assertEqual(processed[1]["karma"], 2)


class IdealPresentRoutineTest(unittest.TestCase):
    def test_load_presents_skips_fieldnames(self):
        presents_dict = ideal_present_routine.load_present_types("presents.csv")

        with self.assertRaises(KeyError):
            print(presents_dict["presents"])

    def test_load_presents_actually_loads(self):
        presents_dict = ideal_present_routine.load_present_types("presents.csv")

        self.assertEqual(presents_dict["pets"], "hamster,cat,dog,bird,turtle")
        self.assertEqual(presents_dict["cloths"], "pants,socks,sweater,t-shirt,jacket")

    def test_calc_presents(self):
        test_profiles = [
            {
                "name": "MacNaughty",
                "karma": -2,
                "ideal present categories": "pets,sports"
            },
            {
                "name": "Mr. Normal",
                "karma": 2,
                "ideal present categories": "pets,cloths"
            },
            {
                "name": "Ms. Saint",
                "karma": 9,
                "ideal present categories": "sports,pets,music"
            }
        ]
        test_presents = {
            "pets": "hamster,cat,dog,bird,turtle",
            "sports": "basket ball,sneakers,dumbbells,fit ball,bicycle,sports bag",
            "cloths": "pants,socks,sweater,t-shirt,jacket",
            "music": "rock album,guitar,Spotify subscription,concert tickets,headphones"
        }
        processed = ideal_present_routine.calc_presents(test_profiles, test_presents)

        self.assertEqual(processed[0]["presents"][0], ideal_present_routine.NAUGHTY_PRESENT)
        self.assertIn(processed[1]["presents"][0], test_presents["pets"].split(","))
        self.assertIn(processed[2]["presents"][0], test_presents["sports"].split(","))
        self.assertIn(processed[2]["presents"][1], test_presents["pets"].split(","))


class DeliveryRoutineTest(unittest.TestCase):
    def test_edge_distance_zero(self):
        edge1 = delivery_routine.Edge(delivery_routine.Point(1, 1), delivery_routine.Point(1, 1))
        edge2 = delivery_routine.Edge(delivery_routine.Point(2.3, 6), delivery_routine.Point(2.3, 6))
        edge3 = delivery_routine.Edge(delivery_routine.Point(-4.2, -1), delivery_routine.Point(-4.2, -1))

        self.assertEqual(edge1.distance(), 0)
        self.assertEqual(edge2.distance(), 0)
        self.assertEqual(edge3.distance(), 0)

    def test_edge_distance_square_diagonal(self):
        edge1 = delivery_routine.Edge(delivery_routine.Point(1, 1), delivery_routine.Point(3, 3))
        edge2 = delivery_routine.Edge(delivery_routine.Point(-1, 3), delivery_routine.Point(-2, 4))
        edge3 = delivery_routine.Edge(delivery_routine.Point(-1.5, -2), delivery_routine.Point(3.5, -6))

        self.assertAlmostEqual(edge1.distance(), math.sqrt(2)*2)
        self.assertAlmostEqual(edge2.distance(), math.sqrt(2))
        self.assertAlmostEqual(edge3.distance(), math.sqrt(2)*4)


if __name__ == '__main__':
    unittest.main()
