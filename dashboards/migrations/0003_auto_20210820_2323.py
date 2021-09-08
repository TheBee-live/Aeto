# Generated by Django 3.0.4 on 2021-08-21 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0002_auto_20210817_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='Excel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='fecha_de_inflado',
            field=models.DateField(blank=True, null=True),
        ),
    ]
