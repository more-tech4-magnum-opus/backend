# Generated by Django 4.0.8 on 2022-10-08 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='salary',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('WORKER', 'worker'), ('HR', 'human resources'), ('ADMIN', 'administrator')], default='WORKER', max_length=6),
        ),
        migrations.AddField(
            model_name='user',
            name='clan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.clan'),
        ),
    ]