# Generated by Django 4.2.7 on 2023-11-30 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_alter_campagne_fish_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campagne_fish',
            name='url',
            field=models.CharField(null=True),
        ),
    ]