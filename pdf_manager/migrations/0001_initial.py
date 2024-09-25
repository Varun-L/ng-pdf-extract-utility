# Generated by Django 4.1.3 on 2024-09-25 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PdfFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_created=True)),
                ("name", models.CharField(max_length=255)),
                ("file", models.FileField(upload_to="pdfs/")),
            ],
        ),
    ]
