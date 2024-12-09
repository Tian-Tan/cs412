# Generated by Django 4.1.6 on 2024-11-23 00:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_borrows_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout_date', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateTimeField(default=datetime.datetime(2024, 11, 30, 0, 36, 56, 23970, tzinfo=datetime.timezone.utc))),
                ('returned_date', models.DateTimeField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.book')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.profile')),
            ],
        ),
        migrations.DeleteModel(
            name='Borrows',
        ),
    ]