# Generated by Django 4.1.6 on 2023-05-07 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_user_gender_alter_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointment_status',
            field=models.CharField(blank=True, choices=[('available', 'available'), ('booked', 'booked'), ('cancelled', 'cancelled')], default='available', max_length=17),
        ),
        migrations.AddField(
            model_name='appointment',
            name='cancelled_by',
            field=models.CharField(blank=True, choices=[('doctor', 'doctor'), ('patient', 'patient')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_date',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='booked_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='patient', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]