# Generated by Django 4.0.5 on 2022-07-20 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devolving_music', '0009_alter_duplicationflag_reviewed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allow_soundcloud',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='allow_spotify',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='allow_youtube',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]