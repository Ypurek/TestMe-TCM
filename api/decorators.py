from django.http import HttpResponseForbidden


def auth_required(func):
    def wrapper(*args, **kwargs):
        if args[0].user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return HttpResponseForbidden()

    return wrapper
