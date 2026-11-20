from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskHtmxTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)

    def test_index_renders_task_rows_from_the_shared_partial(self):
        task = Task.objects.create(user=self.user, title="Dashboard task")

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'id="row-{task.id}"', html=False)
        self.assertContains(response, "Dashboard task", html=False)

    def test_add_task_returns_a_task_row(self):
        response = self.client.post(
            reverse("add_task"),
            {"title": "Buy groceries"},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(user=self.user, title="Buy groceries").exists())
        self.assertContains(response, 'id="row-', html=False)
        self.assertContains(response, "Buy groceries", html=False)

    def test_add_task_rejects_empty_whitespace_and_overlong_titles(self):
        invalid_titles = (
            ("", "Task title cannot be empty."),
            ("   ", "Task title cannot be empty."),
            ("x" * 51, "Task title must be 50 characters or fewer."),
        )
        for title, message in invalid_titles:
            with self.subTest(title=title):
                response = self.client.post(
                    reverse("add_task"),
                    {"title": title},
                    HTTP_HX_REQUEST="true",
                )

                self.assertEqual(response.status_code, 400)
                self.assertContains(response, message, status_code=400)
                self.assertFalse(Task.objects.filter(user=self.user).exists())

    def test_add_task_trims_valid_titles_and_accepts_50_characters(self):
        for title, expected in (
            ("  Learn Django  ", "Learn Django"),
            ("x" * 50, "x" * 50),
            ("A valid title", "A valid title"),
        ):
            with self.subTest(title=title):
                response = self.client.post(
                    reverse("add_task"),
                    {"title": title},
                    HTTP_HX_REQUEST="true",
                )

                self.assertEqual(response.status_code, 200)
                self.assertTrue(
                    Task.objects.filter(user=self.user, title=expected).exists()
                )

    def test_update_task_rejects_empty_whitespace_and_overlong_titles(self):
        invalid_titles = (
            ("", "Task title cannot be empty."),
            ("   ", "Task title cannot be empty."),
            ("x" * 51, "Task title must be 50 characters or fewer."),
        )
        for title, message in invalid_titles:
            with self.subTest(title=title):
                task = Task.objects.create(user=self.user, title="Original title")
                response = self.client.post(
                    reverse("update", args=[task.id]),
                    {"title": title},
                    HTTP_HX_REQUEST="true",
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, message, status_code=200)
                self.assertContains(response, 'id="row-', html=False)
                task.refresh_from_db()
                self.assertEqual(task.title, "Original title")

    def test_update_task_trims_valid_titles_and_accepts_50_characters(self):
        for title, expected in (
            ("  Learn Django  ", "Learn Django"),
            ("x" * 50, "x" * 50),
            ("A valid title", "A valid title"),
        ):
            with self.subTest(title=title):
                task = Task.objects.create(user=self.user, title="Original title")
                response = self.client.post(
                    reverse("update", args=[task.id]),
                    {"title": title},
                    HTTP_HX_REQUEST="true",
                )

                self.assertEqual(response.status_code, 200)
                task.refresh_from_db()
                self.assertEqual(task.title, expected)

    def test_delete_task_route_deletes_owned_task(self):
        task = Task.objects.create(user=self.user, title="Delete me")

        response = self.client.delete(reverse("delete", args=[task.id]), HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
