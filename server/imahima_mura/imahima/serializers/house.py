from ..models import House,HouseMate

from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    """ A serializer class for the House model """
    class Meta:
        model = House
        fields = ('id', 'houseName')
        # fields = ('houseName')
    
    def create(self, validated_data):
        return House.objects.create_house(self.context["request"].user, **validated_data)


class HouseMateSerializer(serializers.ModelSerializer):
    """ A serializer class for the HouseMate model """
    house = HouseSerializer(source = 'houseId',required=False)
    class Meta:
        model = HouseMate
        fields = ('id', 'houseId', 'userId', 'isApproved', 'house')
    
    def create(self, validated_data):
        return HouseMate.objects.create_housemate(self.context["request"].user, **validated_data)
    