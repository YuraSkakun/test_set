from django.shortcuts import render

# Create your views here.


def handler400(request, exception=None):
    return render(request, 'core/errors/400.html',
                  {'title': '400 (Bad request)'}, status=400)


def handler403(request, exception=None):
    return render(request, 'core/errors/403.html',
                  {'title': '403 (HTTP Forbidden)'}, status=403)


def handler404(request, exception=None):
    return render(request, 'core/errors/404.html',
                  {'title': '404 (Page not found)'}, status=404)


def handler500(request):
    return render(request, 'core/errors/500.html',
                  {'title': '500 (Server error)'}, status=500)
