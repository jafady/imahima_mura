from django.db import models
from .mixin import MyBaseModel

class StatusMasterManager(models.Manager):
    def create_statusmaster(self, user, statusName, **extra_fields):
        """
        Creates and saves a StatusMaster
        """
        statusmaster = self.model(
            statusName = statusName,
            create_user = user.username,
            update_user = user.username
        )

        statusmaster.save(using=self._db)
        return statusmaster


class StatusMaster(MyBaseModel):
    statusName = models.TextField(unique=True, null=False)

    objects = StatusMasterManager()

    def __str__(self):
        return self.statusName



class CategoryMasterManager(models.Manager):
    def create_categorymaster(self, user, categoryName, **extra_fields):
        """
        Creates and saves a CategoryMaster
        """
        categorymaster = self.model(
            categoryName = categoryName,
            create_user = user.username,
            update_user = user.username
        )

        categorymaster.save(using=self._db)
        return categorymaster


class CategoryMaster(MyBaseModel):
    categoryName = models.TextField(unique=True, null=False)

    objects = CategoryMasterManager()

    def __str__(self):
        return self.categoryName
