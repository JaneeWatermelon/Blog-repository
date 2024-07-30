# Generated by Django 5.0.7 on 2024-07-28 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_news_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='tags',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='comments',
            field=models.ManyToManyField(blank=True, to='news.comment'),
        ),
    ]
