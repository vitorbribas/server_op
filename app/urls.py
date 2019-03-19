from django.urls import path

from app import views

app_name = 'app'

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    # url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    path('', views.index, name='index'),
    path('projects', views.list_projects, name='projects'),
    path('tree/<int:id>', views.show_tree, name='tree'),
    path('project/<int:id>', views.show_project, name='project'),
    path('features/<int:id>', views.list_features, name='features'),
    path('scenarios/<int:id>', views.list_scenarios, name='list_scenarios'),
    path('createproject', views.create_project),
    path('graphfeatures/<int:id>', views.graph_features, name='graph'),
    path('bublechart/<int:id>', views.bubble_chart, name='bubble'),
    path('insertprob/<int:id>', views.insert_probabilities, name='prob')
]

