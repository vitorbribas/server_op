from django.urls import path

from covrel.views import update_spectrum, covrel

app_name = 'covrel'

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    # url(r'^.*\.html', views.gentella_html, name='gentella'),
    path('<int:id>', covrel, name='covrel'),
    path('update_spectrum', update_spectrum),
]

