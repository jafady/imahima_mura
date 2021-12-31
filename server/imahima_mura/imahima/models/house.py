from django.db import models
from .mixin import MyBaseModel

class HouseManager(models.Manager):
    def create_house(self, user, houseName, **extra_fields):
        """
        Creates and saves a House
        """
        house = self.model(
            houseName = houseName,
            create_user = user.username,
            update_user = user.username
        )

        house.save(using=self._db)
        return house


class House(MyBaseModel):
    houseName = models.TextField()

    objects = HouseManager()

    def __str__(self):
        return self.id



class HouseMateManager(models.Manager):
    def create_housemate(self, user, houseId, userId, **extra_fields):
        """
        Creates and saves a HouseMate
        """
        house = self.model(
            houseId = houseId,
            userId = userId,
            create_user = user.username,
            update_user = user.username
        )

        house.save(using=self._db)
        return house
    
    def accept_invitation(self, user, **extra_fields):
        house = self.model(
            isApproved = True,
            update_user = user.username
        )
        house.save(using=self._db)
        return house


class HouseMate(MyBaseModel):
    houseId = models.ForeignKey('House', to_field='id', on_delete=models.CASCADE, null=False)
    userId = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, null=False)
    isApproved = models.BooleanField(default=False)

    objects = HouseMateManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["houseId", "userId"],
                name="housemate_unique"
            ),
        ]

    def __str__(self):
        return id