from unittest.mock import patch

from . import MyTestCase, db

class RouteGame(MyTestCase):

    def create_app(self):
        return super().create_app()


    def setUp(self):
        return super().setUp()


    def tearDown(self):
        return super().tearDown()

# ================================================================

    # Open game
    def test_game_get(self):
        response = self.client.get("/game")
        self.assertEqual(response.status_code, 200)

    
    # -------- Create a colony --------


    # Correct
    def test_game_colony_create(self):
        with patch('game.routes.current_user') as mock_user:
            mock_user.id = 1

            response = self.client.post('/game', data={'name': "TesterColony2"})
            self.assertEqual(response.status_code, 303)


    # Name is too short
    def test_game_colony_name_short(self):
        with patch('game.routes.current_user') as mock_user:
            mock_user.id = 1

            response = self.client.post('/game', data={'name': "x"})
            self.assertEqual(response.status_code, 400)


    # Name of colony is already in database
    def test_game_colony_name_exist(self):
        with patch('game.routes.current_user') as mock_user:
            mock_user.id = 1

            response = self.client.post('/game', data={'name': "TesterColony"})
            self.assertEqual(response.status_code, 400)