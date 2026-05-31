from django.db.models.signals import post_save
from django.dispatch import receiver
from acounts.models import Acount
from orders.tasks import send_welcome_email


@receiver(post_save, sender=Acount)
def user_registered_signal(sender, instance, created, **kwargs):
    if created:
        send_welcome_email.delay(instance.id)



