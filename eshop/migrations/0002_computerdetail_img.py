# Generated by Django 4.2.2 on 2023-07-08 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='computerdetail',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='pics'),
        ),
    ]