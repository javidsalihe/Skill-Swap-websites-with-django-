print("🔥 users.signals LOADED")

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from users.models.address import Address
from api.services.geocoding import postal_to_latlng

@receiver(post_save, sender=Address)
def address_post_save(sender, instance, created, **kwargs):

    if not instance.postal_code:
        return

    if instance.latitude is not None and instance.longitude is not None:
        return

    def geocode():
        lat, lng = postal_to_latlng(instance.postal_code)
        if lat is not None and lng is not None:
            Address.objects.filter(id=instance.id).update(
                latitude=lat,
                longitude=lng
            )

    transaction.on_commit(geocode)
