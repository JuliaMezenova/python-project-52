# Generated by Django 4.1.2 on 2024-03-14 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0002_alter_status_name_alter_status_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Имя'),
        ),
    ]