# Generated by Django 3.0.5 on 2020-05-19 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountside', '0008_documentnumber_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentnumber',
            name='editable',
            field=models.BooleanField(default=False),
        ),
    ]
