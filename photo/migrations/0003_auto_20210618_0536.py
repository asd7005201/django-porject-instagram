# Generated by Django 2.2 on 2021-06-18 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_auto_20210618_0531'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='update',
            new_name='updated',
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='timeline_photo/%Y/%m/%D'),
        ),
    ]
