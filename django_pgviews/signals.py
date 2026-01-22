from django.dispatch import Signal


# Note: providing_args was removed in Django 4.0
# The signal sends: update, force, status, has_changed
view_synced = Signal()
all_views_synced = Signal()
