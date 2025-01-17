from django.core.paginator import Paginator

PER_PAGE = 9    # number of objects per page

def pagination(request, objs):
    paginator = Paginator(objs, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj
