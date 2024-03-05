from unfold.sites import UnfoldAdminSite
from django.urls import include, path
from http import HTTPStatus
from typing import Any, Callable, Dict, List, Optional, Union
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.validators import EMPTY_VALUES
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.urls import URLPattern, path, reverse, reverse_lazy
from django.utils.functional import lazy
from django.utils.module_loading import import_string

from unfold.settings import get_config
from unfold.utils import hex_to_rgb
from unfold.widgets import CHECKBOX_CLASSES, INPUT_CLASSES

from .forms import LoginForm
from . import tienview

class TienAdmin(UnfoldAdminSite):
    login_form = LoginForm

    index_template = "admin/index.html"
    app_index_template = "admin/dummy2.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
                path("formula/dummy3/", self.admin_view(tienview.my_view), name="formula/dummy3/"),
            ]
        return my_urls + urls

    def index(
        self, request: HttpRequest, extra_context: Optional[Dict[str, Any]] = None
    ) -> TemplateResponse:
        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            "title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            "index": True,
            **(extra_context or {}),
        }

        dashboard_callback = get_config(self.settings_name)["DASHBOARD_CALLBACK"]

        if isinstance(dashboard_callback, str):
            context = import_string(dashboard_callback)(request, context)

        request.current_app = self.name

        return TemplateResponse(
            request, self.index_template or "admin/index.html", context
        )

demo_admin_site = TienAdmin()
