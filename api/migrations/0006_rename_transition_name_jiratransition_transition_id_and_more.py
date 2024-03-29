# Generated by Django 4.1.3 on 2022-11-20 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_service_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jiratransition',
            old_name='transition_name',
            new_name='transition_id',
        ),
        migrations.RemoveField(
            model_name='jiraissue',
            name='oid',
        ),
        migrations.RemoveField(
            model_name='jiraissue',
            name='status',
        ),
        migrations.AddField(
            model_name='jiraissue',
            name='jira_key',
            field=models.CharField(default='', max_length=64, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jiraissue',
            name='jira_id',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
