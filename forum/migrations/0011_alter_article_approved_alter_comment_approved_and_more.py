# Generated by Django 4.2.22 on 2025-06-28 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_alter_article_primary_image_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]
