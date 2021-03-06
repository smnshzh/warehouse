# Generated by Django 3.0.5 on 2020-05-11 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='kind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_code', models.PositiveIntegerField(verbose_name='Code')),
                ('type_name', models.CharField(max_length=12, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='local_id_def',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=12)),
                ('local_name', models.CharField(max_length=12)),
                ('local_code', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='accountside',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('telephonnumber', models.CharField(max_length=11, unique=True)),
                ('address', models.TextField()),
                ('credit', models.PositiveIntegerField()),
                ('property', models.BooleanField(default=False)),
                ('area', models.PositiveSmallIntegerField()),
                ('id_code', models.PositiveSmallIntegerField(unique=True)),
                ('kind', models.ManyToManyField(to='accountside.kind')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accountside.local_id_def')),
            ],
        ),
    ]
