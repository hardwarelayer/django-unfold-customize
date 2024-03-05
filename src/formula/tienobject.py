from django.http import HttpResponse
from django.views.generic import ListView
from .models import Tien

class TienObject(ListView):
    model = Tien
    template_name = 'admin/tien.html'

    def head(self, *args, **kwargs):
        last_book = self.get_queryset().latest("publication_date")
        response = HttpResponse(
            # RFC 1123 date format.
            headers={
                "Last-Modified": last_book.publication_date.strftime(
                    "%a, %d %b %Y %H:%M:%S GMT"
                )
            },
        )
        return response