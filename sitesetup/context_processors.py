from sitesetup.models import SiteSetup

def blog_setup(request):
    site_setup = SiteSetup.objects.get(id=2)
    return {'blog_setup': site_setup,}


def gallery_setup(request):
    site_setup = SiteSetup.objects.get(id=3)
    return {'gallery_setup': site_setup,}
