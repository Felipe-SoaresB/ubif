# Generated by Django 4.1 on 2025-02-15 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0002_remove_ofertacarona_vagas_remove_veiculo_capacidade_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ofertacarona',
            name='veiculo',
        ),
        migrations.DeleteModel(
            name='Veiculo',
        ),
    ]
