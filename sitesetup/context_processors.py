from sitesetup.models import SiteSetup

def blog_setup(request):
    try:
        site_setup = SiteSetup.objects.get(id=2)
    except SiteSetup.DoesNotExist:
        site_setup = None
    return {'blog_setup': site_setup,}


def gallery_setup(request):
    try:
        site_setup = SiteSetup.objects.get(id=3)
    except SiteSetup.DoesNotExist:
        site_setup = None
    return {'gallery_setup': site_setup,}


def main_setup(request):
    try:
        site_setup = SiteSetup.objects.get(id=4)
    except SiteSetup.DoesNotExist:
        site_setup = None
    return {'main_setup': site_setup,}
