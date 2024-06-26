# Generated by Django 4.1.7 on 2024-04-22 17:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0007_alter_codigopedido_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codigopedido',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 22, 14, 36, 26, 751192)),
        ),
        migrations.CreateModel(
            name='Cancelamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(choices=[('E', 'Emergencia'), ('I', 'imprevisto'), ('O', 'Outro')], max_length=1)),
                ('detalhes', models.TextField(blank=True, null=True)),
                ('data', models.DateTimeField(default=datetime.datetime(2024, 4, 22, 14, 36, 26, 757330))),
                ('consulta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='consultas.consulta')),
            ],
        ),
    ]
