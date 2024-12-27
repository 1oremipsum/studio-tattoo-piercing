from sitesetup.models import SiteSetup


def site_setup(request):
    site_setup = SiteSetup.objects.all().first()
    return {'site_setup': site_setup,}