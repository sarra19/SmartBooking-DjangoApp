from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Front-Office

def indexF(request, *args, **kwargs):
    return render(request , 'frontOffice/index.html')

@login_required
def tour(request, *args, **kwargs):
    return render(request , 'frontOffice/tour.html')

@login_required
def testimonial(request, *args, **kwargs):
    return render(request , 'frontOffice/testimonial.html')

@login_required
def services(request, *args, **kwargs):
    return render(request , 'frontOffice/services.html')

@login_required
def packages(request, *args, **kwargs):
    return render(request , 'frontOffice/packages.html')

@login_required
def guides(request, *args, **kwargs):
    return render(request , 'frontOffice/guides.html')

@login_required
def gallery(request, *args, **kwargs):
    return render(request , 'frontOffice/gallery.html')

@login_required
def destination(request, *args, **kwargs):
    return render(request , 'frontOffice/destination.html')

@login_required
def contact(request, *args, **kwargs):
    return render(request , 'frontOffice/contact.html')

@login_required
def booking(request, *args, **kwargs):
    return render(request , 'frontOffice/booking.html')

@login_required
def blog(request, *args, **kwargs):
    return render(request , 'frontOffice/blog.html')

@login_required
def base(request, *args, **kwargs):
    return render(request , 'frontOffice/base.html')

@login_required
def about(request, *args, **kwargs):
    return render(request , 'frontOffice/about.html')

@login_required
def p404(request, *args, **kwargs):
    return render(request , 'frontOffice/404.html')


####################################################################################

# Back-Office

def home(request, *args, **kwargs):
    return render(request, 'backOffice/index.html')

def dashboard(request, *args, **kwargs):
    return render(request, 'backOffice/index.html')

def profile(request, *args, **kwargs):
    return render(request, 'backOffice/pages/profile.html')

def settings(request, *args, **kwargs):
    return render(request, 'backOffice/pages/settings.html')

def billing(request, *args, **kwargs):
    return render(request, 'backOffice/pages/billing.html')

def pricing(request, *args, **kwargs):
    return render(request, 'backOffice/pages/pricing.html')

def error_404(request, *args, **kwargs):
    return render(request, 'backOffice/pages/404-error.html')

def signin(request, *args, **kwargs):
    return render(request, 'backOffice/pages/sign-in.html')

def signup(request, *args, **kwargs):
    return render(request, 'backOffice/pages/sign-up.html')

def forget_password(request, *args, **kwargs):
    return render(request, 'backOffice/pages/forget-password.html')

def docs(request, *args, **kwargs):
    return render(request, 'backOffice/pages/docs.html')

def faq(request, *args, **kwargs):
    return render(request, 'backOffice/pages/faq.html')

# def add_accommodation(request, *args, **kwargs):
#     return render(request, 'backOffice/pages/Accommodation/add.html')

# docs

def accordions(request, *args, **kwargs):
    return render(request, 'backOffice/docs/accordions.html')

def alerts(request, *args, **kwargs):
    return render(request, 'backOffice/docs/alerts.html')

def badge(request, *args, **kwargs):
    return render(request, 'backOffice/docs/badge.html')

def borders(request, *args, **kwargs):
    return render(request, 'backOffice/docs/borders.html')

def breadcrumb(request, *args, **kwargs):
    return render(request, 'backOffice/docs/breadcrumb.html')

def button_group(request, *args, **kwargs):
    return render(request, 'backOffice/docs/button-group.html')

def buttons(request, *args, **kwargs):
    return render(request, 'backOffice/docs/buttons.html')

def card(request, *args, **kwargs):
    return render(request, 'backOffice/docs/card.html')

def carousel(request, *args, **kwargs):
    return render(request, 'backOffice/docs/carousel.html')

def changelog(request, *args, **kwargs):
    return render(request, 'backOffice/docs/changelog.html')

def close_button(request, *args, **kwargs):
    return render(request, 'backOffice/docs/close-button.html')

def collapse(request, *args, **kwargs):
    return render(request, 'backOffice/docs/collapse.html')

def colored_links(request, *args, **kwargs):
    return render(request, 'backOffice/docs/colored-links.html')

def colors(request, *args, **kwargs):
    return render(request, 'backOffice/docs/colors.html')

def credits(request, *args, **kwargs):
    return render(request, 'backOffice/docs/credits.html')

def dropdowns(request, *args, **kwargs):
    return render(request, 'backOffice/docs/dropdowns.html')

def forms(request, *args, **kwargs):
    return render(request, 'backOffice/docs/forms.html')

def gulp(request, *args, **kwargs):
    return render(request, 'backOffice/docs/gulp.html')

def docs(request, *args, **kwargs):
    return render(request, 'backOffice/docs/index.html')

def list_group(request, *args, **kwargs):
    return render(request, 'backOffice/docs/list-group.html')

def modal(request, *args, **kwargs):
    return render(request, 'backOffice/docs/modal.html')

def navbar(request, *args, **kwargs):
    return render(request, 'backOffice/docs/navbar.html')

def navs_tabs(request, *args, **kwargs):
    return render(request, 'backOffice/docs/navs-tabs.html')

def offcanvas(request, *args, **kwargs):
    return render(request, 'backOffice/docs/offcanvas.html')

def opacity(request, *args, **kwargs):
    return render(request, 'backOffice/docs/opacity.html')

def pagination(request, *args, **kwargs):
    return render(request, 'backOffice/docs/pagination.html')

def placeholders(request, *args, **kwargs):
    return render(request, 'backOffice/docs/placeholders.html')
def popovers(request, *args, **kwargs):
    return render(request, 'backOffice/docs/popovers.html')

def progress(request, *args, **kwargs):
    return render(request, 'backOffice/docs/progress.html')

def ratio(request, *args, **kwargs):
    return render(request, 'backOffice/docs/ratio.html')

def scrollspy(request, *args, **kwargs):
    return render(request, 'backOffice/docs/scrollspy.html')

def shadows(request, *args, **kwargs):
    return render(request, 'backOffice/docs/shadows.html')

def spinners(request, *args, **kwargs):
    return render(request, 'backOffice/docs/spinners.html')

def stacks(request, *args, **kwargs):
    return render(request, 'backOffice/docs/stacks.html')

def tables(request, *args, **kwargs):
    return render(request, 'backOffice/docs/tables.html')

def text_truncation(request, *args, **kwargs):
    return render(request, 'backOffice/docs/text-truncation.html')

def text(request, *args, **kwargs):
    return render(request, 'backOffice/docs/text.html')

def toasts(request, *args, **kwargs):
    return render(request, 'backOffice/docs/toasts.html')

def tooltips(request, *args, **kwargs):
    return render(request, 'backOffice/docs/tooltips.html')

def typography(request, *args, **kwargs):
    return render(request, 'backOffice/docs/typography.html')

def vertical_rule(request, *args, **kwargs):
    return render(request, 'backOffice/docs/vertical-rule.html')

