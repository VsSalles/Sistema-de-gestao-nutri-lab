# Generated by Django 4.1.7 on 2024-05-12 01:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0017_alter_cancelamento_data_alter_codigopedido_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consulta',
            name='comprovante_horas',
        ),
        migrations.AlterField(
            model_name='cancelamento',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 11, 22, 47, 58, 89079)),
        ),
        migrations.AlterField(
            model_name='codigopedido',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 11, 22, 47, 58, 87608)),
        ),
    ]
