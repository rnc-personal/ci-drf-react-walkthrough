# Generated by Django 3.2.19 on 2023-07-01 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../mama-comment-scaled.c68deb8d161b.png', upload_to='images/'),
        ),
    ]
