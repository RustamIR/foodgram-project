# Generated by Django 2.2.6 on 2021-03-18 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20210319_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='dimension',
            field=models.CharField(max_length=50, verbose_name='Eдиница измерения'),
        ),
    ]