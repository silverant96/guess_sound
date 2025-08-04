from django.db import models

class SoundItem(models.Model):
    name = models.CharField("Название (например, Утка)", max_length=100)
    sound = models.FileField("Аудиофайл", upload_to='sounds/')
    image = models.ImageField("Картинка", upload_to='images/')

    def __str__(self):
        return self.name