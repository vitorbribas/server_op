import re

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.utils import json

from app.models import Feature, SimpleScenario, Method, Project


def save_methods(methods):
    """
    Save all methods of a project to avoid duplications
    :param methods: json with all methods
    :return: True of False
    """
    print('------------------------- Saving Methods -------------------------')
    loaded_json = json.loads(methods.data)
    for method in loaded_json:
        print('.', ' ')
        base = Method.objects.filter(method_id=method['method_id'])
        if len(base) > 0:
            print('Método já existe: ', method['method_id'])
            print('Olha ele na base: ', base[0].method_id)
        else:
            new_method = Method()
            new_method.class_path = method['class_path']
            new_method.method_name = method['method_name']
            new_method.class_name = method['class_name']
            new_method.method_id = method['method_id']
            new_method.save()


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
        print('------------------------- Reading New Feature -------------------------')
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

        for each_scenario in loaded_json['scenarios']:
            scenario = SimpleScenario()
            scenario.feature = feature
            scenario.scenario_title = each_scenario['scenario_title']
            scenario.line = each_scenario['line']
            criterion1 = Q(scenario_title=scenario.scenario_title)
            criterion2 = Q(feature=scenario.feature)
            base = SimpleScenario.objects.filter(criterion1 & criterion2)
            if len(base) > 0:
                print('Scenario Already exists!')
                base[0] = scenario
            else:
                print('Scenario: ', scenario.scenario_title)
                scenario.save()
            for method in each_scenario['executed_methods']:
                # if is_new_method(method):
                #     met = Method()
                #     met.method_name = method['method_name']
                #     met.class_name = method['class_name']
                #     met.class_path = method['class_path']
                #     met.save()
                #     scenario.executed_methods.add(met)
                # else:
                met = Method.objects.filter(method_id=method['method_id'])
                scenario.executed_methods.add(met[0])

        print('------------------------- DONE! -------------------------')
        return True
    except ValueError as e:
        return False


def is_new_method(method):
    methods = Method.objects.filter(method_id=method['method_id'])
    if len(methods) > 0:
        return False
    else:
        return True


def prepare_method_graph(id):
    SCENARIO_GROUP = 10
    METHOD_GROUP = 15
    print('Preparing Method Graph...')
    graph = {
        "nodes": [],
        "links": []
    }

    method = Method.objects.get(id=id)

    node = {
        "id": re.sub('[^A-Za-z0-9]+', '', (method.method_name + method.class_name)),
        "cod": method.id,
        "name": method.method_name,
        "group": METHOD_GROUP,
        "executed": method.scenarios.count(),
        "size": 1
    }

    graph['nodes'].append(node)
    for scenario in method.scenarios.all():
        feature = scenario.feature
        node = {
            "id": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.path_name)),
            "cod": scenario.id,
            "name": scenario.scenario_title,
            "group": SCENARIO_GROUP,
            "size": len(scenario.executed_methods.all())
        }
        if node not in graph['nodes']:
            graph['nodes'].append(node)

        link = {
            "source": re.sub('[^A-Za-z0-9]+', '', (method.method_name + method.class_name)),
            "target": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.path_name)),
            "value": 2
        }
        graph['links'].append(link)

        node = {
            "id": re.sub('[^A-Za-z0-9]+', '', feature.path_name),
            'cod': feature.id,
            "name": feature.feature_name,
            "group": 5,
            "size": get_size(feature.simple_scenarios.all())
        }
        if node not in graph['nodes']:
            graph['nodes'].append(node)

        link = {
            "source": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.path_name)),
            "target": re.sub('[^A-Za-z0-9]+', '', feature.path_name),
            "value": 2
        }
        graph['links'].append(link)

    with open('app/static/method_graph.json', 'w') as outfile:
        json.dump(graph, outfile)


def prepare_feature_graph(id):
    SCENARIO_GROUP = 10
    METHOD_GROUP = 15

    graph = {
        "nodes": [],
        "links": []
    }

    feature = Feature.objects.filter(id=id)[0]

    scenarios = SimpleScenario.objects.filter(feature=feature)
    print('Scenarios: ', len(scenarios))
    print('feature ', feature.path_name)
    node = {
        "id": re.sub('[^A-Za-z0-9]+', '', feature.path_name),
        'cod': feature.id,
        "name": feature.feature_name,
        "group": 5,
        "size": get_size(scenarios)
    }
    graph['nodes'].append(node)

    print('Feature Defined')

    for scenario in scenarios:
        methods = scenario.executed_methods.all()
        print('Scenario ', scenario.scenario_title, ': ', len(methods), ' executed methods.')
        node = {
            "id": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.path_name)),
            "cod": scenario.id,
            "name": scenario.scenario_title,
            "group": SCENARIO_GROUP,
            "size": len(methods)
        }
        if node not in graph['nodes']:
            graph['nodes'].append(node)

        # Create links between feature and scenarios
        link = {
            "source": re.sub('[^A-Za-z0-9]+', '', feature.path_name),
            "target": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.path_name)),
            "value": 2
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
                "source": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.path_name)),
                "target": re.sub('[^A-Za-z0-9]+', '', (method.method_name + method.class_name)),
                "value": 3
            }
            graph['links'].append(link)
    print('Number of nodes: ', len(graph['nodes']))
    print('Number of links: ', len(graph['links']))
    with open('app/static/feature_graph.json', 'w') as outfile:
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
                "id": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.path_name)),
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
                "target": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.path_name)),
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
                    "source": re.sub('[^A-Za-z0-9]+', '', (scenario.scenario_title + feature.path_name)),
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
