# Generated by Django 4.1.7 on 2024-04-23 01:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0008_alter_codigopedido_data_cancelamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelamento',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 22, 22, 26, 28, 143872)),
        ),
        migrations.AlterField(
            model_name='codigopedido',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 22, 22, 26, 28, 143872)),
        ),
    ]