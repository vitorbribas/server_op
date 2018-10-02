from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json

from app.models import Project, Feature, SimpleScenario


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
    return render(request, 'features_list.html', context)


def list_scenarios(request, id):
    feature = Feature.objects.get(pk=id)
    scenarios = SimpleScenario.objects.filter(feature=id)
    context = {"feature": feature,
               "scenarios": scenarios
               }
    return render(request, 'cenarios_list.html', context)


@api_view(["POST"])
def create_project(project):
    try:
        print(project.data)
        return Response(True)
    except ValueError as e:
        return Response(False)

# def gentella_html(request):
#     context = {}
#     # The template to be loaded as per gentelella.
#     # All resource paths for gentelella end in .html.
#
#     # Pick out the html file name from the url. And load that template.
#     load_template = request.path.split('/')[-1]
#     template = loader.get_template('app/' + load_template)
#     return HttpResponse(template.render(context, request))

