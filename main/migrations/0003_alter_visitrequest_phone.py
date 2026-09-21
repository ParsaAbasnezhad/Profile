from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_visitrequest"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visitrequest",
            name="phone",
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
