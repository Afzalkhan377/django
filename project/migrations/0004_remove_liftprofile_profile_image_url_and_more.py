# Generated by Django 5.1.3 on 2024-12-02 19:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_rename_timestamp_friend_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='liftprofile',
            name='profile_image_url',
        ),
        migrations.AddField(
            model_name='liftprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default.jpg', upload_to='profile_pictures/'),
        ),
        migrations.AlterField(
            model_name='liftprofile',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
