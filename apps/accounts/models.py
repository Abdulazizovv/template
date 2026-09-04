from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model. Kept close to Django's default for now so admin/auth
    internals (which assume an integer-like pk) keep working; extend with
    project-specific fields here instead of swapping AbstractUser later."""
