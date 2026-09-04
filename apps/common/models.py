from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid


class AllObjectsManager(models.Manager):
    """Unfiltered manager: returns every row, including soft-deleted ones."""

    def active(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)


class BaseManager(AllObjectsManager):
    """Default manager: excludes soft-deleted rows. Use `all_objects` to see everything."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    """
    Base abstract model that provides:
    - UUID primary key
    - Timestamp fields (created_at, updated_at)
    - Soft delete functionality
    - Common utility methods
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name=_("Deleted at"))

    objects = BaseManager()
    all_objects = AllObjectsManager()

    def delete(self, using=None, keep_parents=False, hard=False):
        """
        Soft delete by default. Set hard=True for permanent deletion.
        """
        if hard:
            return super().delete(using=using, keep_parents=keep_parents)

        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
        return self

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete the object"""
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """Restore a soft-deleted object"""
        if self.deleted_at:
            self.deleted_at = None
            self.save(update_fields=['deleted_at'])
        return self

    def __str__(self):
        return str(self.id)

    @property
    def is_active(self):
        """Check if object is not deleted"""
        return self.deleted_at is None

    @property
    def is_deleted(self):
        """Check if object is deleted"""
        return self.deleted_at is not None

    @classmethod
    def get_field_names(cls):
        """Get list of all field names"""
        return [field.name for field in cls._meta.fields]

    @classmethod
    def get_fields(cls):
        """Get list of all fields"""
        return cls._meta.fields

    @classmethod
    def active_objects(cls):
        """Get queryset of active (non-deleted) objects"""
        return cls.objects.active()

    @classmethod
    def deleted_objects(cls):
        """Get queryset of deleted objects"""
        return cls.all_objects.deleted()

    class Meta:
        abstract = True
        ordering = ['-created_at']
        get_latest_by = 'created_at'
