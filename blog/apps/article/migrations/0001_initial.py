# Generated by Django 2.0 on 2019-04-12 21:36

import DjangoUeditor.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='标题')),
                ('describe', models.CharField(blank=True, max_length=100, null=True, verbose_name='描述')),
                ('detail', DjangoUeditor.models.UEditorField(default='', verbose_name='课程内容')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/%Y%m', verbose_name='图片')),
                ('related', models.CharField(blank=True, max_length=20, verbose_name='相关博客')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '博客',
                'verbose_name_plural': '博客',
                'ordering': ['-add_time'],
            },
        ),
        migrations.CreateModel(
            name='BlogType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='类型')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '博客类型',
                'verbose_name_plural': '博客类型',
            },
        ),
        migrations.CreateModel(
            name='CourseResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='资源名')),
                ('download', models.FileField(upload_to='blog/resource/%Y%m', verbose_name='资源文件')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Blog', verbose_name='博客')),
            ],
            options={
                'verbose_name': '博客资源',
                'verbose_name_plural': '博客资源',
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.BlogType', verbose_name='博客类型'),
        ),
    ]
