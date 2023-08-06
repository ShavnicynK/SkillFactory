from celery import shared_task

from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category, PostCategory


@shared_task
def weekly_send_posts():
    week_interval = timezone.now() - timedelta(days=7)
    categorys = Category.objects.all()
    for cat in categorys:
        posts = Post.objects.filter(categorys=cat.id, date__gte=week_interval)
        if len(cat.subscribers.all()) > 0 and len(posts) > 0:
            subscribers = []
            subscribers += [sub.email for sub in cat.subscribers.all()]
            html_content = render_to_string(
                'mail/mail_weekly_posts.html',
                {
                    'posts': posts,
                    'cat': cat,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Новинки за неделю в категории "{cat.name}"',
                body='',
                from_email='shavnicyn.work@yandex.ru',
                to=subscribers,
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


@shared_task
def notify_users_post(oid):
    post = Post.objects.get(pk=oid)
    for cat in post.categorys.all():
        if len(cat.subscribers.all()) > 0:
            for sub in cat.subscribers.all():
                html_content = render_to_string(
                    'mail/mail_newpost.html',
                    {
                        'post': post,
                        'username': sub.username,
                        'cat_name': cat.name,
                        'link': f'http://127.0.0.1:8000/news/{post.id}'
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'Новый материал "{post.name}" в категории "{cat.name}"',
                    body=post.content,
                    from_email='shavnicyn.work@yandex.ru',
                    to=[sub.email],
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
