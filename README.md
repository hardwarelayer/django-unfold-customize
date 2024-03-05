## I. The base code:

The demo site of Django Unfold suite: https://demo.unfoldadmin.com/admin/

The code for that site is here: https://github.com/unfoldadmin/formula/

Please look that formula's Readme.MD for clone and run it locally.

## II. Guide for view modification:

Based on the formula code.

I have implemented several ways of customizing Django Unfold.

Running it: see formula above

sample .env file

    DEBUG=1
    SECRET_KEY="adsafdsafr3r2few"
    ALLOWED_HOSTS=127.0.0.1,0.0.0.0,localhost

Run:

    $ poetry run env $(cat .env) python src/manage.py runserver

### 1. Customize the index page:

![Base menu image.](/guide/tien_img1.png)

This use the admin:index method in settings.py

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "items": [
                    {
                        "title": _("Index page"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },

The template file is in: templates/admin/index.html

### 2. Standard model:

This is not customize, but the standard way of usage of Django admin+unfold model and auto-generated-views is as following:

![Base menu image.](/guide/tien_img2.png)

Define model in models.py

    class Constructor(models.Model):
        name = models.CharField(_("name"), max_length=255)

        class Meta:
            db_table = "constructors"
            verbose_name = _("constructor")
            verbose_name_plural = _("constructors")

        def __str__(self):
            return self.name

Use that "constructor" model in settings.py:

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "items": [
                    {
                        "title": _("Index page"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Standard Model"),
                        "icon": "grade",
                        "link": reverse_lazy("admin:formula_constructor_changelist"),
                        "permission": "formula.utils.permission_callback",
                    },

"admin" is the interface "django.contrib.admin", imported here in settings.py

    INSTALLED_APPS = [
        "modeltranslation",
        "unfold",
        "unfold.contrib.filters",
        "unfold.contrib.import_export",
        "unfold.contrib.guardian",
        "unfold.contrib.simple_history",
        "unfold.contrib.forms",
        "django.contrib.admin",

This "admin" will create the view automatically for the model "constructor". Then it will bind to SIDEBAR.

### 3. Proxy model:

I use a proxy model for registering one model repeatedly in admin.py

The Dummy1 model is actually proxy of Constructor model.

in admin.py:

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

and then get imported in settings.py's SIDEBAR:

                    {
                        "title": _("Proxy Model"),
                        "icon": "grade",
                        "link": reverse_lazy("admin:formula_dummy1_changelist"),
                        "permission": "formula.utils.permission_callback",
                    },

### 3. The customized view of a model:

![Base menu image.](/guide/tien_img3.png)

settings.py

                    {
                        "title": _("DummyModel&CustomTemplate"),
                        "icon": "grade",
                        "link": reverse_lazy("admin:formula_dummy2_changelist"),
                        "permission": "formula.utils.permission_callback",
                    },


the Dummy2 model is a proxy in models.py

    class Dummy2(Constructor):
        class Meta:
            proxy = True

being imported in admin.py and register here:

    from formula.models import (
        Constructor,
        Dummy1,
        Dummy2,
        Dummy3,
        User,
        Tien,
    )

register: Note that we specify a custom view template here, not rely on automatically generated view as standard Django admin's way.

    @admin.register(Dummy2, site=formula_admin_site)
    class Dummy2Admin(ModelAdmin):
        change_list_template = "admin/custom_view_for_model.html"
        pass

The template is in: templates/admin/custom_view_for_model.html

Using this way, we can build custom views inside Django Admin+Unfold.

How to code the ModelAdmin: 

https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#custom-template-options

https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_queryset


### 4. Other way of customizing views:

These methods are simpler, but it can't work seamlessly inside SIDEBAR as the above method.

I suggest you use the method 3, but I listed those here to help you understand more about the view customization.

#### 4.a Use a dummy model+override url:

I create SIDEBAR's item using a dummy model, and then override it using custom AdminSite's get_urls()

models.py

    class Dummy3(Constructor):
        class Meta:
            proxy = True


settings.py

                    {
                        "title": _("DummyModel for override"),
                        "icon": "grade",
                        "link": reverse_lazy("admin:formula_dummy3_changelist"),
                        "permission": "formula.utils.permission_callback",
                    },

tienadmin.py

    class TienAdmin(UnfoldAdminSite):
        login_form = LoginForm

        def get_urls(self):
            urls = super().get_urls()
            my_urls = [
                    path("formula/dummy3/", self.admin_view(tienview.my_view), name="formula/dummy3/"),
                ]
            return my_urls + urls

the TemplateView object is in tienview.py

    def my_view(request):
      template = loader.get_template("admin/dummy2.html")

      context = {
          "field1": "abc",
      }
      return HttpResponse(template.render(context, request))

#### 4.b Use a template view object:

In settings.py, we set the url directly

                    {
                        "title": _("TemplateView Object"),
                        "icon": "grade",
                        "link": "/admin/formula/chart2/",
                        "permission": "formula.utils.permission_callback",
                    },

in urls.py, we set the object:

    from formula.tienview import TienChartView
    ...
    urlpatterns = [
    ...
    path("admin/formula/chart2/", TienChartView.as_view()),
    ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


##### 4.c Use a custom object with template:

settings.py

                    {
                        "title": _("Custom Object"),
                        "icon": "grade",
                        "link": "/admin/formula/tien/",
                        "permission": "formula.utils.permission_callback",
                    },

urls.py

    from formula.tienobject import TienObject
    urlpatterns = [
        path("admin/formula/tien/", TienObject.as_view()),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

tienobject.py

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

