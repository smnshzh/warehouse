# Generated by Django 3.0.5 on 2020-05-16 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountside', '0006_autojoournalfields'),
    ]

    operations = [
        migrations.AddField(
            model_name='autojoournalfields',
            name='name',
            field=models.CharField(default=1, max_length=45),
            preserve_default=False,
        ),
    ]
