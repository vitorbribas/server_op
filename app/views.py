from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from app.models import Project, Feature


def index(request):
    context = {}
    return render(request, 'index.html')


def list_projects(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, 'projects.html', context)


def show_project(request, id):
    project = Project.objects.get(pk=id)
    context = {"project": project}
    return render(request, 'project_detail.html', context)


def list_features(request, id):
    features = Feature.objects.filter(project=id)
    context = {"features": features}
    return render(request, 'tables_dynamic.html', context)


# def gentella_html(request):
#     context = {}
#     # The template to be loaded as per gentelella.
#     # All resource paths for gentelella end in .html.
#
#     # Pick out the html file name from the url. And load that template.
#     load_template = request.path.split('/')[-1]
#     template = loader.get_template('app/' + load_template)
#     return HttpResponse(template.render(context, request))

