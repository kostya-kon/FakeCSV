# Generated by Django 3.1.4 on 2020-12-15 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csvgen', '0004_csvfile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvfile',
            old_name='user',
            new_name='schema',
        ),
    ]
