#from unfold.sites import UnfoldAdminSite
from .tienadminsite import TienAdminSite 
from .forms import LoginForm

class FormulaAdminSite(TienAdminSite):
    login_form = LoginForm

formula_admin_site = FormulaAdminSite()
