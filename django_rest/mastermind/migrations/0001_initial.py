# Generated by Django 3.1.3 on 2022-11-27 12:20

from django.db import migrations, models
import django.db.models.deletion
import mastermind.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.CharField(default=mastermind.models.Game.create_sequence, max_length=4)),
                ('guess_limit', models.IntegerField()),
                ('status', models.CharField(default='off', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.CharField(max_length=4)),
                ('black_pegs', models.IntegerField(default=0)),
                ('white_pegs', models.IntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mastermind.game')),
            ],
        ),
    ]
