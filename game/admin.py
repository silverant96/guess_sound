from django.contrib import admin
from .models import SoundItem, GameSound

@admin.register(SoundItem)
class SoundItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sound', 'image')

@admin.register(GameSound)
class GameSoundAdmin(admin.ModelAdmin):
    list_display = ('get_sound_type_display', 'audio')
    # Удалим sound_type из readonly_fields
    fields = ('sound_type', 'audio')  # Теперь sound_type будет доступен для редактирования

    def has_add_permission(self, request):
        # Разрешаем добавить только если ещё нет таких записей
        return GameSound.objects.count() < 2

    def has_delete_permission(self, request, obj=None):
        return False  # Чтобы случайно не удалить