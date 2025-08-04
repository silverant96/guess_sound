from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SoundItem
import random

@login_required
def play(request):
    sounds = list(SoundItem.objects.all())
    if not sounds:
        return render(request, 'game/play.html', {'error': 'Нет доступных звуков.'})

    # Если только один звук — не можем составить выбор (нужны 2 неправильных варианта)
    if len(sounds) < 3:
        # Всё равно играем, но просто показываем все доступные картинки
        choices = sounds.copy()
        random.shuffle(choices)
        correct = random.choice(sounds)
        return render(request, 'game/play.html', {
            'sound': correct,
            'choices': choices,
            'warning': 'Добавьте больше звуков, чтобы игра была интереснее!',
        })

    # Обычная игра: выбираем правильный + 2 случайных неправильных
    correct = random.choice(sounds)
    all_others = [s for s in sounds if s.id != correct.id]
    wrong_choices = random.sample(all_others, 2)  # теперь точно есть минимум 2 других
    choices = wrong_choices + [correct]
    random.shuffle(choices)

    return render(request, 'game/play.html', {
        'sound': correct,
        'choices': choices,
    })