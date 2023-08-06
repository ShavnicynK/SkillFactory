from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from .tasks import notify_users_post


@receiver(m2m_changed, sender=Post.categorys.through)
def new_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        notify_users_post.apply_async([instance.id], countdown=5)




