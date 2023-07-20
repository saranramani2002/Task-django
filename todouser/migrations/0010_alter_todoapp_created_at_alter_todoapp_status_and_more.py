# Generated by Django 4.2.2 on 2023-07-18 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todouser', '0009_alter_todoapp_status_alter_todoapp_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoapp',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='todoapp',
            name='status',
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('In Progress', 'In Progress'), ('Not Completed', 'Not Completed')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='todoapp',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
