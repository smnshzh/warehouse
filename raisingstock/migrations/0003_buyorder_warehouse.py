# Generated by Django 3.0.5 on 2020-05-15 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0004_inventory_warehousedefinde'),
        ('raisingstock', '0002_buyorder_items_warehouse'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyorder',
            name='warehouse',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Shop.WareHouseDefinde'),
            preserve_default=False,
        ),
    ]
