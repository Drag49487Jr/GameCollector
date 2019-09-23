# Generated by Django 2.2.3 on 2019-09-10 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('rating', models.CharField(choices=[('E', 'Everyone'), ('T', 'Teen'), ('M', 'Mature')], default='E', max_length=1)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Game')),
            ],
        ),
    ]
