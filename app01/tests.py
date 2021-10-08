from django.test import TestCase

#Createyourtestshere.
import os

if __name__=="__main__":
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django0002.settings')
    import django
    django.setup()
    #-------------------------------------------------------------------------------->>>>
    from app01 import models
    import datetime
    models.Book.objects.create(title='论语',price=1223.54,publish_id=3)
    models.Book.objects.create(title='happy day', price=123.54, publish_id=2)