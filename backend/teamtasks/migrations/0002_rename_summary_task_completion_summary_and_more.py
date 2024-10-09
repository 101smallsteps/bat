# Generated by Django 4.2 on 2024-10-09 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamtasks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='summary',
            new_name='completion_summary',
        ),
        migrations.AddField(
            model_name='task',
            name='completion_evidence',
            field=models.ImageField(blank=True, null=True, upload_to='task_evidence/'),
        ),
        migrations.AddField(
            model_name='task',
            name='expected_completed_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='expected_outcome',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='task_status',
            field=models.CharField(choices=[('created', 'Created'), ('started', 'Started'), ('completed', 'Completed'), ('accepted', 'Accepted'), ('closed', 'Closed')], default='created', max_length=20),
        ),
    ]
