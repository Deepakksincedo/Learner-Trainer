# Generated by Django 3.2.19 on 2023-06-04 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lxpapp', '0005_auto_20230604_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learnerdetails',
            name='profile_pic',
        ),
    ]