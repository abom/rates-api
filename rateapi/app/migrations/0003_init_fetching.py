from django.db import migrations


def forwards(apps, schema_editor):
    from rateapi.app.helpers import fetch_and_save_rate

    fetch_and_save_rate()


class Migration(migrations.Migration):

    dependencies = [("app", "0001_initial"), ("app", "0002_auto_20210822_0238")]

    operations = [
        migrations.RunPython(forwards, hints={"target_db": "default"}),
    ]

