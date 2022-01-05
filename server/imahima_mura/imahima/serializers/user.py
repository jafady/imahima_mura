from ..models import User,UserSetting,UserSelectCategory

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ A serializer class for the User model """
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'is_admin', 'is_active', 'is_superuser')
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserSetting.objects.create_usersetting(self.context["request"].user, userId=user)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    """ A serializer class for the User model """
    class Meta:
        model = User
        fields = ('id', 'username')
    
    def update(self, instance, validated_data):
        return User.objects.update_user(self.context["request"].user, instance, **validated_data)



class UserSettingSerializer(serializers.ModelSerializer):
    """ A serializer class for the UserSetting model """
    class Meta:
        model = UserSetting
        fields = ('id', 'userId', 'icon', 'statusId',
                  'isAllCategorySelected', 'noticableTimeStart', 'noticableTimeEnd',
                  'canNoticeMon','canNoticeTue','canNoticeWed','canNoticeThu','canNoticeFri','canNoticeSat','canNoticeSun'
                  )
    
    def create(self, validated_data):
        return UserSetting.objects.create_usersetting(self.context["request"].user, **validated_data)

    def update(self, instance, validated_data):
        return UserSetting.objects.update_usersetting(self.context["request"].user, instance, **validated_data)


class UserSelectCategorySerializer(serializers.ModelSerializer):
    """ A serializer class for the UserSelectCategory model """
    class Meta:
        model = UserSelectCategory
        fields = ('id', 'userId', 'categoryId')
    
    def create(self, validated_data):
        return UserSelectCategory.objects.create_userselectcategory(self.context["request"].user, **validated_data)