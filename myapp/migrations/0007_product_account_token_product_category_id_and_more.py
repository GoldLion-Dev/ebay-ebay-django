# Generated by Django 4.2.4 on 2023-10-28 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='account_token',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='category_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='condition_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=30000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='item_specifics',
            field=models.TextField(max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='listing_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='picture_urls',
            field=models.TextField(max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='qty',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
