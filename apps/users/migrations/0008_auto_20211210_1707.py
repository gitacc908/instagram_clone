# Generated by Django 3.2.6 on 2021-12-10 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='full name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=32, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(upload_to='profile_images/', verbose_name='image'),
        ),
    ]
