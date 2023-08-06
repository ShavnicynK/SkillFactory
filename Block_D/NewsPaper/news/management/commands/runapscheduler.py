import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category, PostCategory

logger = logging.getLogger(__name__)


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


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_send_posts,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="weekly_send_posts",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_send_posts'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")