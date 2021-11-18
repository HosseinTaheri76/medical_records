# Generated by Django 3.2.5 on 2021-07-23 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('documents', '0002_alter_doctor_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(max_length=200, verbose_name='دلیل مراجعه')),
                ('visit_date', models.DateField(verbose_name='تاریخ مراجعه')),
                ('next_visit', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ مراجعه بعدی')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='documents.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='accounts.patient')),
            ],
            options={
                'verbose_name': 'مراجعه',
                'verbose_name_plural': 'مراجعات',
            },
        ),
    ]
