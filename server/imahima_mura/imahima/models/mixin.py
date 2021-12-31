from django.db import models
import uuid

class MyBaseModel(models.Model):
    class Meta:
        abstract = True

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)

    create_user = models.CharField(
        max_length=255,
        unique=False,
        blank=True
    )
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_user = models.CharField(
        max_length=255,
        unique=False,
        blank=True
    )
    update_datetime = models.DateTimeField(auto_now=True)