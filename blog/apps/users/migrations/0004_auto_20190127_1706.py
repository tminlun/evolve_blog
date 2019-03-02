# Generated by Django 2.0 on 2019-01-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190110_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='访问地址'),
        ),
    ]