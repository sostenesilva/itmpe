# Generated by Django 4.2.13 on 2024-06-08 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avaliacao', '0007_remove_db_criterios_responsavel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_avaliacao',
            name='status',
            field=models.CharField(choices=[('Pendente', 'Pendente'), ('Em análise', 'Em análise'), ('Publicado', 'Publicado')], default=('Pendente', 'Pendente'), max_length=20),
        ),
    ]
