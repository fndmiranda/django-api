# Generated by Django 3.0.7 on 2020-06-17 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='title')),
                ('slug', models.SlugField(max_length=80, verbose_name='slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('slug', models.SlugField(max_length=80, verbose_name='slug')),
                ('description', models.TextField(verbose_name='description')),
                ('brand', models.CharField(max_length=50, verbose_name='brand')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('ordering', models.IntegerField(db_index=True, default=0, verbose_name='ordering')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('categories', models.ManyToManyField(blank=True, related_name='products', to='catalog.Category', verbose_name='categories')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('ordering',),
            },
        ),
    ]
