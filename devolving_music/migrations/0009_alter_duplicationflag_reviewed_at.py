# Generated by Django 4.0.5 on 2022-06-07 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devolving_music', '0008_duplicationflag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duplicationflag',
            name='reviewed_at',
            field=models.DateTimeField(null=True),
        ),
    ]