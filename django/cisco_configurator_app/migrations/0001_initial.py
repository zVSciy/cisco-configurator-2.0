# Generated by Django 5.0.2 on 2024-03-12 13:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Router_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Router_Interfaces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port_name', models.CharField(max_length=100)),
                ('router', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cisco_configurator_app.router_model')),
            ],
        ),
    ]
