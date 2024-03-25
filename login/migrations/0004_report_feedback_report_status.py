# Generated by Django 4.2.10 on 2024-03-25 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='feedback',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('NEW', 'New'), ('INP', 'In Progress'), ('RES', 'Resolved')], default='NEW', max_length=3),
        ),
    ]