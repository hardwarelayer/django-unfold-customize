from django.contrib.auth.decorators import user_passes_test
from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import OuterRef, Sum
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django_svelte_jsoneditor.widgets import SvelteJSONEditorWidget
from guardian.admin import GuardedModelAdmin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeNumericFilter,
    SingleNumericFilter,
)
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import action, display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.widgets import UnfoldAdminColorInputWidget

from formula.models import (
    Constructor,
    Dummy1,
    Dummy2,
    Dummy3,
    User,
    Tien,
)
from formula.resources import ConstructorResource
from formula.tienadmin import demo_admin_site as formula_admin_site

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(Group)

@admin.register(PeriodicTask, site=formula_admin_site)
class PeriodicTaskAdmin(ModelAdmin):
    pass


@admin.register(IntervalSchedule, site=formula_admin_site)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule, site=formula_admin_site)
class CrontabScheduleAdmin(ModelAdmin):
    pass

@admin.register(SolarSchedule, site=formula_admin_site)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule, site=formula_admin_site)
class ClockedScheduleAdmin(ModelAdmin):
    pass


@admin.register(User, site=formula_admin_site)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = [
        "display_header",
        "is_active",
        "display_staff",
        "display_superuser",
        "display_created",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": (("first_name", "last_name"), "email", "biography")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    readonly_fields = ["last_login", "date_joined"]

    @display(description=_("User"), header=True)
    def display_header(self, instance: User):
        return instance.full_name, instance.email

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, instance: User):
        return instance.is_staff

    @display(description=_("Superuser"), boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

    @display(description=_("Created"))
    def display_created(self, instance: User):
        return instance.created_at


@admin.register(Group, site=formula_admin_site)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(Constructor, site=formula_admin_site)
class ConstructorAdmin(ModelAdmin):
    search_fields = []
    list_display = []
    list_filter = ["name"]
    autocomplete_fields = []

#TienTN: using proxy model
@admin.register(Dummy1, site=formula_admin_site)
class Dummy1Admin(ModelAdmin):
    pass

"""
#this to fool the settings.py only, the url will be direct by TienAdmin to custom view 
@admin.register(Dummy2, site=formula_admin_site)
class Dummy2Admin(ModelAdmin):
    pass
"""

@admin.register(Dummy2, site=formula_admin_site)
class Dummy2Admin(ModelAdmin):
    change_list_template = "admin/custom_view_for_model.html"
    pass

#this to fool the settings.py only, the url will be direct by TienAdmin to custom view 
@admin.register(Dummy3, site=formula_admin_site)
class Dummy3Admin(ModelAdmin):
    pass
