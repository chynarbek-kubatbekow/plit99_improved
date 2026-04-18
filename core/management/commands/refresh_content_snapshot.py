from django.core.management.base import BaseCommand

from core.content_snapshot import export_content_snapshot, safe_export_content_snapshot


class Command(BaseCommand):
    help = 'Refresh JSON snapshot files for news and gallery content.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--safe',
            action='store_true',
            help='Log snapshot export errors without failing the command.',
        )

    def handle(self, *args, **options):
        if options['safe']:
            path = safe_export_content_snapshot()
            if path:
                self.stdout.write(self.style.SUCCESS(f'Content snapshot refreshed: {path}'))
            else:
                self.stdout.write('Content snapshot refresh was skipped because export failed.')
            return

        path = export_content_snapshot()
        self.stdout.write(self.style.SUCCESS(f'Content snapshot refreshed: {path}'))
