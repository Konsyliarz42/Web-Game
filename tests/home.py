from . import MyTestCase, db, MAIN_TESTER

class RouteHome(MyTestCase):

    def create_app(self):
        return super().create_app()


    def setUp(self):
        return super().setUp()


    def tearDown(self):
        return super().tearDown()
    

# ================================================================

    # Open home page
    def test_home_get(self):
        response = self.client.get("/home")
        self.assertEqual(response.status_code, 200)


    # -------- Register user --------


    # Correct
    def test_register_user(self):
        data = {
            'register': 'x',
            'login': '',
            'email': "tester@test.com",
            'password': "testPassword",
            'cpassword': "testPassword",
            'nick': "Tester2"
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 301)


    # Nick is too short
    def test_register_user_nick_short(self):
        data = {
            'register': 'x',
            'login': '',
            'email': "tester@test.com",
            'password': "testPassword",
            'cpassword': "testPassword",
            'nick': "x"
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 400)


    # Wrong cpassword
    def test_register_user_cpassword_wrong(self):
        data = {
            'register': 'x',
            'login': '',
            'email': "tester@test.com",
            'password': "testPassword",
            'cpassword': "testPass",
            'nick': "Tester2"
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 400)


    # Password is too short
    def test_register_user_password_short(self):
        data = {
            'register': 'x',
            'login': '',
            'email': "tester@test.com",
            'password': "test",
            'cpassword': "test",
            'nick': "Tester2"
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 400)


    # Wrong email
    def test_register_user_email_wrong(self):
        data = {
            'register': 'x',
            'login': '',
            'email': "tester@",
            'password': "testPassword",
            'cpassword': "testPassword",
            'nick': "Tester2"
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 400)


    # Email is already in database
    def test_register_user_email_exists(self):
        data = {
            'register': 'x',
            'login': '',
            'email': MAIN_TESTER['email'],
            'password': "testPassword",
            'cpassword': "testPassword",
            'nick': "Tester2"
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 400)


    # -------- Login user -------


    # Correct
    def test_login_user(self):
        data = {
            'register': '',
            'login': 'x',
            'email': MAIN_TESTER['email'],
            'password': MAIN_TESTER['password']
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 301)


    # Wrong email
    def test_login_user_email_wrong(self):
        data = {
            'register': '',
            'login': 'x',
            'email': "test@",
            'password': MAIN_TESTER['password']
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 400)


    # Email is not in database
    def test_login_user_email_not_exists(self):
        data = {
            'register': '',
            'login': 'x',
            'email': "test@test.com",
            'password': MAIN_TESTER['password']
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 400)


    # Wrong password
    def test_login_user_password_wrong(self):
        data = {
            'register': '',
            'login': 'x',
            'email': MAIN_TESTER['email'],
            'password': 'password'
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 400)


    # Password is too short
    def test_login_user_password_short(self):
        data = {
            'register': '',
            'login': 'x',
            'email': MAIN_TESTER['email'],
            'password': MAIN_TESTER['password'][:4]
        }

        response = self.client.post('/home', data=data)
        self.assertEqual(response.status_code, 400)