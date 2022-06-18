from django.db import models
from .mixin import MyBaseModel
import datetime
from django.utils import timezone

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
    
    def update_house(self, user, instance, **extra_fields):
        """
        update and saves a House
        """
        [setattr(instance, k, v) for k, v in extra_fields.items()]
        instance.update_user = user.username
        instance.save(using=self._db)
        return instance


class House(MyBaseModel):
    houseName = models.TextField(blank=True)
    discordUrl = models.TextField(blank=True)
    discordNoticeUrl = models.TextField(blank=True)

    objects = HouseManager()

    def __str__(self):
        return self.id



class HouseMateManager(models.Manager):
    def create_housemate(self, user, houseId, userId, **extra_fields):
        """
        Creates and saves a HouseMate
        """
        housemate = self.model(
            houseId = houseId,
            userId = userId,
            create_user = user.username,
            update_user = user.username
        )

        housemate.save(using=self._db)
        return housemate
    
    def accept_invitation(self, user, **extra_fields):
        housemate = self.model(
            isApproved = True,
            update_user = user.username
        )
        housemate.save(using=self._db)
        return housemate


class HouseMate(MyBaseModel):
    houseId = models.ForeignKey('House', to_field='id', on_delete=models.CASCADE, null=False)
    userId = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, null=False)
    isApproved = models.BooleanField(default=False)
    lastMemberNoticeTime = models.DateTimeField(blank=True, default=timezone.now)
    lastMemberNoticeNumber = models.IntegerField(blank=True, default=0)

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


class InviteHouseTokenManager(models.Manager):
    def create_inviteHouseToken(self, user, houseId, **extra_fields):
        """
        Creates and saves a HouseMate
        """
        inviteHouse = self.model(
            houseId = houseId,
            validDateTime = datetime.datetime.now() + datetime.timedelta(days=7),
            create_user = user.username,
            update_user = user.username
        )

        inviteHouse.save(using=self._db)
        return inviteHouse


class InviteHouseToken(MyBaseModel):
    houseId = models.ForeignKey('House', to_field='id', on_delete=models.CASCADE, null=False)
    validDateTime = models.DateTimeField(blank=True)

    objects = InviteHouseTokenManager()

    def __str__(self):
        return id


class GameManager(models.Manager):
    def create_game(self, user, houseId, **extra_fields):
        """
        Creates and saves a Game
        """
        Game = self.model(
            houseId = houseId,
            create_user = user.username,
            update_user = user.username
        )
        [setattr(Game, k, v) for k, v in extra_fields.items()]

        Game.save(using=self._db)
        return Game


class Game(MyBaseModel):
    houseId = models.ForeignKey('House', to_field='id', on_delete=models.CASCADE, null=False)
    gameName = models.TextField(blank=True)
    sortNo = models.IntegerField(blank=True, default=0)
    
    objects = GameManager()

    def __str__(self):
        return id

class GameDetailTypeManager(models.Manager):
    def create_gameDetailType(self, user, houseId, **extra_fields):
        """
        Creates and saves a GameDetailType
        """
        GameDetailType = self.model(
            houseId = houseId,
            create_user = user.username,
            update_user = user.username
        )
        [setattr(GameDetailType, k, v) for k, v in extra_fields.items()]

        GameDetailType.save(using=self._db)
        return GameDetailType


class GameDetailType(MyBaseModel):
    houseId = models.ForeignKey('House', to_field='id', on_delete=models.CASCADE, null=False)
    gameId = models.ForeignKey('Game', to_field='id', on_delete=models.CASCADE, null=False)
    gameDetailTypeName = models.TextField(blank=True)
    leftName = models.TextField(blank=True)
    rightName = models.TextField(blank=True)
    sortNo = models.IntegerField(blank=True, default=0)
    
    objects = GameDetailTypeManager()

    def __str__(self):
        return id

class HouseMateFeelingManager(models.Manager):
    def create_housemateFeeling(self, user, houseId, userId, **extra_fields):
        """
        Creates and saves a HouseMateFeeling
        """
        housemateFeeling = self.model(
            houseId = houseId,
            userId = userId,
            create_user = user.username,
            update_user = user.username
        )
        [setattr(housemateFeeling, k, v) for k, v in extra_fields.items()]

        housemateFeeling.save(using=self._db)
        return housemateFeeling


class HouseMateFeeling(MyBaseModel):
    houseId = models.ForeignKey('House', to_field='id', on_delete=models.CASCADE, null=False)
    userId = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, null=False)
    gameId = models.ForeignKey('Game', to_field='id', on_delete=models.CASCADE, null=False)
    gameDetailTypeId = models.ForeignKey('GameDetailType', to_field='id', on_delete=models.CASCADE, null=True)
    choice = models.IntegerField(default=0)
    

    objects = HouseMateFeelingManager()

    def __str__(self):
        return id