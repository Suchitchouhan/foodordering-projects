# Generated by Django 3.1.2 on 2020-12-31 12:35

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foodordering', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='delivery_employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default='', max_length=20)),
                ('name', models.CharField(default='', max_length=100)),
                ('mobile', models.CharField(default='9999999999', max_length=20)),
                ('city', models.CharField(default='noida', max_length=50)),
                ('state', models.CharField(default='Delhi', max_length=50)),
                ('zipcode', models.CharField(default='666666', max_length=10)),
                ('address', models.CharField(default='First Name', max_length=400)),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('package', models.IntegerField(default=10)),
                ('on_duty', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='rating_for_delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=0)),
                ('for_emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.delivery_employee')),
            ],
        ),
        migrations.CreateModel(
            name='delivery_assign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='pending', max_length=100)),
                ('des', models.CharField(default='pending', max_length=400)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.delivery_employee')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='foodordering.order')),
            ],
        ),
    ]