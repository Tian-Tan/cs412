# Generated by Django 4.1.6 on 2024-11-23 00:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_borrow_due_date_alter_borrow_returned_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 30, 0, 40, 32, 21020, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='returned_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
