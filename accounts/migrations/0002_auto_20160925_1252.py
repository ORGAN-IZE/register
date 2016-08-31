# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-25 12:52
from __future__ import unicode_literals

import accountsplus.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('masquerade', 'Can sign in as User'),), 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accountsplus.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='auditlogevent',
            name='company',
        ),
        migrations.AddField(
            model_name='auditlogevent',
            name='company_id',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Company ID'),
        ),
        migrations.AddField(
            model_name='auditlogevent',
            name='company_name',
            field=models.CharField(blank=True, db_index=True, max_length=100, verbose_name='Company Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accounts_user_users', to='accounts.Company'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Admin'),
        ),
    ]