from sitesetup.models import SiteSetup

from django.shortcuts import render
from django.shortcuts import get_object_or_404

def index(request):
    context = {
        'site_title': get_object_or_404(SiteSetup, id=4).title,
    }
    return render(request, 'main/pages/index.html', context)
