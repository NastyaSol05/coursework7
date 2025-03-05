# Generated by Django 4.2.2 on 2025-02-28 20:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mailing", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="newsletter",
            options={
                "permissions": [
                    ("can_view_detail_newsletter", "Can view detail newsletter"),
                    ("can_delete_newsletter", "Can view detail newsletter"),
                ],
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
        migrations.AddField(
            model_name="emailattempt",
            name="owner",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="message",
            name="owner",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="newsletter",
            name="owner",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="recipient",
            name="owner",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
