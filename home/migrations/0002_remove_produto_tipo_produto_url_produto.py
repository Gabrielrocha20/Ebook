# Generated by Django 4.1.2 on 2022-10-18 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='tipo',
        ),
        migrations.AddField(
            model_name='produto',
            name='url_produto',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]