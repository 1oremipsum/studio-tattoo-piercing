# Generated by Django 5.1.4 on 2025-02-05 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_portfolio_created_at_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='description',
            field=models.CharField(blank=True, max_length=85, null=True),
        ),
    ]
