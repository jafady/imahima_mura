from ..models import StatusMaster,CategoryMaster

from rest_framework import serializers


class StatusMasterSerializer(serializers.ModelSerializer):
    """ A serializer class for the StatusMaster model """
    class Meta:
        model = StatusMaster
        fields = ('id', 'statusName')
    
    def create(self, validated_data):
        return StatusMaster.objects.create_statusmaster(self.context["request"].user, **validated_data)


class CategoryMasterSerializer(serializers.ModelSerializer):
    """ A serializer class for the CategoryMaster model """
    class Meta:
        model = CategoryMaster
        fields = ('id', 'categoryName')
    
    def create(self, validated_data):
        return CategoryMaster.objects.create_categorymaster(self.context["request"].user, **validated_data)
