# Generated by Django 4.2.13 on 2024-06-07 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('avaliacao', '0004_db_avaliacao_log_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_criterios',
            name='responsavel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.group'),
        ),
    ]
