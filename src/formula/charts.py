import json
import random

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView


class Chart1View(RedirectView):
    pattern_name = "admin:index"


def dashboard_callback(request, context):
    WEEKDAYS = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    context.update(
        {
        },
    )

    return context

def my_model_list_view(request): 
    html = "<html><body>Hello! It is now %s.</body></html>" % now
    return HttpResponse(html)
