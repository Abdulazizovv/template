from django.test import TestCase

from apps.botapp.models import TelegramUser


class BaseModelSoftDeleteTests(TestCase):
    def setUp(self):
        self.user = TelegramUser.objects.create(telegram_id=1, username="alice")

    def test_default_manager_hides_deleted_rows(self):
        self.user.delete()
        self.assertFalse(TelegramUser.objects.filter(pk=self.user.pk).exists())

    def test_all_objects_still_sees_deleted_rows(self):
        self.user.delete()
        self.assertTrue(TelegramUser.all_objects.filter(pk=self.user.pk).exists())
        self.assertTrue(TelegramUser.all_objects.deleted().filter(pk=self.user.pk).exists())

    def test_restore_brings_row_back_to_default_manager(self):
        self.user.delete()
        deleted = TelegramUser.all_objects.get(pk=self.user.pk)
        deleted.restore()
        self.assertTrue(TelegramUser.objects.filter(pk=self.user.pk).exists())

    def test_hard_delete_removes_row_entirely(self):
        pk = self.user.pk
        self.user.hard_delete()
        self.assertFalse(TelegramUser.all_objects.filter(pk=pk).exists())

    def test_is_active_and_is_deleted_properties(self):
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_deleted)
        self.user.delete()
        self.assertFalse(self.user.is_active)
        self.assertTrue(self.user.is_deleted)


class PingTaskTests(TestCase):
    def test_ping_returns_pong(self):
        from apps.common.tasks import ping

        self.assertEqual(ping.apply().get(), "pong")
