# Generated by Django 4.1.6 on 2024-11-10 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.TextField()),
                ('first_name', models.TextField()),
                ('st_no', models.IntegerField()),
                ('st_name', models.TextField()),
                ('apt_no', models.TextField()),
                ('zip_code', models.IntegerField()),
                ('dof_b', models.DateField()),
                ('dof_reg', models.DateField()),
                ('party_aff', models.TextField()),
                ('precinct_no', models.IntegerField()),
                ('v20state', models.BooleanField()),
                ('v21town', models.BooleanField()),
                ('v21primary', models.BooleanField()),
                ('v22general', models.BooleanField()),
                ('v23town', models.BooleanField()),
                ('voter_score', models.IntegerField()),
            ],
        ),
    ]