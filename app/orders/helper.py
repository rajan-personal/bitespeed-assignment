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
    primary_order = check_if_primary_order_exists(email, phoneNumber)
    if primary_order:
        serializer.validated_data['linkPrecedence'] = LinkPrecedence.SECONDARY
        serializer.validated_data['linkedId'] = primary_order.id
    return serializer
    
def check_if_primary_order_exists(email, phoneNumber):
    primary_order_email = Order.objects.filter(linkPrecedence=LinkPrecedence.PRIMARY).filter(Q(email=email) & Q(email__isnull=False)).exclude(deletedAt__isnull=False).order_by('createdAt').first()
    primary_order_phoneNumber = Order.objects.filter(linkPrecedence=LinkPrecedence.PRIMARY).filter(Q(phoneNumber=phoneNumber) & Q(phoneNumber__isnull=False)).exclude(deletedAt__isnull=False).order_by('createdAt').first()
    if primary_order_email and primary_order_phoneNumber:
        if primary_order_email.id != primary_order_phoneNumber.id:
            primary_order = primary_order_email
            secondary_order = primary_order_phoneNumber
            if primary_order_phoneNumber.createdAt < primary_order_email.createdAt:
                primary_order = primary_order_phoneNumber
                secondary_order = primary_order_email

            secondary_order.linkPrecedence = LinkPrecedence.SECONDARY
            secondary_order.linkedId = primary_order.id
            secondary_order.save()
            Order.objects.filter(linkedId=secondary_order.id).update(linkedId=primary_order.id)
            return primary_order
    elif primary_order_email:
        return primary_order_email
    elif primary_order_phoneNumber:
        return primary_order_phoneNumber
    


    