# Generated by Django 3.2.14 on 2022-08-01 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='image',
            field=models.ImageField(null=True, upload_to='blogimages'),
        ),
    ]
