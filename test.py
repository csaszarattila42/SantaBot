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
        edge_1 = delivery_routine.Edge(delivery_routine.Point(1, 1), delivery_routine.Point(1, 1))
        edge_2 = delivery_routine.Edge(delivery_routine.Point(2.3, 6), delivery_routine.Point(2.3, 6))
        edge_3 = delivery_routine.Edge(delivery_routine.Point(-4.2, -1), delivery_routine.Point(-4.2, -1))

        self.assertEqual(edge_1.distance, 0)
        self.assertEqual(edge_2.distance, 0)
        self.assertEqual(edge_3.distance, 0)

    def test_edge_distance_square_diagonal(self):
        edge_1 = delivery_routine.Edge(delivery_routine.Point(1, 1), delivery_routine.Point(3, 3))
        edge_2 = delivery_routine.Edge(delivery_routine.Point(-1, 3), delivery_routine.Point(-2, 4))
        edge_3 = delivery_routine.Edge(delivery_routine.Point(-1.5, -2), delivery_routine.Point(2.5, -6))

        self.assertAlmostEqual(edge_1.distance, math.sqrt(2)*2)
        self.assertAlmostEqual(edge_2.distance, math.sqrt(2))
        self.assertAlmostEqual(edge_3.distance, math.sqrt(2)*4)

    def test_edge_equality(self):
        point_a = delivery_routine.Point(0.2, 3)
        point_b = delivery_routine.Point(-2.1, 1)
        point_c = delivery_routine.Point(-0.6, -1.5)
        edge_1 = delivery_routine.Edge(point_a, point_c)
        edge_2 = delivery_routine.Edge(point_b, point_a)
        edge_3 = delivery_routine.Edge(point_c, point_a)
        edge_4 = delivery_routine.Edge(delivery_routine.Point(-2.1, 1), delivery_routine.Point(0.2, 3))

        self.assertEqual(edge_1, edge_1)
        self.assertEqual(edge_3, edge_1)
        self.assertEqual(edge_2, edge_4)

        self.assertNotEqual(edge_1, edge_2)
        self.assertNotEqual(edge_4, edge_3)
        self.assertNotEqual(edge_3, edge_2)

    def test_connecting_point_equal_edges(self):
        point_a = delivery_routine.Point(0.2, 3)
        point_b = delivery_routine.Point(-2.1, 1)
        point_c = delivery_routine.Point(-0.6, -1.5)
        edge_1 = delivery_routine.Edge(point_a, point_c)
        edge_2 = delivery_routine.Edge(point_b, point_a)
        edge_3 = delivery_routine.Edge(point_c, point_a)
        edge_4 = delivery_routine.Edge(delivery_routine.Point(-2.1, 1), delivery_routine.Point(0.2, 3))

        self.assertIsNone(edge_1.get_connecting_point(edge_1))
        self.assertIsNone(edge_3.get_connecting_point(edge_1))
        self.assertIsNone(edge_2.get_connecting_point(edge_4))

    def test_connecting_point_no_point(self):
        point_a = delivery_routine.Point(0.2, 3)
        point_b = delivery_routine.Point(-2.1, 1)
        point_c = delivery_routine.Point(-0.6, -1.5)
        point_d = delivery_routine.Point(3.4, -3.7)
        edge_1 = delivery_routine.Edge(point_a, point_c)
        edge_2 = delivery_routine.Edge(point_b, point_d)
        edge_3 = delivery_routine.Edge(point_b, point_a)
        edge_4 = delivery_routine.Edge(point_c, point_d)

        self.assertIsNone(edge_1.get_connecting_point(edge_2))
        self.assertIsNone(edge_3.get_connecting_point(edge_4))

    def test_connecting_point(self):
        point_a = delivery_routine.Point(0.2, 3)
        point_b = delivery_routine.Point(-2.1, 1)
        point_c = delivery_routine.Point(-0.6, -1.5)
        point_d = delivery_routine.Point(3.4, -3.7)
        edge_1 = delivery_routine.Edge(point_a, point_c)
        edge_2 = delivery_routine.Edge(point_b, point_d)
        edge_3 = delivery_routine.Edge(point_b, point_a)
        edge_4 = delivery_routine.Edge(point_c, point_d)

        self.assertEqual(edge_1.get_connecting_point(edge_3), point_a)
        self.assertEqual(edge_2.get_connecting_point(edge_4), point_d)
        self.assertEqual(edge_4.get_connecting_point(edge_1), point_c)
        self.assertEqual(edge_3.get_connecting_point(edge_2), point_b)

    def test_path_init(self):
        points = [
            delivery_routine.Point(3, 1),   # 0 A
            delivery_routine.Point(0, 1),   # 1 B
            delivery_routine.Point(-3, 1),  # 2 C
            delivery_routine.Point(3, 5),   # 3 D
            delivery_routine.Point(0, 5),   # 4 E
            delivery_routine.Point(-3, 5)   # 5 F
        ]
        edges = [
            delivery_routine.Edge(points[0], points[1]),  # 0
            delivery_routine.Edge(points[4], points[0]),  # 1
            delivery_routine.Edge(points[0], points[5]),  # 2
            delivery_routine.Edge(points[3], points[1]),  # 3
            delivery_routine.Edge(points[1], points[5]),  # 4
            delivery_routine.Edge(points[2], points[3]),  # 5
            delivery_routine.Edge(points[2], points[4]),  # 6
            delivery_routine.Edge(points[5], points[3])   # 7
        ]
        path1 = [edges[2], edges[7], edges[5]]
        path2 = [edges[6], edges[1], edges[0], edges[3], ]


if __name__ == '__main__':
    unittest.main()
