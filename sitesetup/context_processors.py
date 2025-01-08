from sitesetup.models import SiteSetup


def blog_setup(request):
    site_setup = SiteSetup.objects.all().first()
    return {'blog_setup': site_setup,}