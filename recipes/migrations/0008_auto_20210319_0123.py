# Generated by Django 2.2.6 on 2021-03-18 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20210301_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='dimension',
            field=models.PositiveSmallIntegerField(max_length=50, verbose_name='Eдиница измерения'),
        ),
    ]
