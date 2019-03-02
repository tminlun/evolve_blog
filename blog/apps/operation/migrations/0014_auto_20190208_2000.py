# Generated by Django 2.0 on 2019-02-08 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0013_auto_20190128_0949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='photh_type',
        ),
        migrations.AddField(
            model_name='photo',
            name='photo_type',
            field=models.CharField(blank=True, max_length=20, verbose_name='图片类型'),
        ),
        migrations.DeleteModel(
            name='PhotoType',
        ),
    ]