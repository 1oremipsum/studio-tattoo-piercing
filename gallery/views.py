from django.shortcuts import render

def gallery(request):
    ctx = {
        'site_title': 'Gallery - Tattoo & Piercing',
    }
    return render(request, 'gallery/pages/gallery.html', ctx)
