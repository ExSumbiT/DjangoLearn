from django.conf import settings
from ClanApp.models import Members


class DatabaseAppsRouter(object):
    """
    A router to control all database operations on models for different
    databases.

    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.

    Settings example:

    DATABASE_APPS_MAPPING = {'model_name1': 'db1', 'model_name2': 'db2'}

    """
    route_app_labels = {'other'}

    def db_for_read(self, model, **hints):
        """Point all read operations to the specific database."""
        if model == Members:
            return 'other'
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        if model == Members:
            return 'other'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Have no opinion on whether the relation should be allowed."""
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):  # if using Django version 1.8
        """Have no opinion on whether migration operation is allowed to run. """
        if app_label in self.route_app_labels:
            return db == 'other'
        return None
