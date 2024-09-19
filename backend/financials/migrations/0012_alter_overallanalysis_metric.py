# Generated by Django 4.2 on 2024-09-06 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0011_remove_financedata_symbol_balancesheet_symbol_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overallanalysis',
            name='metric',
            field=models.CharField(choices=[('Cashratio', 'Cashratio'), ('Quickratio', 'Quickratio'), ('Currentratio', 'Currentratio'), ('TDTAratio', 'TDTAratio'), ('DEratio', 'DEratio'), ('NetProfitMargin', 'NetProfitMargin'), ('GrossProfitMargin', 'GrossProfitMargin'), ('RevenueGrowth', 'RevenueGrowth'), ('RevenueVsCoR', 'RevenueVsCoR'), ('Revenue', 'Revenue')], max_length=40),
        ),
    ]