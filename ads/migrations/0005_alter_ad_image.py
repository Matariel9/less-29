# Generated by Django 4.1.4 on 2023-01-12 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_alter_category_options_alter_location_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]