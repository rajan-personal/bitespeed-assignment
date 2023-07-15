from .models import LinkPrecedence, Order
from django.db.models import Q

def populate_choices(data):
    for d in data:
        d['linkPrecedence'] = LinkPrecedence(d['linkPrecedence']).name
    return data

def populate_choice(d):
    d['linkPrecedence'] = LinkPrecedence(d['linkPrecedence']).name
    return d

def pre_serialize(serializer):
    error = None
    serializer.initial_data['linkPrecedence'] = LinkPrecedence.PRIMARY
    serializer.initial_data['linkedId'] = None
    serializer.initial_data['deletedAt'] = None
    email = serializer.initial_data.get('email')
    phoneNumber = serializer.initial_data.get('phoneNumber')
    if not email and not phoneNumber:
        error = ['email or phoneNumber is required']
    return serializer, error

def presave_order(serializer):
    email = serializer.validated_data.get('email')
    phoneNumber = serializer.validated_data.get('phoneNumber')
    primary_order = validate_user(email, phoneNumber)
    if primary_order:
        serializer.validated_data['linkPrecedence'] = LinkPrecedence.SECONDARY
        serializer.validated_data['linkedId'] = primary_order.id
    return serializer

def validate_user(email, phoneNumber):
    primary_order = Order.objects.filter(linkPrecedence=LinkPrecedence.PRIMARY).filter((Q(email=email) & (Q(email__isnull=False)) | Q(phoneNumber=phoneNumber) & Q(phoneNumber__isnull=False))).exclude(deletedAt__isnull=False).order_by('createdAt').first()
    if primary_order:
        return primary_order



    