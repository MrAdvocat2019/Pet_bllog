# Generated by Django 5.1 on 2024-08-23 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('posts', '0004_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(to='categories.category'),
        ),
    ]
