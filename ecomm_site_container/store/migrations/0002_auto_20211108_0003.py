# Generated by Django 3.2.8 on 2021-11-07 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ecomuser',
            name='phone_num',
        ),
        migrations.AddField(
            model_name='ecomuser',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='ecomuser',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='ecomuser',
            name='password',
            field=models.CharField(default='', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ecomuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='ecomuser',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='ecomuser',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('C', 'Confirmed'), ('T', 'In Transit'), ('D', 'Delivered'), ('X', 'Cancelled')], default='C', max_length=20),
        ),
    ]