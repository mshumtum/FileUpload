# Generated by Django 2.2.13 on 2020-09-07 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageRepo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]