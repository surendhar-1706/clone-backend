# Generated by Django 3.2.8 on 2021-11-19 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20211031_2224'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
        ),
    ]