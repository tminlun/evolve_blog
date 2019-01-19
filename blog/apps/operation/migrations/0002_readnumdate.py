# Generated by Django 2.0 on 2019-01-12 09:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20190112_1701'),
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadNumDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_num', models.IntegerField(default=0, verbose_name='阅读的数量')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='阅读的时间')),
                ('read_blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Blog', verbose_name='阅读的博客')),
            ],
            options={
                'verbose_name': '博客阅读数量',
                'verbose_name_plural': '博客阅读数量',
            },
        ),
    ]
