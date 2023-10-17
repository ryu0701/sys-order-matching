from django.conf import settings

def constant_text(request):
    return {
        'GA_GTAG_CODE': settings.GA_GTAG_CODE,
        #'GA_GTAG_CODE': 'G-444444',
    }

