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

class UserPasswordSerializer(serializers.ModelSerializer):
    """ A serializer class for the User model """
    class Meta:
        model = User
        fields = ('id', 'password',
                  'is_admin', 'is_active', 'is_superuser')
    
    def update(self, instance, validated_data):
        user = User.objects.update_password(self.context["request"].user,instance,**validated_data)
        return user

class UserNameSerializer(serializers.ModelSerializer):
    """ A serializer class for the User model """
    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'is_admin', 'is_active', 'is_superuser')

class UserSettingSerializer(serializers.ModelSerializer):
    """ A serializer class for the UserSetting model """
    userId = serializers.CharField(required = False)
    class Meta:
        model = UserSetting
        fields = ('id', 'userId', 'icon', 
                  'statusId', 'statusValidDateTime','isAllCategorySelected', 
                  'noticableMonTimeStart','noticableMonTimeEnd','noticableTueTimeStart','noticableTueTimeEnd',
                  'noticableWedTimeStart','noticableWedTimeEnd','noticableThuTimeStart','noticableThuTimeEnd',
                  'noticableFriTimeStart','noticableFriTimeEnd','noticableSatTimeStart','noticableSatTimeEnd',
                  'noticableSunTimeStart','noticableSunTimeEnd',
                  )
        # read_only_fields = ('id',)
    
    def create(self, validated_data):
        return UserSetting.objects.create_usersetting(self.context["request"].user, **validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
        self.readonly_fields = ('id',)
        return UserSetting.objects.update_usersetting(self.context["request"].user, instance, **validated_data)
    


class UserSelectCategorySerializer(serializers.ModelSerializer):
    """ A serializer class for the UserSelectCategory model """
    class Meta:
        model = UserSelectCategory
        fields = ('id', 'userId', 'categoryId')
    
    def create(self, validated_data):
        return UserSelectCategory.objects.create_userselectcategory(self.context["request"].user, **validated_data)


# 未使用だが、SlugRelatedFieldのサンプル用に残す
# class UserInfoSerializer(serializers.ModelSerializer):
#     """ A serializer class for the User model """
#     userSetting = serializers.SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='icon'
#      )
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'userSetting')
    
#     def update(self, instance, validated_data):
#         return User.objects.update_user(self.context["request"].user, instance, **validated_data)