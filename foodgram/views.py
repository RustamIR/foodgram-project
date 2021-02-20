from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    template_name = 'flatpages/about/author.html'


class SpecView(TemplateView):
    template_name = 'flatpages/about/spec.html'


def page_not_found(request, exception):
    return render(
        request, 'error/404.html', status=404
    )


def server_error(request):
    return render(request, 'error/500.html', status=500)
