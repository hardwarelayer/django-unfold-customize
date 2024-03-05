from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from formula.charts import Chart1View
from formula.tienadmin import demo_admin_site as formula_admin_site
from formula.tienview import TienChartView
from formula.tienobject import TienObject

urlpatterns = [
    path("", Chart1View.as_view(), name="home"),
    path("admin/formula/chart2/", TienChartView.as_view()),
    path("admin/formula/tien/", TienObject.as_view()),
    path('admin/', formula_admin_site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
