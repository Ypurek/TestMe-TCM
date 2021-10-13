from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from tcm.views.decorators import allowed_methods
from tcm.models import TestCase, TestRun
from tcm.views.testnrun import get_stats
from django.core.exceptions import ValidationError
from api.decorators import auth_required
import json


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


@auth_required
@allowed_methods('GET')
def api_test_cases(request):
    page = request.GET.get('page', '0')
    size = request.GET.get('size', '20')
    if page.isnumeric() and size.isnumeric():
        p = int(page)
        s = int(size)
    else:
        p, s = 0, 20
    tc_list = TestCase.objects.all()
    results = list()
    for tc in tc_list[p * s:(p + 1) * s]:
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
            'executor': None if executor is None else executor.username
        })
    return JsonResponse({'page': p, 'size': s, 'total': len(tc_list), 'tests': results}, status=200)


@auth_required
@allowed_methods('GET', 'PUT', 'PATCH', 'DELETE')
def api_test(request, test_id: int):
    test = TestCase.objects.filter(id=test_id)
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
                'executor': None if executor is None else executor.username
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
def update_test_status(request, test_id: int):
    try:
        body = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({'error': 'bad input data'}, status=400)
    test = TestCase.objects.filter(id=test_id)
    if len(test) == 0:
        return JsonResponse({'error': 'test not found'}, status=404)
    run = TestRun.objects.create(test_case=test[0], status=body['status'], executor=request.user)
    return JsonResponse({'runId': run.id}, status=200)


@auth_required
@allowed_methods('GET')
def api_stats(request):
    return JsonResponse(get_stats(), status=200)


@allowed_methods('POST')
def api_new_test(request):
    try:
        body = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({'error': 'bad input data'}, status=400)

    match body:
        case {'name': str(), 'description': str()}:
            test = TestCase(name=body['name'],
                            description=body['description'],
                            author=request.user)
            try:
                test.validate_unique()
                test.save()
                return JsonResponse({'test_id': test.id}, status=201)
            except ValidationError:
                return JsonResponse({'error': 'test with such name already exists'}, status=400)

    return JsonResponse({'error': 'bad input data'}, status=400)
