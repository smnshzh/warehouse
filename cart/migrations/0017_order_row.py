# Generated by Django 3.0.5 on 2020-05-23 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_order_settlement'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='row',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
