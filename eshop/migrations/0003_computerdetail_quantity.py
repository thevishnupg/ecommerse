# Generated by Django 4.2.1 on 2023-07-13 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0002_computerdetail_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='computerdetail',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
