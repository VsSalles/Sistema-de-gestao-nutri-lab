# Generated by Django 4.1.7 on 2024-04-30 02:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0012_alter_cancelamento_data_alter_codigopedido_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelamento',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 29, 23, 24, 53, 725779)),
        ),
        migrations.AlterField(
            model_name='codigopedido',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 29, 23, 24, 53, 722935)),
        ),
    ]