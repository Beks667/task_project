from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import CustomUser

import ssl

context = ssl.create_default_context()
from django.core.mail import get_connection


@receiver(post_save, sender=CustomUser)
def send_email(sender, instance, created, **kwargs):
    if created:
        subject = "Подтвердите учетную запись!"
        message = 'Вы зарегистрировались на сайте бла бла бла , Пожалуйста перейдите по ссылке для подтверждения !'
        from_email = 'beksturgunbaev@gmail.com'
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list,
                  connection=get_connection(use_ssl=True, ssl_context=context))
