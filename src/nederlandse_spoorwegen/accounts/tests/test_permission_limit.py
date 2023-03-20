from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from .factories import StaffUserFactory, SuperUserFactory


class PasswordResetViewTests(TestCase):
    def setUp(self):
        super().setUp()

        self.superuser = SuperUserFactory.create(
            username="superuser", password="secret"
        )
        self.other_superuser = SuperUserFactory.create(
            username="other_superuser", password="secret"
        )

        self.less_perms_staff_user = StaffUserFactory.create(
            username="less_perms_staff_user", password="secret"
        )
        for p in Permission.objects.filter(
            content_type=ContentType.objects.get(app_label="accounts", model="user")
        ):
            self.less_perms_staff_user.user_permissions.add(p)

        self.more_perms_staff_user = StaffUserFactory.create(
            username="more_perms_staff_user", password="secret"
        )
        for p in Permission.objects.all():
            self.more_perms_staff_user.user_permissions.add(p)

    def _change_user(self, target_user, as_user):
        self.client.force_login(as_user)

        response = self.client.post(
            reverse("admin:accounts_user_change", args=(target_user.pk,)),
            {
                "username": "example",
                "date_joined_0": "2022-01-01",
                "date_joined_1": "12:00:00",
                "_save": "1",
            },
        )
        return response

    def test_change_user_as_superuser(self):
        response = self._change_user(
            target_user=self.other_superuser, as_user=self.superuser
        )
        self.assertEqual(response.status_code, 302, response.content)

    def test_change_superuser_as_non_superuser(self):
        response = self._change_user(
            target_user=self.superuser, as_user=self.more_perms_staff_user
        )
        self.assertEqual(response.status_code, 200, response.content)

    def test_change_user_as_user_with_less_permissions(self):
        response = self._change_user(
            target_user=self.more_perms_staff_user, as_user=self.less_perms_staff_user
        )
        self.assertEqual(response.status_code, 200, response.content)

    def test_change_user_as_user_with_more_permissions(self):
        response = self._change_user(
            target_user=self.less_perms_staff_user, as_user=self.more_perms_staff_user
        )
        self.assertEqual(response.status_code, 302, response.content)

    def _change_password_page(self, target_user, as_user):
        self.client.force_login(as_user)

        change_password_url = "{}{}/password/".format(
            reverse("admin:accounts_user_changelist"), target_user.pk
        )
        response = self.client.get(change_password_url, follow=True)
        return response

    def test_change_password_as_superuser(self):
        response = self._change_password_page(
            target_user=self.other_superuser, as_user=self.superuser
        )
        self.assertEqual(response.status_code, 200, response.content)

    def test_change_password_as_non_superuser(self):
        response = self._change_password_page(
            target_user=self.superuser, as_user=self.more_perms_staff_user
        )
        self.assertEqual(response.status_code, 403, response.content)

    def test_change_password_as_user_with_less_permissions(self):
        response = self._change_password_page(
            target_user=self.more_perms_staff_user, as_user=self.less_perms_staff_user
        )
        self.assertEqual(response.status_code, 403, response.content)

    def test_change_password_as_user_with_more_permissions(self):
        response = self._change_password_page(
            target_user=self.less_perms_staff_user, as_user=self.more_perms_staff_user
        )
        self.assertEqual(response.status_code, 200, response.content)
