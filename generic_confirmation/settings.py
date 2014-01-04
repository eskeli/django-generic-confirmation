from django.conf import settings

EXPIRE_OLD = getattr(settings, 'GENERIC_CONFIRMATION_EXPIRE_OLD', False) # If set to true, makes old confirmations for the same object expire when a new confirmation is added (i.e. only the most recent confirmation is valid)