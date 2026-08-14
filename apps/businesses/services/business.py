from apps.businesses.models import Business


def create_business(**data):
    return Business.objects.create(**data)


def update_business(business, **data):
    for field, value in data.items():
        setattr(business, field, value)

    business.save()
    return business
