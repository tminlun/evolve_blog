# Generated by Django 2.0 on 2019-01-19 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0007_auto_20190118_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecomments',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='operation.CourseComments', verbose_name='上一级评论'),
        ),
    ]