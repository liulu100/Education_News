from django.core.management.base import BaseCommand,CommandError
from news.tagimg import create_tag_cloud

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            create_tag_cloud()
        except CommandError:
            print "error"