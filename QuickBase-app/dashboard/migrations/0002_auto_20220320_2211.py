# Generated by Django 3.1.2 on 2022-03-20 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historical_yesterday_Id',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('historical_id', models.IntegerField()),
                ('date', models.FloatField()),
                ('exchange', models.CharField(choices=[('FTX', 'FTX'), ('BIN', 'Binance')], default='FTX', max_length=3)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='HistoricalIesterdayId',
        ),
    ]
