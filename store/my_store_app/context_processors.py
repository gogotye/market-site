from .models import SiteConfiguration


def config(request):
    return {'configurations': SiteConfiguration.objects.first()}


def session(request):
    return {'session': request.session}