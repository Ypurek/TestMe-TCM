from django.http import HttpResponseNotAllowed


def allowed_methods(*methods):
    def intern_decorator(func):
        def wrapper(*args, **kwargs):
            if args[0].method in methods:
                return func(*args, **kwargs)
            else:
                return HttpResponseNotAllowed(list(methods))



        return wrapper

    return intern_decorator