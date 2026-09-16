from django.contrib import admin

from .models import (
    ContactLink,
    ContactMessage,
    HeroStat,
    NowBuilding,
    Profile,
    Project,
    ProjectFeature,
    ProjectGalleryImage,
    Quote,
    SkillCategory,
    SkillItem,
    Tag,
    VisitRequest,
)

admin.site.site_header = "پنل مدیریت پورتفولیو"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "خوش اومدی 👋"



class HeroStatInline(admin.TabularInline):
    model = HeroStat
    extra = 1


class NowBuildingInline(admin.TabularInline):
    model = NowBuilding
    extra = 0
    show_change_link = True


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role_title", "is_available_for_freelance")
    inlines = [HeroStatInline, NowBuildingInline]


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "is_active")
    list_editable = ("is_active",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class SkillItemInline(admin.TabularInline):
    model = SkillItem
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "show_as_bars", "order")
    list_editable = ("order",)
    inlines = [SkillItemInline]


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1


class ProjectGalleryImageInline(admin.TabularInline):
    model = ProjectGalleryImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "order", "created_at")
    list_editable = ("is_published", "order")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    search_fields = ("title", "description")
    inlines = [ProjectFeatureInline, ProjectGalleryImageInline]


@admin.register(ContactLink)
class ContactLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    readonly_fields = ("name", "contact", "message", "created_at")
    search_fields = ("name", "contact", "message")


@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display = ("phone", "created_at", "is_contacted")
    list_editable = ("is_contacted",)
    list_filter = ("is_contacted", "created_at")
    search_fields = ("phone",)
    readonly_fields = ("phone", "created_at")