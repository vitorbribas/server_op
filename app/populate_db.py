from rest_framework.response import Response
from rest_framework.utils import json

from app.models import Feature, SimpleScenario, Method, Project


def create_entities(proj, project):
    feature = Feature()
    feature.project = proj

    try:
        print('------------------------- SE LIGA AQUI MANO NESSA TRETA -------------------------')
        print(project.data)
        loaded_json = json.loads(project.data)
        feature.path_name = loaded_json['path_name']
        feature.feature_name = loaded_json['feature_name']
        feature.language = loaded_json['language']
        feature.user_story = loaded_json['user_story']
        feature.background = loaded_json['background']

        feature.save()

        for each_scenario in loaded_json['scenarios']:
            scenario = SimpleScenario()
            scenario.feature = feature
            scenario.scenario_title = each_scenario['scenario_title']
            scenario.line = each_scenario['line']
            scenario.save()
            for method in each_scenario['executed_methods']:
                if is_new_method(method):
                    met = Method()
                    met.method_name = method['method_name']
                    met.class_name = method['class_name']
                    met.class_path = method['class_path']
                    met.save()
                    scenario.executed_methods.add(met)
                else:
                    met = Method.objects.filter(method_name=method['method_name'], class_path=method['class_path'])
                    scenario.executed_methods.add(met[0])

        print('------------------------- FOI NERVOSO -------------------------')
        return True
    except ValueError as e:
        return False


def is_new_method(method):
    methods = Method.objects.filter(method_name=method['method_name'], class_path=method['class_path'])
    if len(methods) > 0:
        return False
    else:
        return True


def prepare_graph():
    FEATURE_GROUP = 5
    SCENARIO_GROUP = 10
    METHOD_GROUP = 15

    graph = {
        "nodes": [],
        "links": []
    }

    project = Project.objects.get(pk=1)
    features = Feature.objects.filter(project=project)

    for feature in features:
        scenarios = SimpleScenario.objects.filter(feature=feature)
        node = {
            "id":feature.path_name,
            "group": FEATURE_GROUP,
            "size": get_size(scenarios)
        }
        if node not in graph['nodes']:
            graph['nodes'].append(node)
        for scenario in scenarios:
            methods = scenario.executed_methods.all()
            node = {
                "id": scenario.scenario_title,
                "group": SCENARIO_GROUP,
                "size": len(methods)
            }
            if node not in graph['nodes']:
                graph['nodes'].append(node)

            link = {
                "source": feature.path_name,
                "target": scenario.scenario_title,
                "value": 3
            }
            graph['links'].append(link)

            for method in methods:
                node = {
                    "id": method.method_name,
                    "group": METHOD_GROUP,
                    "size": 1
                }
                if node not in graph['nodes']:
                    graph['nodes'].append(node)

                link = {
                    "source": scenario.scenario_title,
                    "target": method.method_name,
                    "value": 3
                }
                graph['links'].append(link)

    with open('app/static/data2.json', 'w') as outfile:
        json.dump(graph, outfile)


def get_size(scenarios):
    methods_total = []
    for scenario in scenarios:
        methods = scenario.executed_methods.all()
        for meth in methods:
            if meth not in methods_total:
                methods_total.append(meth)

    return len(methods_total)