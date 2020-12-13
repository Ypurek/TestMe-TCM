from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from tcm.conf import TestStatus
from tcm.forms import TestCaseForm, UpdateTestCaseForm
from tcm.models import TestCaseStat, TestCase, TestRun
from django.http import HttpResponseNotFound, JsonResponse
import json
import datetime as dt

PAGE_SIZE = 40


def get_stats():
    stats = dict()
    stats['total'] = TestCaseStat.objects.count()
    stats['passed'] = TestCaseStat.objects.filter(status=TestStatus.PASS.value).count()
    stats['failed'] = TestCaseStat.objects.filter(status=TestStatus.FAIL.value).count()
    stats['norun'] = stats['total'] - stats['passed'] - stats['failed']
    return stats


@login_required
def dashboard(request):
    return render(request, 'home.html', context=get_stats())


@login_required
def test_cases(request):
    tc_list = TestCaseStat.objects.all()
    print(str(tc_list.query))
    return render(request, 'testcases.html', context={'tests': tc_list[:PAGE_SIZE],
                                                      'count': len(tc_list),
                                                      'end': len(tc_list) <= PAGE_SIZE})


@login_required
def test_runs(request):
    payload = dict()
    runs = TestRun.objects.all()
    payload['test_runs'] = runs[:PAGE_SIZE]
    payload['count'] = len(runs)
    payload['end'] = len(runs) <= PAGE_SIZE

    return render(request, 'testruns.html', context=payload)


@login_required
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
def update_test_status(request, test_id: int):
    body = json.loads(request.body)
    test = TestCase.objects.filter(id=test_id)
    if len(test) == 0:
        return JsonResponse({'error': 'test not found'}, status=404)
    run = TestRun.objects.create(test_case=test[0], status=body['status'], executor=request.user)
    return JsonResponse({'runId': run.id}, status=200)


@login_required
def delete_test(request, test_id: int):
    test = get_object_or_404(TestCase, id=test_id)
    test.delete()
    return JsonResponse({'deleted': True}, status=200)


@login_required
def refresh_stats(request):
    return JsonResponse(get_stats(), status=200)


@login_required
def lazy_load_tests(request):
    current_page = int(request.GET.get('page'))
    tc_list = TestCaseStat.objects.all()
    the_end = (current_page + 1) * PAGE_SIZE > len(tc_list)
    payload = tests_2_json(tc_list[current_page * PAGE_SIZE: (current_page + 1) * PAGE_SIZE])
    return JsonResponse({'tests': payload,
                         'end': the_end}, status=200)


def tests_2_json(tests: list):
    result = []
    for test in tests:
        author = None if test.test_case.author is None else test.test_case.author.username
        executor = None if test.last_executor is None else test.last_executor.username
        result.append({'id': test.test_case.id,
                       'name': test.test_case.name,
                       'description': test.test_case.description,
                       'author': author,
                       'status': test.status,
                       'executor': executor})
    return result


@login_required
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
