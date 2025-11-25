from django.shortcuts import render
from django.conf import settings
from .forms import InputForm
from datetime import datetime
import os

def ex02_view(request):
    form = InputForm(request.POST or None)
    history = []
    log_file = settings.LOG_FILE

    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))
    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                timestamp, text = line.split(' | ', 1)
                history.append({'timestamp': timestamp, 'text': text})
    
    if request.method == 'POST' and form.is_valid():
        text = form.cleaned_data['text']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        history.append({'timestamp': timestamp, 'text': text})

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} | {text}\n")
 
        form = InputForm()

    context = {
        'form': form,
        'history': history
    }
    return render(request, 'ex02/ex02.html', context)
