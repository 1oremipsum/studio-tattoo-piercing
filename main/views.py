from django.shortcuts import render

def index(request):
    context = {
        'site_title': 'Studio Tattoo & Piercing'
    }
    return render(request, 'main/pages/index.html', context)
