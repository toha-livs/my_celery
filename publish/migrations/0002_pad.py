# Generated by Django 2.1.4 on 2019-01-24 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('price', models.IntegerField()),
                ('locate', models.CharField(max_length=40)),
                ('date', models.DateTimeField()),
            ],
        ),
    ]