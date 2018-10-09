from rest_framework.response import Response
from rest_framework.utils import json

from app.models import Feature, SimpleScenario, Method


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
