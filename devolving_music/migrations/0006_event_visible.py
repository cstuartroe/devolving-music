# Generated by Django 3.2 on 2022-05-30 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devolving_music', '0005_alter_event_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='visible',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
