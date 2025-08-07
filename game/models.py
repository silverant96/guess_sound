from django.db import models

class SoundItem(models.Model):
    name = models.CharField("Название (например, Утка)", max_length=100)
    sound = models.FileField("Аудиофайл", upload_to='sounds/')
    image = models.ImageField("Картинка", upload_to='images/')

    def __str__(self):
        return self.name

class GameSound(models.Model):
    SOUND_TYPE_CHOICES = [
        ('correct', 'Звук правильного ответа'),
        ('wrong', 'Звук неправильного ответа'),
    ]

    sound_type = models.CharField(
        max_length=10,
        choices=SOUND_TYPE_CHOICES,
        unique=True,
        verbose_name="Тип звука"
    )
    audio = models.FileField(
        upload_to='game_sounds/',
        verbose_name="Аудиофайл"
    )

    def __str__(self):
        return dict(self.SOUND_TYPE_CHOICES)[self.sound_type]

    class Meta:
        verbose_name = "Системный звук игры"
        verbose_name_plural = "Системные звуки игры"