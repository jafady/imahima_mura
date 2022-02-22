from ..models import Event,EventMembers

from rest_framework import serializers


class EventMembersSerializer(serializers.ModelSerializer):
    """ A serializer class for the EventMembers model """
    class Meta:
        model = EventMembers
        fields = ('id', 'eventId', 'userId')
    
    def create(self, validated_data):
        return EventMembers.objects.create_eventmembers(self.context["request"].user, **validated_data)


class EventSerializer(serializers.ModelSerializer):
    """ A serializer class for the Event model """
    class Meta:
        model = Event
        fields = ('id', 'houseId', 'eventName', 'recruitmentNumbersLower', 'recruitmentNumbersUpper',
                'location', 'startDate', 'startTime', 'endTime', 'categoryId', 'detail')
    
    def create(self, validated_data):
        event = Event.objects.create_event(self.context["request"].user, **validated_data)
        print(event.id)
        EventMembers.objects.create_eventmembers(self.context["request"].user, eventId = event, userId = self.context["request"].user)
        return event
    
    def update(self, instance, validated_data):
        self.readonly_fields = ('id',)
        return Event.objects.update_event(self.context["request"].user, instance, **validated_data)