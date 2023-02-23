from customer.models import *
from django.core.exceptions import ObjectDoesNotExist


def enquiry_count(request):
    try:
        enquiry = Contact.objects.filter(status='unread')
    except Contact.ObjectDoesNotExist:
        return {}
    contact_count = enquiry.count()
    return {"contact_count":contact_count}