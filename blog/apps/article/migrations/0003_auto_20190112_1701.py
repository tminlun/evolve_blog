# Generated by Django 2.0 on 2019-01-12 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_readnumdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readnumdate',
            name='read_blog',
        ),
        migrations.DeleteModel(
            name='ReadNumDate',
        ),
    ]