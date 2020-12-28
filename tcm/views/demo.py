from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import time


@login_required
def dashboard(request):
    return render(request, 'demo.html')


@login_required
def wait_page(request):
    try:
        wait_time = int(request.GET.get('time'))
        if wait_time < 1 or wait_time > 100:
            return render(request, 'wait.html', status=400, context={'status': 'time not in range 1-100'})
    except ValueError:
        return render(request, 'wait.html', status=400, context={'status': 'time not int'})
    time.sleep(wait_time)
    return render(request, 'wait.html', context={'status': f'ok after {wait_time}'})


@login_required
def wait_ajax(request):
    return render(request, 'ajax.html', context={'status': f'ok'})


@login_required
def ajax_wait(request):
    try:
        wait_time = int(request.GET.get('time'))
        if wait_time < 1 or wait_time > 100:
            return JsonResponse(data={'status': 'time not in range 1-100'}, status=400)
    except ValueError:
        return JsonResponse(data={'status': 'time not int'}, status=400)
    time.sleep(wait_time)
    return JsonResponse(data={'status': 'ok'}, status=200)
