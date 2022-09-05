# Generated by Django 4.0 on 2022-09-05 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0002_alter_candidate_qualifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('state', models.CharField(max_length=30)),
                ('state_code', models.CharField(max_length=20)),
                ('senatorial_district', models.CharField(max_length=200)),
                ('senatorial_district_code', models.CharField(max_length=100)),
                ('federal_constituency', models.CharField(max_length=200)),
                ('federal_constituency_code', models.CharField(max_length=100)),
                ('state_constituency', models.CharField(max_length=200)),
                ('state_constituency_code', models.CharField(max_length=100)),
                ('lga', models.CharField(max_length=200)),
                ('lga_code', models.CharField(max_length=100)),
                ('ward', models.CharField(max_length=200)),
                ('ward_code', models.CharField(max_length=100)),
                ('polling_unit', models.CharField(max_length=100)),
                ('polling_unit_code', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='federal_constituency',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='federal_constituency_code',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='lga',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='lga_code',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='polling_unit',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='polling_unit_code',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='senatorial_district',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='senatorial_district_code',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='state',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='state_code',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='state_constituency',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='state_constituency_code',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='ward',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='ward_code',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='year',
        ),
        migrations.AddField(
            model_name='candidate',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='candidates.location'),
        ),
    ]
