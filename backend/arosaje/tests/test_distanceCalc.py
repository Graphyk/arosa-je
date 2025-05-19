from arosaje.services import calculate_distance
from django.test import TestCase

class DistanceCalcTestCase(TestCase):

    def test_distance_calc(self):
        self.assertAlmostEqual(
            3659,
            calculate_distance(49.77099519999999, 4.7084253, 49.7392619, 4.721925),
            0
        )

        self.assertEqual(
            calculate_distance(49.77099519999999, 4.7084253, 49.7392619, 4.721925),
            calculate_distance(49.7392619, 4.721925, 49.77099519999999, 4.7084253),
        )
