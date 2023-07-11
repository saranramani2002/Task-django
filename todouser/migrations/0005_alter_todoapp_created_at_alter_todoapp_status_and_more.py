# Generated by Django 4.2.2 on 2023-07-11 10:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todouser', '0004_alter_todoapp_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoapp',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='todoapp',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='todoapp',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]