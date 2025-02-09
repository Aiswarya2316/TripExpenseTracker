# Generated by Django 5.0.1 on 2025-02-06 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='adminregister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.TextField()),
                ('phone', models.IntegerField()),
                ('password', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='userregister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.TextField()),
                ('phone', models.IntegerField()),
                ('password', models.TextField()),
                ('location', models.TextField()),
                ('confirm_password', models.TextField()),
            ],
        ),
    ]
