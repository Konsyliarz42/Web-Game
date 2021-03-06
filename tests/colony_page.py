from unittest.mock import patch

from . import MyTestCase, db

class RouteColonyPage(MyTestCase):

    def create_app(self):
        return super().create_app()


    def setUp(self):
        return super().setUp()


    def tearDown(self):
        return super().tearDown()

# ================================================================

    # Open colony page
    def test_colpage_get(self):
        with patch('game.routes.get_colonies') as mock_colony:
            mock_colony = dict()

            response = self.client.get("/game/colonies/1")
            self.assertEqual(response.status_code, 200)
