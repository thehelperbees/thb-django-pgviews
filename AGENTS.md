# thb-django-pgviews

THB fork of [mypebble/django-pgviews](https://github.com/mypebble/django-pgviews) (v0.5.7). Provides Django ORM support for PostgreSQL views and materialized views.

## Why We Forked

The upstream library uses the default database connection for all view operations. THB's fork adds **database routing** (`router.db_for_write()`) so views are created/synced on the correct database in multi-database setups. Also adds `PGVIEWS_DISABLE_AUTO_SYNC` setting and a Django 3.0 compatibility fix (`six` as standalone dep).

## THB-Specific Changes (vs upstream)

- **Database routing**: `models.py` and `clear_pgviews.py` use `router.db_for_write()` instead of the default connection
- **`PGVIEWS_DISABLE_AUTO_SYNC`**: Django setting (in `apps.py`) to skip automatic view sync after migrations
- **Django 3.0 fix**: `import six` as standalone package (removed from `django.utils` in Django 3.0)

## Which Apps Use This

Installed via `pip install` from this GitHub repo (not PyPI). Any THB Django app that defines PostgreSQL views or materialized views as Django models. Check consuming repos for `django_pgviews` in `INSTALLED_APPS` or `requirements.txt`.

## Key Files

- `django_pgviews/view.py` -- Core: View, MaterializedView, ReadOnlyView base classes
- `django_pgviews/models.py` -- ViewSyncer (creates/updates views with dependency ordering)
- `django_pgviews/apps.py` -- Post-migrate hook (auto-syncs views unless disabled)
- `django_pgviews/management/commands/` -- `sync_pgviews` and `clear_pgviews` commands

## Development

```bash
# Sync views manually
python manage.py sync_pgviews
python manage.py sync_pgviews --force  # force-update incompatible schemas

# Clear all views (run before migrations that alter view dependencies)
python manage.py clear_pgviews

# Run tests (requires PostgreSQL)
tox
```

## Notes

- **Low activity** (~1 commit per quarter). Sole THB contributor: AJ Botello.
- **CI**: CircleCI with tox (Python 3.6-3.8, Django 2.0-3.1).
- **Django compat**: Tested up to Django 3.1. Upstream README references Django 1.x-era patterns.
- Uses `psycopg2` directly for view DDL (not Django migrations -- views are `managed = False`).
