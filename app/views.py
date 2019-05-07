
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.analyze_project import get_methods_without_features, get_all_tested_methods, get_features_without_methods, \
    distribute_importance_group, number_tests_by_group
from app.forms import FeatureForm
from app.models import Project, Feature, SimpleScenario, Method, Spec
from app.populate_db import create_entities, prepare_graph, prepare_feature_graph, prepare_method_graph, save_methods, \
    distribute_prob, prepare_spec_graph
from app.tree_object import create_chart, create_nodes


def index(request):
    context = {}
    return render(request, 'index.html')


def list_projects(request):
    projects = Project.objects.all()

    context = {"projects": projects}
    return render(request, 'projects.html', context)


def show_tree(request, id):
    project = Project.objects.get(pk=id)
    chart = create_chart()
    nodeStructure = create_nodes(project)

    context = {"chart": str(chart),
               "nodeStructure": str(nodeStructure),
               "project": project}
    return render(request, 'feature_tree.html', context)


def show_project(request, id):
    project = Project.objects.get(pk=id)
    met_features = get_methods_without_features(id)
    met_specs = get_all_tested_methods(id)
    methods = project.methods.all()
    specs = project.specs.all()
    # features_without_methods = get_features_without_methods(id)
    context = {"project": project,
               "met_features": met_features,
               "met_specs": met_specs,
               "methods": methods,
               "specs": specs}
               # "features_without_methods": features_without_methods}
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


def list_specs(request, id):
    specs = Spec.objects.filter(project=id)
    context = {"specs": specs
               }
    return render(request, 'specs_list.html', context)


def list_methods(request, id):
    methods = Method.objects.filter(project=id).all()

    sorted_methods = sorted(methods, key=lambda t: t.get_probability(), reverse=True)

    importance_groups = distribute_importance_group(sorted_methods)
    number_tests = number_tests_by_group(importance_groups)

    project = Project.objects.filter(id=id)
    context = {"methods": importance_groups,
               "number_tests": number_tests,
               "project": project
               }
    return render(request, 'methods_list.html', context)


def all_methods(request, id):
    methods = Method.objects.filter(project=id)
    project = Project.objects.filter(id=id)

    context = {
        "methods": methods,
        "project": project
    }

    return render(request, 'all_methods.html', context)



def bubble_chart(request, id):
    graph = prepare_graph(id)
    context = {
        "graph": graph
    }
    return render(request, 'bubble_chart.html', context)


def random_prob(request, id):
    distribute_prob(id)
    return render(request, 'index.html')


def graph(request, id):
    graph = prepare_graph(id)
    context = {
        "graph": graph
    }
    return render(request, 'full_graph.html', context)


def graph_features(request, id):
    graph = prepare_feature_graph(id)
    context = {
        "graph": graph
    }
    return render(request, 'graph_representation.html', context)


def graph_specs(request, id):
    graph = prepare_spec_graph(id)
    context = {
        "graph": graph
    }
    return render(request, 'graph_specs.html', context)


def graph_method(request, id):
    graph = prepare_method_graph(id)
    context = {
        "graph": graph
    }
    return render(request, 'graph_method.html', context)


@api_view(["POST"])
def create_project(project):

    result = create_entities(project)
    return Response(result)


@api_view(["POST"])
def create_methods(methods):

    result = save_methods(methods)
    return Response(result)


def insert_probabilities(request, id):
    context = {}
    features = Feature.objects.filter(project=id)

    if request.method == 'POST':
        # print(request.POST)
        # if 'features' in request.POST:
        #     for feature in features:
        #         feature.probability = float(request.POST['features'][feature.path_name])
        #         feature.save()
        #     try:
        #         content = json.loads(project.features)
        #     except json.JSONDecodeError:
        #         content = {}

        return render(request, 'index.html')

    else:
        new_fields = {}
        context['features'] = []
        for feature in features:
            context['features'].append(FeatureForm)

    context['oi'] = 'lslalsalsalslaslalsla'
    # IngForm = DynamicIngridientsForm(content)
    # context['features_form'] = IngForm
    # print(context)
    # return render(request, "demo/dynamic.html", context)
    return render(request, 'insert_prob.html', context)

