# Generated by Django 5.0.1 on 2024-02-10 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracking_system', '0012_userproject_created_at_userproject_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproject',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
