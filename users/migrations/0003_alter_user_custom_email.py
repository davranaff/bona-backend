# Generated by Django 4.1.4 on 2023-05-08 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_custom_email_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='custom_email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_email', to='users.email', verbose_name='User email'),
        ),
    ]
