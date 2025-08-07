from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SoundItem
import random

@login_required
def play(request):
    sounds = list(SoundItem.objects.all())
    if not sounds:
        return render(request, 'game/play.html', {'error': 'Нет доступных звуков.'})

    correct_sound = random.choice(sounds)
    all_choices = sounds.copy()
    random.shuffle(all_choices)

    # Получаем системные звуки
    try:
        correct_audio = GameSound.objects.get(sound_type='correct').audio.url
    except GameSound.DoesNotExist:
        correct_audio = None  # или оставить пустым

    try:
        wrong_audio = GameSound.objects.get(sound_type='wrong').audio.url
    except GameSound.DoesNotExist:
        wrong_audio = None

    return render(request, 'game/play.html', {
        'sound': correct_sound,
        'choices': all_choices,
        'correct_feedback_audio': correct_audio,
        'wrong_feedback_audio': wrong_audio,
    })