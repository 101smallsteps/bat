# Generated by Django 4.2 on 2024-09-02 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0007_rename_grossmargin_ratio_cashratio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overallanalysis',
            name='metricDisplay',
            field=models.CharField(max_length=36),
        ),
    ]
