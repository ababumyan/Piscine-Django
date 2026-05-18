from django.shortcuts import render
from django.http import JsonResponse
import random
from d06 import settings
from datetime import datetime, timedelta

SESSION_DATETIME_FORMATS = ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f')


def _parse_session_datetime(value):
    for fmt in SESSION_DATETIME_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"time data {value!r} does not match expected formats")


# Create your views here.
def index(request):
    return render(request, 'ex/index.html', {
        'session_duration': settings.SESSION_DURATION,
    })

def get_random_user(request):
    username = request.session.get('username')
    user_session_str = request.session.get('user_session')
    now = datetime.now()
    if username and user_session_str:
        user_session = _parse_session_datetime(user_session_str)
        if now - user_session > timedelta(seconds=settings.SESSION_DURATION):
            request.session.clear()
            request.session['username'] = get_random_name()
            request.session['user_session'] = now.strftime('%Y-%m-%d %H:%M:%S') 
            return JsonResponse({'message': 'New session started', 'username': request.session['username'], 'user_session': request.session['user_session']}, status=202)
    else:
        request.session['username'] = get_random_name()
        request.session['user_session'] = now.strftime('%Y-%m-%d %H:%M:%S')
        return JsonResponse({'message': 'Session started', 'username': request.session['username'], 'user_session': request.session['user_session']}, status=201)
    return JsonResponse({'message': 'Same session', 'username': request.session['username'], 'user_session': request.session['user_session']}, status=200)
    



def get_random_name():
    username = random.choice(settings.USER_NAMES)
    return username