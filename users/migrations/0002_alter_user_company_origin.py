# Generated by Django 4.1.1 on 2022-12-19 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company_origin',
            field=models.CharField(choices=[('0', 'Iranian'), ('1', 'Foreign')], default='0', max_length=1),
        ),
    ]