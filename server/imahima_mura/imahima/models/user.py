from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.utils import timezone
import uuid
from .mixin import MyBaseModel
from .master import StatusMaster

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        id = str(uuid.uuid4())[:8]
        user = self.model(
            id = id,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given name and password.
        """
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    def update_user(self, user, instance, **extra_fields):
        """
        ユーザ情報更新
        """
        [setattr(instance, k, v) for k, v in extra_fields.items()]
        instance.save(using=self._db)
        return instance
    
    


class User(AbstractBaseUser):
    id = models.TextField(primary_key=True, unique=True, blank=True)
    username = models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=False,
        blank=True,
        null=True
    )

    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class UserSettingManager(models.Manager):
    def create_usersetting(self, user, userId, **extra_fields):
        """
        Creates and saves a UserSetting
        """
        print('UserSettingManager userId')
        print(userId)
        print(user.username)
        # userId = '68f047ff'
        usersetting = self.model(
            userId = userId,
            create_user = user.username,
            update_user = user.username
        )

        usersetting.save(using=self._db)
        return usersetting


    def update_usersetting(self, user, instance, **extra_fields):
        """
        update and saves a UserSetting
        """
        [setattr(instance, k, v) for k, v in extra_fields.items()]
        instance.update_user = user.username
        instance.save(using=self._db)
        return instance


class UserSetting(MyBaseModel):
    userId = models.ForeignKey('User', to_field='id', related_name='userSetting', on_delete=models.CASCADE, null=False, unique=True)
    icon = models.TextField(null=True,editable=True)
    statusId = models.ForeignKey('StatusMaster', to_field='id', on_delete=models.PROTECT, default=StatusMaster.objects.get(statusName = 'ヒマ').id ,null=False)
    statusValidDateTime = models.DateTimeField(null=True, default=timezone.now)
    isAllCategorySelected = models.BooleanField(default=True)
    noticableMonTimeStart = models.TimeField(null=True, default='00:00')
    noticableMonTimeEnd = models.TimeField(null=True, default='00:00')
    noticableTueTimeStart = models.TimeField(null=True, default='00:00')
    noticableTueTimeEnd = models.TimeField(null=True, default='00:00')
    noticableWedTimeStart = models.TimeField(null=True, default='00:00')
    noticableWedTimeEnd = models.TimeField(null=True, default='00:00')
    noticableThuTimeStart = models.TimeField(null=True, default='00:00')
    noticableThuTimeEnd = models.TimeField(null=True, default='00:00')
    noticableFriTimeStart = models.TimeField(null=True, default='00:00')
    noticableFriTimeEnd = models.TimeField(null=True, default='00:00')
    noticableSatTimeStart = models.TimeField(null=True, default='00:00')
    noticableSatTimeEnd = models.TimeField(null=True, default='00:00')
    noticableSunTimeStart = models.TimeField(null=True, default='00:00')
    noticableSunTimeEnd = models.TimeField(null=True, default='00:00')

    objects = UserSettingManager()

    def __str__(self):
        return self.id



class UserSelectCategoryManager(models.Manager):
    def create_userselectcategory(self, user, **extra_fields):
        """
        Creates and saves a UserSelectCategory
        """
        existed = UserSelectCategory.objects.filter(userId=extra_fields.get('userId'),categoryId=extra_fields.get('categoryId')).first()
        if existed:
            return existed

        userselectcategory = self.model(
            create_user = user.username,
            update_user = user.username
        )
        [setattr(userselectcategory, k, v) for k, v in extra_fields.items()]

        userselectcategory.save(using=self._db)
        return userselectcategory


class UserSelectCategory(MyBaseModel):
    userId = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, null=False)
    categoryId = models.ForeignKey('CategoryMaster', to_field='id', on_delete=models.CASCADE, null=False)

    objects = UserSelectCategoryManager()

    def __str__(self):
        return self.id