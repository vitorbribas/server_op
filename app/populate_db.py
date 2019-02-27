import re

from rest_framework.response import Response
from rest_framework.utils import json

from app.models import Feature, SimpleScenario, Method, Project


def get_project(loaded_json):
    name = loaded_json['project']['name']
    language = loaded_json['project']['language']
    repository = loaded_json['project']['repository']
    project = Project.objects.filter(name=name)
    if project:
        return project[0]
    else:
        project = Project()
        project.name = name
        project.repository = repository
        project.language = language
        project.save()
        return project


def create_entities(project):
    feature = Feature()

    try:
        print('------------------------- SE LIGA AQUI MANO NESSA TRETA -------------------------')
        # print(project.data)
        loaded_json = json.loads(project.data)
        project = get_project(loaded_json)
        feature.project = project

        feature.path_name = loaded_json['path_name']
        feature.feature_name = loaded_json['feature_name']
        feature.language = loaded_json['language']
        feature.user_story = loaded_json['user_story']
        feature.background = loaded_json['background']
        features_db = Feature.objects.filter(path_name=feature.path_name).filter(project=feature.project)
        if not features_db:
            feature.save()
        print('SALVOU!')
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


def prepare_feature_graph(id):
    SCENARIO_GROUP = 10
    METHOD_GROUP = 15

    graph = {
        "nodes": [],
        "links": []
    }

    feature = Feature.objects.filter(id=id)[0]

    scenarios = SimpleScenario.objects.filter(feature=feature)
    node = {
        "id": re.sub('[^A-Za-z0-9]+', '', feature.feature_name),
        'cod': feature.id,
        "name": feature.feature_name,
        "group": 5,
        "size": get_size(scenarios)
    }
    graph['nodes'].append(node)

    for scenario in scenarios:
        methods = scenario.executed_methods.all()
        node = {
            "id": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.feature_name)),
            "cod": scenario.id,
            "name": scenario.scenario_title,
            "group": SCENARIO_GROUP,
            "size": len(methods)
        }
        if node not in graph['nodes']:
            graph['nodes'].append(node)

        # Create links between feature and scenarios
        link = {
            "source": re.sub('[^A-Za-z0-9]+', '', feature.feature_name),
            "target": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.feature_name)),
            "value": 3
        }
        graph['links'].append(link)

        for method in methods:
            node = {
                "id": re.sub('[^A-Za-z0-9]+', '', (method.method_name + method.class_name)),
                "cod": method.id,
                "name": method.method_name,
                "group": METHOD_GROUP,
                "executed": method.scenarios.count(),
                "size": 1
            }
            if node not in graph['nodes']:
                graph['nodes'].append(node)

            link = {
                "source": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.feature_name)),
                "target": re.sub('[^A-Za-z0-9]+', '', (method.method_name + method.class_name)),
                "value": 3
            }
            graph['links'].append(link)

    with open('app/static/feature_graph.json', 'w') as outfile:
        print(graph)
        json.dump(graph, outfile)


def prepare_graph(id):
    FEATURE_GROUP = 5
    SCENARIO_GROUP = 10
    METHOD_GROUP = 15

    graph = {
        "nodes": [],
        "links": []
    }

    project = Project.objects.get(pk=id)
    features = Feature.objects.filter(project=project)

    for feature in features:
        scenarios = SimpleScenario.objects.filter(feature=feature)
        node = {
            "id": re.sub('[^A-Za-z0-9]+', '', feature.feature_name),
            "cod": feature.id,
            "name": feature.feature_name,
            "group": FEATURE_GROUP,
            "size": get_size(scenarios)/5
        }
        if node not in graph['nodes']:
            graph['nodes'].append(node)
        for scenario in scenarios:
            methods = scenario.executed_methods.all()
            node = {
                "id": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.feature_name)),
                "cod": scenario.id,
                "name": scenario.scenario_title,
                "group": SCENARIO_GROUP,
                "size": len(methods)/5
            }
            if node not in graph['nodes']:
                graph['nodes'].append(node)

            # Create links between feature and scenarios
            link = {
                "source": re.sub('[^A-Za-z0-9]+', '', feature.feature_name),
                "target": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.feature_name)),
                "value": 3
            }
            graph['links'].append(link)

            for method in methods:
                node = {
                    "id": re.sub('[^A-Za-z0-9]+', '', (method.method_name + method.class_name)),
                    "cod": method.id,
                    "name": method.method_name,
                    "group": METHOD_GROUP,
                    "size": 1
                }
                if node not in graph['nodes']:
                    graph['nodes'].append(node)

                link = {
                    "source": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.feature_name)),
                    "target": re.sub('[^A-Za-z0-9]+', '', (method.method_name + method.class_name)),
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
