# Generated by Django 5.0.1 on 2025-02-06 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_userregister_confirm_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregister',
            name='confirm_password',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userregister',
            name='password',
            field=models.TextField(),
        ),
    ]
