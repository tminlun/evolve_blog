# Generated by Django 2.0 on 2019-01-10 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190110_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nick_name',
            field=models.CharField(blank=True, default='', max_length=15, null=True, verbose_name='昵称'),
        ),
    ]
