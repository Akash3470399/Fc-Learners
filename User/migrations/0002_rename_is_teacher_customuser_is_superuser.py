# Generated by Django 4.0 on 2022-01-13 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_teacher',
            new_name='is_superuser',
        ),
    ]