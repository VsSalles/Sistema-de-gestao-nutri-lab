# Generated by Django 4.1.7 on 2024-05-12 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0013_remove_geradados_consultas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opcao',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='opcao'),
        ),
    ]
