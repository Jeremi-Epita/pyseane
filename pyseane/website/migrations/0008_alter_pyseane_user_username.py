# Generated by Django 4.2.7 on 2023-11-25 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_pyseane_user_first_name_pyseane_user_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pyseane_user',
            name='username',
            field=models.CharField(max_length=30),
        ),
    ]