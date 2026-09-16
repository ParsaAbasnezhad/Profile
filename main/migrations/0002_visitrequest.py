from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VisitRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_contacted", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Visit request",
                "verbose_name_plural": "Visit requests",
            },
        ),
    ]
