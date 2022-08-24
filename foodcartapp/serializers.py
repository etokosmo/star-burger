from rest_framework.serializers import ModelSerializer, IntegerField, \
    Serializer

from .models import Order, OrderElements


class OrderDeleteSerializer(Serializer):
    id = IntegerField()

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Order.objects.update(**validated_data)


class OrderUpdateSerializer(ModelSerializer):
    id = IntegerField()

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address']
        extra_kwargs = {
            'firstname': {'required': False},
            'lastname': {'required': False},
            'phonenumber': {'required': False},
            'address': {'required': False},
        }

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Order.objects.update(**validated_data)


class OrderElementsSerializer(ModelSerializer):
    class Meta:
        model = OrderElements
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderElementsSerializer(many=True,
                                       allow_empty=False,
                                       write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address',
                  'products']

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Order.objects.update(**validated_data)
