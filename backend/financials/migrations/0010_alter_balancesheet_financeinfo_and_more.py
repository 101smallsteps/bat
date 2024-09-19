# Generated by Django 4.2 on 2024-09-03 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0009_alter_overallanalysis_metric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancesheet',
            name='financeInfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.financedata'),
        ),
        migrations.AlterField(
            model_name='cashflow',
            name='financeInfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.financedata'),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='financeInfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.financedata'),
        ),
    ]