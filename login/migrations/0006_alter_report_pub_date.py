# Generated by Django 4.2.10 on 2024-04-27 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_report_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
