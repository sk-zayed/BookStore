# Generated by Django 3.2.6 on 2021-08-30 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Online_BookStore', '0003_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('ordered_book', models.CharField(max_length=50)),
                ('book_category', models.CharField(max_length=50)),
                ('book_cost', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Online_BookStore.customer')),
            ],
        ),
    ]
