from django.contrib import admin
from sitesetup.models import MenuLink, SiteSetup


class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1


@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'url_or_path')
    list_display_links = ('id', 'text', 'url_or_path')
    search_fields = ('id', 'text', 'url_or_path')


@admin.register(SiteSetup)
class SiteSetup(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = MenuLinkInline,
