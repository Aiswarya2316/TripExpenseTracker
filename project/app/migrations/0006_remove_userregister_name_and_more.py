# Generated by Django 5.0.1 on 2025-02-06 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_userregister_user_alter_expensegroup_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregister',
            name='name',
        ),
        migrations.RemoveField(
            model_name='userregister',
            name='password',
        ),
        migrations.AlterField(
            model_name='userregister',
            name='confirm_password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='userregister',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='userregister',
            name='location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userregister',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
