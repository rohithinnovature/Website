# Generated by Django 5.0.6 on 2024-07-03 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_userprofile_id_alter_userprofile_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='date_of_birth',
            new_name='date_of_birt',
        ),
    ]
