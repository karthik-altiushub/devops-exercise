import sys

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.loader import MigrationLoader


class Command(BaseCommand):
    help = 'Checks unapplied migration files for table locking schema changes for a specific app and database.'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Name of the app to check migrations for.')
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            help=(
                "Nominates a database to show migrations for. Defaults to the "
                '"default" database.'
            ),
        )

    def handle(self, *args, **options):
        app_name = options['app_name']
        db_name = options['database']

        # Validate app name
        try:
            apps.get_app_config(app_name)
        except LookupError as err:
            self.stderr.write(str(err))
            sys.exit(1)

        # Validate database name
        if db_name not in connections:
            self.stderr.write(f"Unknown database: {db_name}")
            sys.exit(1)

        connection = connections[db_name]

        # Load migrations
        loader = MigrationLoader(connection, ignore_no_migrations=True)
        graph = loader.graph

        print(f"Checking migrations for app '{app_name}' in database '{db_name}'...")

        for node in graph.leaf_nodes(app_name):
            for plan_node in graph.forwards_plan(node):
                if plan_node[0] == app_name:
                    migration = loader.get_migration(plan_node[0], plan_node[1])

                    # Check if migration is applied
                    if plan_node not in loader.applied_migrations:
                        for operation in migration.operations:
                            if self._is_table_locking(operation):
                                error_message = (
                                    f"ERROR: Table locking schema change found in "
                                    f"{plan_node[0]}.{plan_node[1]}: {operation.__class__.__name__}"
                                )
                                self.stdout.write(self.style.ERROR(error_message))
                                sys.exit(0)

        self.stdout.write(self.style.SUCCESS("No table locking schema changes found."))

    def _is_table_locking(self, operation):
        """
        Check if the given operation can cause table locking.
        """
        if operation.__class__.__name__ == 'AddField':
            # Ignore AddField operations where null=True
            return not getattr(operation.field, 'null', False)

        if operation.__class__.__name__ in {'RemoveField', 'RenameField'}:
            return True

        if operation.__class__.__name__ == 'AlterField':
            # Check if changing column type or adding a non-null default value
            if getattr(operation, 'field', None):
                if operation.field.__class__.__name__ in ['IntegerField', 'BigIntegerField', 'FloatField', 'DecimalField']:
                    return True
                if operation.field.default is not None and not operation.field.null:
                    return True

        return False
