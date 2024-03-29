# Generated by Django 4.2 on 2024-02-19 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0002_overallanalysis_rank_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overallanalysis',
            name='analysisResult',
            field=models.CharField(choices=[('VGOOD', 'verygood'), ('GOOD', 'good'), ('BAD', 'bad'), ('OK', 'ok'), ('NAVL', 'navl')], default='NAVL', max_length=6),
        ),
        migrations.AlterField(
            model_name='overallanalysis',
            name='rank',
            field=models.IntegerField(default=0),
        ),
    ]
