# Generated by Django 5.1.2 on 2025-02-07 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_userprofile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
