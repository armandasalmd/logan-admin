# Generated by Django 2.1.3 on 2019-01-22 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20190122_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminsolditems',
            name='date',
            field=models.CharField(default='2019-01-22 21:52:07', max_length=100),
        ),
    ]