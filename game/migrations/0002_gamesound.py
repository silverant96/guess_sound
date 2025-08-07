from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sound_type', models.CharField(choices=[('correct', 'Звук правильного ответа'), ('wrong', 'Звук неправильного ответа')], max_length=10, unique=True, verbose_name='Тип звука')),
                ('audio', models.FileField(upload_to='game_sounds/', verbose_name='Аудиофайл')),
            ],
            options={
                'verbose_name': 'Системный звук игры',
                'verbose_name_plural': 'Системные звуки игры',
            },
        ),
    ]