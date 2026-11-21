from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskCrudTests(TestCase):
    def test_list_and_detail_tasks(self):
        task = Task.objects.create(
            title="Prepare report",
            description="Summarize this week's work",
        )

        list_response = self.client.get(reverse("home"))
        detail_response = self.client.get(
            reverse("task_detail", kwargs={"pk": task.pk})
        )

        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "Prepare report")
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Summarize this week's work", html=True)

    def test_create_task(self):
        response = self.client.post(
            reverse("task_create"),
            {
                "title": "Call supplier",
                "description": "Ask about delivery",
                "completed": "",
            },
        )

        task = Task.objects.get(title="Call supplier")
        self.assertRedirects(
            response,
            reverse("task_detail", kwargs={"pk": task.pk}),
        )
        self.assertFalse(task.completed)

    def test_update_task(self):
        task = Task.objects.create(title="Old title", description="Old description")

        response = self.client.post(
            reverse("task_update", kwargs={"pk": task.pk}),
            {
                "title": "Updated title",
                "description": "Updated description",
                "completed": "on",
            },
        )

        task.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("task_detail", kwargs={"pk": task.pk}),
        )
        self.assertEqual(task.title, "Updated title")
        self.assertTrue(task.completed)

    def test_delete_task_only_on_post(self):
        task = Task.objects.create(title="Remove this", description="")
        url = reverse("task_delete", kwargs={"pk": task.pk})

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())

        post_response = self.client.post(url)
        self.assertRedirects(post_response, reverse("home"))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
