from django.core.management.base import BaseCommand
from pilotCore.dispatcher import run_pooling


class Command(BaseCommand):
    """
    `python manage.py run_polling`
    Before start make sure WebHook deleted:
    https://api.telegram.org/bot{TOKEN}/deleteWebhook?url=https://domain.ltd/

    And afterwards set WebHook back:
    https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://domain.ltd/
    """

    help = 'Polling mode for pilotCore app'

    def handle(self, *args, **options):
        run_pooling()
