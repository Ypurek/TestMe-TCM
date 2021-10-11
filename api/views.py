from django.shortcuts import render, get_object_or_404
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from tcm.views.decorators import allowed_methods
from django.shortcuts import redirect
import json
from tcm.models import TestCase, TestRun
from tcm.views.testnrun import get_stats


@csrf_exempt
def get_csrf_token(request):
    return HttpResponse(get_token(request), status=200)


@csrf_exempt
@allowed_methods('POST')
def api_login(request):
    body = json.loads(request.body)
    match body:
        case {'username': username, 'password': password}:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('', status=200)
            else:
                return JsonResponse({'error': 'username or password not correct'}, status=401)
        case _:
            return JsonResponse({'error': 'bad input data'}, status=400)


def api_logout(request):
    logout(request)
    return HttpResponse('', status=200)


def api_tests(request):
    page = request.GET.get('page')
    size = request.GET.get('size')
    if page is None or size is None:
        page, size = 0, 20
    elif page.isnumeric() and size.isnumeric():
        page, size = int(page), int(size)
    else:
        return JsonResponse({'error': 'bad query params'}, status=400)
    tc_list = TestCase.objects.all()
    results = list()
    for tc in tc_list[page:size]:
        if tc.runs.count() > 0:
            status = tc.runs.latest('timestamp').status
            executor = tc.runs.latest('timestamp').executor
        else:
            status, executor = 'Norun', None
        results.append({
            'id': tc.id,
            'name': tc.name,
            'description': tc.description,
            'author': tc.author.username,
            'status': status,
            'executor': executor.username
        })
    return JsonResponse({'page': page, 'size': size, 'total': len(tc_list), 'tests': results}, status=200)


@allowed_methods('GET', 'PUT', 'PATCH', 'DELETE')
def api_test(request, id: int):
    test = TestCase.objects.filter(id=id)
    if len(test) == 0:
        return HttpResponse('', status=404)

    test = test[0]
    match request.method:
        case 'GET':
            if test.runs.count() > 0:
                status = test.runs.latest('timestamp').status
                executor = test.runs.latest('timestamp').executor
            else:
                status, executor = 'Norun', None
            return JsonResponse({
                'id': test.id,
                'name': test.name,
                'description': test.description,
                'author': test.author.username,
                'status': status,
                'executor': executor.username
            }, status=200)
        case 'PUT':
            try:
                body = json.loads(request.body)
            except json.decoder.JSONDecodeError:
                return JsonResponse({'error': 'bad input data'}, status=400)
            match body:
                case {'name': str(), 'description': str()}:
                    test.name = body['name']
                    test.description = body['description']
                    test.author = request.user
                    test.save()
                    return JsonResponse({
                        'id': test.id,
                        'name': test.name,
                        'description': test.description,
                        'author': test.author.username,
                    }, status=200)
                case _:
                    return JsonResponse({'error': 'bad input data'}, status=200)
        case 'PATCH':
            try:
                body = json.loads(request.body)
            except json.decoder.JSONDecodeError:
                return JsonResponse({'error': 'bad input data'}, status=400)
            if body.get('name') is not None:
                test.name = body.get('name')
            if body.get('description') is not None:
                test.description = body.get('description')
            test.author = request.user
            test.save()
            return JsonResponse({
                'id': test.id,
                'name': test.name,
                'description': test.description,
                'author': test.author.username,
            }, status=200)
        case 'DELETE':
            test = get_object_or_404(TestCase, id=id)
            test.delete()
            return JsonResponse({'status': 'deleted'}, status=200)


@allowed_methods('POST')
def update_test_status(request, id: int):
    try:
        body = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({'error': 'bad input data'}, status=400)
    test = TestCase.objects.filter(id=id)
    if len(test) == 0:
        return JsonResponse({'error': 'test not found'}, status=404)
    run = TestRun.objects.create(test_case=test[0], status=body['status'], executor=request.user)
    return JsonResponse({'runId': run.id}, status=200)


@allowed_methods('GET')
def api_stats(request):
    return JsonResponse(get_stats(), status=200)
