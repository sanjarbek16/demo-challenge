# Generated by Django 3.1.3 on 2020-11-24 04:15

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ('created',)},
        ),
        migrations.AddField(
            model_name='profile',
            name='joined_challenges',
            field=models.ManyToManyField(through='challenges.Joined', to='challenges.Challenge'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.upload_to),
        ),
        migrations.AlterField(
            model_name='profile',
            name='back_image',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.upload_back),
        ),
    ]
