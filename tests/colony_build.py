from unittest.mock import patch

from . import MyTestCase, db, Colony

class RouteColonyBuild(MyTestCase):

    def create_app(self):
        return super().create_app()


    def setUp(self):
        return super().setUp()


    def tearDown(self):
        return super().tearDown()

# ================================================================

    # Open colony build page
    def test_colbuild_get(self):
        with patch('game.routes.get_colonies') as mock_colony:
            mock_colony.return_value = {'pages': {'build': {'activate': False}}}

            response = self.client.get("/game/colonies/1/build")
            self.assertEqual(response.status_code, 200)

    
    # Add new building and canneling
    def test_colbuild_build(self):      
        building = "sawmill" 

        response = self.client.post("/game/colonies/1/build", data={'build': building})
        self.assertEqual(response.status_code, 303)

        response = self.client.post("/game/colonies/1/build", data={'cannel': building})
        self.assertEqual(response.status_code, 303)


    # Canneling first build
    def test_colbuild_build_cannel_first(self):
        building = ["sawmill", "quarry"]
        self.client.post("/game/colonies/1/build", data={'build': building[0]})
        self.client.post("/game/colonies/1/build", data={'build': building[1]})

        build_now = Colony.query.filter_by(id=1).first().build_now
        before = build_now[building[0]]['build_start'][:-8]

        self.client.post("/game/colonies/1/build", data={'cannel': building[0]})
        build_now = Colony.query.filter_by(id=1).first().build_now
        after = build_now[building[1]]['build_start'][:-8]

        self.assertEqual(before, after)
