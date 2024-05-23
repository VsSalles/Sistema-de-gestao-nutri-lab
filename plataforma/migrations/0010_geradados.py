# Generated by Django 4.1.7 on 2024-04-30 02:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plataforma', '0009_alter_dadospaciente_taxa_metabolismo_basal'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeraDados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limite', models.IntegerField(default=160)),
                ('nutri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]