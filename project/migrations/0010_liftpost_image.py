# Generated by Django 5.1.3 on 2024-12-02 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_delete_friendrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='liftpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
