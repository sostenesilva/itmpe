# Generated by Django 4.2.13 on 2024-06-09 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('avaliacao', '0008_alter_db_avaliacao_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email_group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_group', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
    ]