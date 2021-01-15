from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from tcm.conf import TestStatus, PAGE_SIZE
from tcm.forms import TestCaseForm, UpdateTestCaseForm
from tcm.models import TestCase, TestRun
from django.http import JsonResponse, HttpResponse
from .decorators import allowed_methods
import json
import csv
import os
import uuid


def get_stats():
    stats = dict()
    stats['total'] = TestCase.objects.count()
    passed = 0
    failed = 0
    for test in TestCase.objects.prefetch_related('runs').all():
        runs = test.runs
        if runs.count() > 0:
            if runs.latest('timestamp').status == TestStatus.PASS.value:
                passed += 1
            elif runs.latest('timestamp').status == TestStatus.FAIL.value:
                failed += 1
    stats['passed'] = passed
    stats['failed'] = failed
    stats['norun'] = stats['total'] - failed - passed
    return stats


@login_required
@allowed_methods('GET')
def dashboard(request):
    return render(request, 'home.html', context=get_stats())


@login_required
@allowed_methods('GET')
def test_cases(request):
    tc_list = TestCase.objects.prefetch_related('runs').all()
    full_list = list()
    for tc in tc_list[:PAGE_SIZE]:
        if tc.runs.count() > 0:
            status = tc.runs.latest('timestamp').status
            executor = tc.runs.latest('timestamp').executor
        else:
            status, executor = 'Norun', None
        full_list.append({
            'id': tc.id,
            'name': tc.name,
            'description': tc.description,
            'author': tc.author,
            'status': status,
            'last_executor': executor
        })
    return render(request, 'testcases.html', context={'tests': full_list,
                                                      'count': len(tc_list),
                                                      'end': len(tc_list) <= PAGE_SIZE})


@login_required
@allowed_methods('GET')
def test_runs(request):
    payload = dict()
    runs = TestRun.objects.all()
    payload['test_runs'] = runs[:PAGE_SIZE]
    payload['count'] = len(runs)
    payload['end'] = len(runs) <= PAGE_SIZE

    return render(request, 'testruns.html', context=payload)


@login_required
@allowed_methods('GET', 'POST')
def new_test(request):
    if request.method == "POST":
        data = dict()
        data['name'] = request.POST['name']
        data['description'] = request.POST['description']
        data['author'] = request.user.id
        form = TestCaseForm(data)
        if form.is_valid():
            form.save()
            return redirect('new_test')
    else:
        form = TestCaseForm()
    return render(request, "newtest.html", {"form": form})


@login_required
@allowed_methods('GET', 'POST')
def update_test(request, test_id: int):
    test = get_object_or_404(TestCase, id=test_id)
    form = UpdateTestCaseForm(request.POST or None, instance=test)
    if form.is_valid():
        t = form.save(commit=False)
        t.save()
    return render(request, "updateTest.html", {"form": form,
                                               "author": test.author,
                                               'test_id': test.id,
                                               'test_runs': test.runs.count()})


@login_required
@allowed_methods('POST')
def update_test_status(request, test_id: int):
    body = json.loads(request.body)
    test = TestCase.objects.filter(id=test_id)
    if len(test) == 0:
        return JsonResponse({'error': 'test not found'}, status=404)
    run = TestRun.objects.create(test_case=test[0], status=body['status'], executor=request.user)
    return JsonResponse({'runId': run.id}, status=200)


@login_required
@allowed_methods('DELETE')
def delete_test(request, test_id: int):
    test = get_object_or_404(TestCase, id=test_id)
    test.delete()
    return JsonResponse({'deleted': True}, status=200)


@login_required
@allowed_methods('GET')
def refresh_stats(request):
    return JsonResponse(get_stats(), status=200)


@login_required
@allowed_methods('GET')
def lazy_load_tests(request):
    current_page = int(request.GET.get('page'))
    # todo
    tc_list = TestCase.objects.all()
    the_end = (current_page + 1) * PAGE_SIZE > len(tc_list)
    tests = tc_list[current_page * PAGE_SIZE: (current_page + 1) * PAGE_SIZE]
    payload = list()
    for tc in tests:
        if tc.runs.count() > 0:
            status = tc.runs.latest('timestamp').status
            executor = tc.runs.latest('timestamp').executor
        else:
            status, executor = 'Norun', None
        payload.append({
            'id': tc.id,
            'name': tc.name,
            'description': tc.description,
            'author': tc.author,
            'status': status,
            'executor': executor
        })
    return JsonResponse({'tests': payload,
                         'end': the_end}, status=200)


@login_required
@allowed_methods('GET')
def lazy_load_runs(request):
    current_page = int(request.GET.get('page'))
    run_list = TestRun.objects.all()
    the_end = (current_page + 1) * PAGE_SIZE > len(run_list)
    payload = runs_2_json(run_list[current_page * PAGE_SIZE: (current_page + 1) * PAGE_SIZE])
    return JsonResponse({'runs': payload,
                         'end': the_end}, status=200)


def runs_2_json(runs: list):
    result = []
    for run in runs:
        result.append({'id': run.test_case.id,
                       'name': run.test_case.name,
                       'status': run.status,
                       'executor': run.executor.username,
                       'timestamp': run.timestamp.strftime('%d-%m-%Y %H:%M:%S')})
    return result


@login_required
@allowed_methods('POST')
def upload_tests(request):
    if request.FILES.get('file') is None:
        return HttpResponse(status=400, content='not file provided')
    try:
        handle_uploaded_file(request.FILES.get('file'), request.user)
    except ValueError:
        return HttpResponse(status=400, content='not valid CSV')
    except TypeError:
        return HttpResponse(status=400, content='issue with headers or file format')
    except NotImplementedError:
        return HttpResponse(status=400, content='data not valid')
    return HttpResponse(status=201)


def handle_uploaded_file(f, user):
    file_data = b''
    for chunk in f.chunks():
        file_data += chunk
        # file_name = str(str(uuid.uuid4()) + '.csv')
        # with open(file_name, 'wb+') as file:
        #     for chunk in f.chunks():
        #         file.write(chunk)
        # with open(file_name, 'r') as file:
    reader = csv.reader(file_data.decode('utf-8').splitlines())
    headers = next(reader)
    if len(headers) != 2 or headers[0].lower().strip() != 'summary' or headers[1].lower().strip() != 'description':
        raise TypeError
    tests = list()
    for row in reader:
        form = TestCaseForm({'name': row[0], 'description': row[1], 'author': user})
        if not form.is_valid():
            raise NotImplementedError
        tests.append(form.save(commit=False))
    TestCase.objects.bulk_create(tests)
# if os.path.exists(file_name):
#     os.remove(file_name)


@login_required
@allowed_methods('GET')
def download_tests(request):
    tests = TestCase.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="testCases.csv"'
    writer = csv.writer(response)
    writer.writerow(['summary', 'description'])
    for test in tests:
        writer.writerow([test.name, test.description])

    return response
