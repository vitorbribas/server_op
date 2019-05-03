import re
from random import randint

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.utils import json

from app.models import Feature, SimpleScenario, Method, Project, Spec


def save_methods(project):
    """
    Save all methods of a project to avoid duplications
    :param methods: json with all methods
    :return: True of False
    """
    print('------------------------- Saving Methods -------------------------')
    loaded_json = json.loads(project.data)
    project = get_project(loaded_json)
    for method in loaded_json['methods']:
        print('.', ' ')
        base = Method.objects.filter(method_id=method['method_id'])
        if len(base) > 0:
            print('Método já existe: ', method['method_id'])
            print('Olha ele na base: ', base[0].method_id)
        else:
            new_method = Method()
            new_method.class_path = method['class_path']
            new_method.method_name = method['method_name']
            new_method.content = method['content']
            new_method.class_name = method['class_name']
            new_method.method_id = method['method_id']
            if method['abc_score']:
                new_method.abc_score = method['abc_score']
            else:
                new_method.abc_score = 0
            new_method.project = project
            new_method.save()


def get_project(project_json):
    name = project_json['name']
    language = project_json['language']
    repository = project_json['repository']
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
        project = get_project(loaded_json['project'])
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


def prepare_spec_graph(id):
    SPEC_GROUP = 20
    METHOD_GROUP = 15

    graph = {
        "nodes": [],
        "links": []
    }

    specs = Spec.objects.filter(project=id)

    for spec in specs:
        node = {
            "id": re.sub('[^A-Za-z0-9]+', '', (spec.description + spec.file + str(spec.line))),
            'cod': spec.id,
            "name": spec.description,
            "group": SPEC_GROUP,
            "size": len(spec.executed_methods.all())
        }
        if node not in graph['nodes']:
            graph['nodes'].append(node)

        for method in spec.executed_methods.all():
            node = {
                "id": re.sub('[^A-Za-z0-9]+', '', (method.method_id + method.class_path)),
                "cod": method.id,
                "name": method.method_name,
                "group": METHOD_GROUP,
                "executed": method.scenarios.count(),
                "size": 1
            }
            if node not in graph['nodes']:
                graph['nodes'].append(node)

                # Create links between spec and method
            link = {
                "source": re.sub('[^A-Za-z0-9]+', '', (spec.description + spec.file + str(spec.line))),
                "target": re.sub('[^A-Za-z0-9]+', '', (method.method_id + method.class_path)),
                "value": 2
            }
            graph['links'].append(link)

    print('Number of nodes: ', len(graph['nodes']))
    print('Number of links: ', len(graph['links']))
    with open('app/static/spec_graph.json', 'w') as outfile:
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
            "id": re.sub('[^A-Za-z0-9]+', '', feature.path_name),
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
                "source": re.sub('[^A-Za-z0-9]+', '', feature.path_name),
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


def distribute_prob_scenarios(feature):
    scenarios = SimpleScenario.objects.filter(feature=feature)
    i = len(scenarios)
    print('Quantidade de Cenarios: ', i)
    aux = {}
    total = 0
    for count in range(i):
        aux[count] = randint(1, 100)
        total += aux[count]
    results = normalize(total, aux, feature.probability)
    total = 0
    for result, i in enumerate(results):
        scenarios[i].probability = results[i]
        total += scenarios[i].probability
        print('scenario Probability: ', scenarios[i].probability)
        scenarios[i].save()
    print('Total Scenarios: ', total)


def distribute_prob(id):
    features = Feature.objects.filter(project=id)
    i = len(features)
    aux = {}
    total = 0
    for count in range(i):
        aux[count] = randint(1, 100)
        total += aux[count]
    results = normalize(total, aux, 100)
    total = 0
    for result, i in enumerate(results):
        features[i].probability = results[i]
        total += features[i].probability
        features[i].save()
        print('Feature Prob: ', features[i].probability)
        distribute_prob_scenarios(features[i])
        print('-----------------------------------------')
    print('Total features: ', total)


def normalize(total, aux, base):
    for i in range(len(aux)):
        aux[i] = (aux[i]/total) * base
    return aux


