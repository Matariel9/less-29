# Generated by Django 4.1.4 on 2023-01-19 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0007_alter_user_options_alter_ad_is_published_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='location_id',
        ),
        migrations.AddField(
            model_name='user',
            name='location_id',
            field=models.ManyToManyField(to='ads.location'),
        ),
    ]
