from rest_framework.test import APITestCase
from .models import CustomUser, UserProfile
from .views import get_random, get_access_token, get_refresh_token
from message_control.tests import create_image, SimpleUploadedFile


class TestGenericFunctions(APITestCase):
    def test_get_random(self):
        rand1 = get_random(10)
        rand2 = get_random(10)
        rand3 = get_random(15)

        # check that we are getting a result
        self.assertTrue(rand1)

        # check that rand1 is not equal to rand2
        self.assertNotEqual(rand1, rand2)

        # check that the length of result is what is expected
        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)

    def test_get_access_token(self):
        payload = {
            "id": 1
        }

        token = get_access_token(payload)

        # check that we obtained a result
        self.assertTrue(token)

    def test_get_refresh_token(self):

        token = get_refresh_token()

        # check that we obtained a result
        self.assertTrue(token)


class TestAuth(APITestCase):
    login_url = "/user/login"
    register_url = "/user/register"
    refresh_url = "/user/refresh"

    def test_register(self):
        payload = {
            "username": "ekrem12",
            "password": "ekrm123",
            "email": "ekrem12@yahoo.com"
        }

        response = self.client.post(self.register_url, data=payload)

        # check that we obtain a status of 201
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        payload = {
            "username": "ekrem12",
            "password": "ekrm123",
            "email": "ekrem12@yahoo.com"
        }

        # register
        self.client.post(self.register_url, data=payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        result = response.json()
        # print(result)

        # check that we obtain a status of 200
        self.assertEqual(response.status_code, 200)

        # check that we obtained both the refresh and access token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):
        payload = {
            "username": "ekrem12",
            "password": "ekrm123",
            "email": "ekrem12@yahoo.com"
        }

        # register
        self.client.post(self.register_url, data=payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        refresh = response.json()["refresh"]

        # get refresh
        response = self.client.post(
            self.refresh_url, data={"refresh": refresh})
        result = response.json()

        # check that we obtain a status of 200
        self.assertEqual(response.status_code, 200)

        # check that we obtained both the refresh and access token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])


class TestUserInfo(APITestCase):
    profile_url = "/user/profile"
    file_upload_url = "/message/file-upload"

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='ekrem11', password='ekrm123')

        self.client.force_authenticate(user=self.user)

    def test_post_user_profile(self):

        payload = {
            "user_id": self.user.id,
            "first_name": "Ekrem",
            "last_name": "Sarı",
            "caption": "Being alive is different from living",
            "about": "I am a passionation lover of ART, graphics and creation"
        }

        response = self.client.post(
            self.profile_url, data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Ekrem")
        self.assertEqual(result["last_name"], "Sarı")
        self.assertEqual(result["user"]["username"], "ekrem11")

    def test_post_user_profile_with_profile_picture(self):

        # upload image
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {
            "file_upload": avatar_file
        }

        # processing
        response = self.client.post(
            self.file_upload_url, data=data)
        result = response.json()

        payload = {
            "user_id": self.user.id,
            "first_name": "Ekrem",
            "last_name": "Sarı",
            "caption": "Being alive is different from living",
            "about": "I am a passionation lover of ART, graphics and creation",
            "profile_picture_id": result["id"]
        }

        response = self.client.post(
            self.profile_url, data=payload)
        result = response.json()
        # print(result)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Ekrem")
        self.assertEqual(result["last_name"], "Sarı")
        self.assertEqual(result["user"]["username"], "ekrem11")
        self.assertEqual(result["profile_picture"]["id"], 1)

    def test_update_user_profile(self):
        # create profile

        payload = {
            "user_id": self.user.id,
            "first_name": "Ekrem",
            "last_name": "Sarı",
            "caption": "Being alive is different from living",
            "about": "I am a passionation lover of ART, graphics and creation"
        }

        response = self.client.post(
            self.profile_url, data=payload)
        result = response.json()

        # --- created profile

        payload = {
            "first_name": "Z.Ekrem",
            "last_name": "Sarı",
        }

        response = self.client.patch(
            self.profile_url + f"/{result['id']}", data=payload)
        result = response.json()
        print(result)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["first_name"], "Z.Ekrem")
        self.assertEqual(result["last_name"], "Sarı")
        self.assertEqual(result["user"]["username"], "ekrem11")
