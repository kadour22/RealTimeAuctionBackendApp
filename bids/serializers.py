from rest_framework import serializers
from .models import Bidding
from .validations.amount_validation import validate_amount

class bidding_serializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Bidding
        fields = ['id', 'auction', 'user', 'amount', 'created_at']
        read_only_fields = ['user']
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username
        }

    def validate(self,attrs) :
        amount = attrs["amount"]
        return validate_amount(amount=amount)
    