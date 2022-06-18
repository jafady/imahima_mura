from ..models import House,HouseMate,InviteHouseToken,Game,GameDetailType,HouseMateFeeling

from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    """ A serializer class for the House model """
    class Meta:
        model = House
        fields = ('id', 'houseName', 'discordUrl', 'discordNoticeUrl')
    
    def create(self, validated_data):
        return House.objects.create_house(self.context["request"].user, **validated_data)
    
    def update(self, instance, validated_data):
        self.readonly_fields = ('id',)
        return House.objects.update_house(self.context["request"].user, instance, **validated_data)


class HouseMateSerializer(serializers.ModelSerializer):
    """ A serializer class for the HouseMate model """
    house = HouseSerializer(source = 'houseId',required=False)
    class Meta:
        model = HouseMate
        fields = ('id', 'houseId', 'userId', 'isApproved', 'house')
    
    def create(self, validated_data):
        return HouseMate.objects.create_housemate(self.context["request"].user, **validated_data)


class InviteHouseTokenSerializer(serializers.ModelSerializer):
    """ A serializer class for the HouseMate model """
    class Meta:
        model = InviteHouseToken
        fields = ('id', 'houseId', 'validDateTime')
    
    def create(self, validated_data):
        return InviteHouseToken.objects.create_inviteHouseToken(self.context["request"].user, **validated_data)

class GameSerializer(serializers.ModelSerializer):
    """ A serializer class for the Game model """
    class Meta:
        model = Game
        fields = ('id', 'houseId', 'gameName', 'sortNo')
    
    def create(self, validated_data):
        return Game.objects.create_game(self.context["request"].user, **validated_data)

class GameDetailTypeSerializer(serializers.ModelSerializer):
    """ A serializer class for the GameDetailType model """
    game = GameSerializer(source = 'gameId',required=False)
    class Meta:
        model = GameDetailType
        fields = ('id', 'houseId', 'gameId', 'gameDetailTypeName', 'leftName', 'rightName', 'sortNo', 'game')
    
    def create(self, validated_data):
        return GameDetailType.objects.create_gameDetailType(self.context["request"].user, **validated_data)

class HouseMateFeelingSerializer(serializers.ModelSerializer):
    """ A serializer class for the HouseMateFeeling model """
    class Meta:
        model = HouseMateFeeling
        fields = ('id', 'houseId', 'userId', 'gameId', 'gameDetailTypeId', 'choice')
    
    def create(self, validated_data):
        obj, created = HouseMateFeeling.objects.update_or_create(
            houseId = validated_data['houseId'], userId = validated_data['userId'],
            gameId = validated_data['gameId'], gameDetailTypeId = validated_data['gameDetailTypeId'],
            defaults = {
                'choice': validated_data['choice'],
                'create_user':self.context["request"].user.username,
                'update_user':self.context["request"].user.username
            }
        )
        return obj
    