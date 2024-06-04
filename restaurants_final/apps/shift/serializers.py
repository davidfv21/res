
from rest_framework import serializers
from .models import WaiterShift

class WaiterShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaiterShift
        fields = ['id', 'waiter', 'start_date', 'end_date', 'restaurant']