from rest_framework import serializers

class BudgetSerializer(serializers.Serializer):
    code                = serializers.CharField(max_length=8)
    name                = serializers.CharField(max_length=2000)
    startdate           = serializers.DateTimeField()
    enddate             = serializers.DateTimeField()
    status              = serializers.CharField(max_length=7)
    budgettype          = serializers.CharField(max_length=2)

class PPO_Serializer(serializers.Serializer):
    code                = serializers.CharField(max_length=8)
    name                = serializers.CharField(max_length=2000)
    budgetname          = serializers.CharField(max_length=254)
    startdate           = serializers.DateTimeField()
    enddate             = serializers.DateTimeField()