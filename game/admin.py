from django.contrib import admin
from .models import SoundItem

@admin.register(SoundItem)
class SoundItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sound', 'image')