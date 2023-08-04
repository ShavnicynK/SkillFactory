from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post


@receiver(m2m_changed, sender=Post.categorys.through)
def notify_users_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.categorys.all():
            if len(cat.subscribers.all()) > 0:
                for sub in cat.subscribers.all():
                    html_content = render_to_string(
                        'mail/mail_newpost.html',
                        {
                            'post': instance,
                            'username': sub.username,
                            'cat_name': cat.name,
                            'link': f'http://127.0.0.1:8000/news/{instance.id}'
                        }
                    )

                    msg = EmailMultiAlternatives(
                        subject=f'Новый материал "{instance.name}" в категории "{cat.name}"',
                        body=instance.content,
                        from_email='shavnicyn.work@yandex.ru',
                        to=[sub.email],
                    )
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()



