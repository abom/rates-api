# Generated by Django 3.2.6 on 2021-08-22 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddIndex(
            model_name='apikey',
            index=models.Index(fields=['key'], name='app_apikey_key_d1566d_idx'),
        ),
    ]