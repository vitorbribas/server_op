from app.models import Feature, SimpleScenario, Method


def create_chart():
    chart = {
        "container": "#OrganiseChart-big-commpany",
        "levelSeparation": 45,

        "rootOrientation": "NORTH",

        "nodeAlign": "BOTTOM",

        "connectors": {
            "type": "bCurve",
            "style": {
                "stroke-width": 2
            }
        },
        "node": {
            "HTMLclass": "big-commpany",
            "collapsable": "true"
        }
    }
    return chart


def create_nodes(project):
    features = Feature.objects.filter(project=project)
    nodeStructure = {
        "text": {"name": project.name},
        "connectors": {
            "style": {
                'stroke': '#bbb',
                'arrow-end': 'oval-wide-long'
            }
        },
        "children": create_features(features)
    }
    return nodeStructure


def create_features(parents):
    nodes = []
    for feature in parents:
        nodes.append({'text': {'name': feature.feature_name},
                      'children': create_scenarios(feature)})

    return nodes


def create_scenarios(feature):
    nodes = []
    scenarios = SimpleScenario.objects.filter(feature=feature)
    print('Number of scenarios: ', len(scenarios))
    for scenario in scenarios:
        nodes.append({'text': {'name': scenario.scenario_title},
                      'children': create_methods(scenario)})

    return nodes


def create_methods(scenario):
    nodes = []
    methods = Method.objects.filter(scenarios=scenario.id)
    for method in methods:
        nodes.append({'text': {'name': method.method_name},
                      "HTMLclass": "method"+str(method.id)})

    return nodes
