# Generated by Django 2.0 on 2019-03-27 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190127_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(blank=True, default='banner/default.png', null=True, upload_to='banner/%Y%m', verbose_name='轮播图'),
        ),
    ]
