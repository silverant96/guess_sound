from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import SoundItem, GameSound
import random
import json

@login_required
def play(request):
    # Проверяем, не в процессе ли уже игра
    if request.method == "POST":
        # Сброс игры (если нажали "Начать игру" снова)
        request.session['game_started'] = True
        sounds = list(SoundItem.objects.all())
        if not sounds:
            return render(request, 'game/play.html', {'error': 'Нет доступных звуков.'})

        # Перемешиваем звуки один раз и сохраняем в сессии
        shuffled_sounds = random.sample(sounds, len(sounds))
        request.session['sound_order'] = [s.id for s in shuffled_sounds]
        request.session['current_index'] = 0
        request.session['correct_count'] = 0
        request.session['wrong_answers'] = []  # Будем хранить имена неправильных ответов

        return redirect('game:play')  # Перенаправляем, чтобы избежать повторной отправки POST

    # GET-запрос: либо показываем игру, либо результаты
    if not request.session.get('game_started'):
        # Показываем кнопку "Начать игру"
        return render(request, 'game/play.html', {
            'show_start': True,
            'error': None
        })

    # Получаем текущий прогресс
    current_index = request.session.get('current_index', 0)
    sound_order = request.session.get('sound_order', [])

    if current_index >= len(sound_order):
        # Игра закончена — показываем результаты
        return redirect('game:results')

    # Получаем текущий звук
    try:
        correct_sound = SoundItem.objects.get(id=sound_order[current_index])
    except SoundItem.DoesNotExist:
        return render(request, 'game/play.html', {'error': 'Ошибка: звук не найден.'})

    # Все варианты для выбора (всё ещё перемешиваем)
    all_sounds = list(SoundItem.objects.all())
    random.shuffle(all_sounds)

    # Получаем системные звуки
    try:
        correct_audio = GameSound.objects.get(sound_type='correct').audio.url
    except GameSound.DoesNotExist:
        correct_audio = None

    try:
        wrong_audio = GameSound.objects.get(sound_type='wrong').audio.url
    except GameSound.DoesNotExist:
        wrong_audio = None

    return render(request, 'game/play.html', {
        'sound': correct_sound,
        'choices': all_sounds,
        'correct_feedback_audio': correct_audio,
        'wrong_feedback_audio': wrong_audio,
        'progress': {
            'current': current_index + 1,
            'total': len(sound_order)
        }
    })


@login_required
def check_answer(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не разрешён'}, status=405)

    data = json.loads(request.body)
    selected = data.get('selected')
    correct = data.get('correct')

    # Проверяем ответ
    is_correct = selected == correct

    # Обновляем сессию
    if is_correct:
        request.session['correct_count'] += 1
        # Только при правильном ответе — переходим к следующему звуку
        request.session['current_index'] += 1
    else:
        request.session['current_index'] += 1  # ✅ ДОЛЖНО БЫТЬ!
        if correct not in request.session['wrong_answers']:
            request.session['wrong_answers'].append(correct)

    return JsonResponse({'correct': is_correct})


@login_required
def results(request):
    correct_count = request.session.get('correct_count', 0)
    total = len(request.session.get('sound_order', []))
    wrong_list = request.session.get('wrong_answers', [])

    # Опционально: сброс сессии после завершения
    for key in ['game_started', 'sound_order', 'current_index', 'correct_count', 'wrong_answers']:
        request.session.pop(key, None)

    return render(request, 'game/results.html', {
        'correct_count': correct_count,
        'wrong_count': total - correct_count,
        'wrong_list': wrong_list,
        'total': total
    })