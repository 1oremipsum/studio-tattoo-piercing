# Generated by Django 5.1.4 on 2024-12-27 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitesetup', '0003_menulink_site_setup'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetup',
            name='favicon',
            field=models.ImageField(blank=True, default='', upload_to='assets/favicon/%Y/%m/'),
        ),
    ]