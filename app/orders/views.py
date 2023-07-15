from .models import Order, LinkPrecedence
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .helper import populate_choices, populate_choice, pre_serialize,  presave_order
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

        id = serializers.IntegerField(read_only=True)
        phoneNumber = serializers.CharField(max_length=20, required=False)
        email = serializers.CharField(max_length=50, required=False)
        linkedId = serializers.IntegerField(required=False, read_only=True)
        linkPrecedence = serializers.IntegerField(required=False, read_only=True)


class OrderList(APIView):
    def get(self, request, format=None):
        orders = Order.objects.all()
        data = OrderSerializer(orders, many=True).data
        orders = populate_choices(data)
        return Response(orders)
    
    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        serializer, error = pre_serialize(serializer)
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer = presave_order(serializer)
            serializer.save()
            return Response(populate_choice(serializer.data), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

