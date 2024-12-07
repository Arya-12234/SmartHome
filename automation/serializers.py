from rest_framework import serializers
from .models import PricingPlan, Payment

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlan
        fields = ['id', 'name', 'description', 'price']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'plan', 'phone_number', 'amount', 'status', 'transaction_id', 'created_at', 'updated_at']
        read_only_fields = ['status', 'transaction_id', 'created_at', 'updated_at']

from .models import ChatHistory

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = '__all__'