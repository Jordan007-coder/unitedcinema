# Generated by Django 4.2.1 on 2023-05-18 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_alter_film_date_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='thumb',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]