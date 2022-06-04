from django.db import models
from .mixin import MyBaseModel
from django.utils import timezone

class EventManager(models.Manager):
    def create_event(self, user, **extra_fields):
        """
        Creates and saves a Event
        """
        event = self.model(
            create_user = user.username,
            update_user = user.username
        )
        [setattr(event, k, v) for k, v in extra_fields.items()]

        event.save(using=self._db)
        return event
    
    def update_event(self, user, instance, **extra_fields):
        """
        update and saves a Event
        """
        [setattr(instance, k, v) for k, v in extra_fields.items()]
        instance.update_user = user.username
        instance.save(using=self._db)
        return instance


class Event(MyBaseModel):
    houseId = models.ForeignKey('House', to_field='id', on_delete=models.CASCADE, null=False, blank=True)

    eventName = models.TextField(blank=True)
    recruitmentNumbersLower = models.IntegerField(blank=True, default=0)
    recruitmentNumbersUpper = models.IntegerField(blank=True, default=0, null=True)

    location = models.TextField(blank=True)
    locationUrl = models.TextField(blank=True)

    startDate = models.DateTimeField(null=True, default=timezone.now)
    startTime = models.TimeField(null=True, default='00:00')
    endTime = models.TimeField(null=True, default='00:00')

    tyouseiUrl = models.TextField(blank=True)

    categoryId = models.ForeignKey('CategoryMaster', to_field='id', on_delete=models.CASCADE, null=False, blank=True)
    detail = models.TextField(blank=True)

    objects = EventManager()

    def __str__(self):
        return self.id



class EventMembersManager(models.Manager):
    def create_eventmembers(self, user, **extra_fields):
        """
        Creates and saves a EventMembers
        """
        event_members = self.model(
            create_user = user.username,
            update_user = user.username
        )
        [setattr(event_members, k, v) for k, v in extra_fields.items()]

        event_members.save(using=self._db)
        return event_members


class EventMembers(MyBaseModel):
    eventId = models.ForeignKey('Event', to_field='id', on_delete=models.CASCADE, null=False)
    userId = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, null=False)

    objects = EventMembersManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["eventId", "userId"],
                name="eventmembers_unique"
            ),
        ]

    def __str__(self):
        return id