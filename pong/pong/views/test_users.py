from django.test import TestCase
from django.urls import reverse
from pong.models.user import User
import jwt
from django.conf import settings
from datetime import datetime
from PIL import Image
import tempfile
import os
import uuid


def create_user_with_tokens():
    user = User.objects.create_user(
        name="ユーザー名",
        nickname="sample",
        email="example@email.com",
        password="p4s$W0rd",
    )
    token_payload = {
        "uuid": str(user.uuid),
        "exp": datetime.utcnow() + settings.JWT_AUTH["JWT_EXPIRATION_DELTA"],
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(
        token_payload,
        settings.JWT_AUTH["JWT_PRIVATE_KEY"],
        algorithm=settings.JWT_AUTH["JWT_ALGORITHM"],
    )
    refresh_token_payload = {
        "uuid": str(user.uuid),
        "exp": datetime.utcnow() + settings.JWT_AUTH["JWT_REFRESH_EXPIRATION_DELTA"],
        "iat": datetime.utcnow(),
    }
    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.JWT_AUTH["JWT_PRIVATE_KEY"],
        algorithm=settings.JWT_AUTH["JWT_ALGORITHM"],
    )
    return user, token, refresh_token


class GetUserTest(TestCase):
    def setUp(self):
        self.user, self.token, self.refresh_token = create_user_with_tokens()
        self.client.cookies["token"] = self.token
        self.client.cookies["refresh_token"] = self.refresh_token

    def test_get_user_normal(self):
        response = self.client.get(
            reverse("pong:user", kwargs={"uuid": self.user.uuid}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_patch_user_normal(self):
        response = self.client.patch(
            reverse("pong:user", kwargs={"uuid": self.user.uuid}),
            {"name": "changed"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "changed")

    def test_get_user_not_allowed_method(self):
        response = self.client.post(
            reverse("pong:user", kwargs={"uuid": self.user.uuid}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_user_not_found(self):
        response = self.client.get(
            reverse(
                "pong:user", kwargs={"uuid": "b4cf1ef4-1cab-490b-a32c-f6528f95c796"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)


class UserIconTest(TestCase):
    def setUp(self):
        self.user, self.token, self.refresh_token = create_user_with_tokens()
        self.client.cookies["token"] = self.token
        self.client.cookies["refresh_token"] = self.refresh_token

    def test_user_icon_post_normal(self):
        image = Image.new("RGB", (100, 100), color="red")
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file)
        tmp_file.seek(0)

        with open(tmp_file.name, "rb") as img:
            response = self.client.post(
                reverse("pong:user_icon", kwargs={"uuid": str(self.user.uuid)}),
                {"icon": img},
                format="multipart",
            )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.icon.name.startswith("uploads/"))

    def test_user_icon_post_no_file(self):
        response = self.client.post(
            reverse("pong:user_icon", kwargs={"uuid": str(self.user.uuid)})
        )

        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertFalse(self.user.icon.name.startswith("uploads/"))

    def test_user_icon_post_invalid_data(self):
        image = "string"

        response = self.client.post(
            reverse("pong:user_icon", kwargs={"uuid": str(self.user.uuid)}),
            {"icon": image},
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertFalse(self.user.icon.name.startswith("uploads/"))

    def test_user_icon_post_user_not_found(self):
        image = Image.new("RGB", (100, 100), color="red")
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file)
        tmp_file.seek(0)

        with open(tmp_file.name, "rb") as img:
            response = self.client.post(
                reverse("pong:user_icon", kwargs={"uuid": str(uuid.uuid4())}),
                {"icon": img},
                format="multipart",
            )

        self.assertEqual(response.status_code, 404)
        self.user.refresh_from_db()
        self.assertFalse(self.user.icon.name.startswith("uploads/"))

    def tearDown(self):
        if self.user.icon:
            if os.path.exists(self.user.icon.path):
                os.remove(self.user.icon.path)


class OtherUserTest(TestCase):
    def setUp(self):
        self.user, self.token, self.refresh_token = create_user_with_tokens()
        self.client.cookies["token"] = self.token
        self.client.cookies["refresh_token"] = self.refresh_token

    def test_get_other_user_normal(self):
        response = self.client.get(
            reverse("pong:other_user", kwargs={"name": self.user.name}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_get_other_user_not_found(self):
        response = self.client.get(
            reverse("pong:other_user", kwargs={"name": "notfound"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_get_other_user_not_allowed_method(self):
        response = self.client.post(
            reverse("pong:other_user", kwargs={"name": self.user.name}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class SearchedUserTest(TestCase):
    def setUp(self):
        self.user, self.token, self.refresh_token = create_user_with_tokens()
        self.client.cookies["token"] = self.token
        self.client.cookies["refresh_token"] = self.refresh_token

    def test_get_searched_user_normal(self):
        response = self.client.get(
            reverse("pong:searched_users", kwargs={"name": self.user.name}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_get_other_user_not_found(self):
        response = self.client.get(
            reverse("pong:searched_users", kwargs={"name": "notfound"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_get_other_user_not_allowed_method(self):
        response = self.client.post(
            reverse("pong:searched_users", kwargs={"name": self.user.name}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
