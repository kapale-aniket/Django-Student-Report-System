# Generated migration for adding uuid_name and original_filename fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_evaluatorstudentassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectreport',
            name='uuid_name',
            field=models.CharField(blank=True, help_text='Unique UUID-based filename', max_length=255),
        ),
        migrations.AddField(
            model_name='projectreport',
            name='original_filename',
            field=models.CharField(blank=True, help_text='Original filename uploaded by user', max_length=255),
        ),
    ]

