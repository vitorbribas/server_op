from rest_framework.utils import json

from app.models import Project, Method, Feature, Spec
from app.populate_db import is_new_method


def group_methods(id):
    features = Feature.objects.filter(project=id)
    methods = set()
    for feature in features:
        scenarios = feature.simple_scenarios.all()
        for scenario in scenarios:
            methds = scenario.executed_methods.all()
            for me in methds:
                methods.add(me)
    methods = list(methods)
    methods.sort(key=lambda x: x.get_spec_count_spectra(), reverse=True)

    # part = int(len(methods)/3)
    groups = {
        "high": [],
        "medium": [],
        "low": []
    }

    max = methods[0].get_spec_count_spectra()

    part = max/3

    for method in methods:
        if method.get_spec_count_spectra() < part:
            groups['low'].append(method)
        elif method.get_spec_count_spectra() < (part*2):
            groups['medium'].append(method)
        else:
            groups['high'].append(method)

    return groups


def include_new_spec(spec):
    try:
        loaded_json = json.loads(spec.data)
        project_name = loaded_json['project']['name']
        project = Project.objects.filter(name=project_name)

        if len(project) > 0:
            project = project[0]
            print('Project already exists: ', project.name)
            it = Spec()
            it.key = loaded_json['key']
            it.project = project
            it.description = loaded_json['description']
            it.line = loaded_json['line']
            it.file = loaded_json['file']
            data = Spec.objects.filter(key=it.key)
            if len(data) > 0:
                print('Spec already exists.. updating it..')
                it.id = data[0].id
                it.key = data[0].key
            else:
                it.save()

            for method in loaded_json['executed_methods']:
                print(method['method_name'])
                # if is_new_method(method):
                #     print('New Method!')
                #     met = Method()
                #     met.method_name = method['method_name']
                #     met.class_name = method['class_name']
                #     met.class_path = method['class_path']
                #     met.save()
                #     it.executed_methods.add(met)
                # else:
                #     print('Method already exists!')
                met = Method.objects.filter(method_id=method['method_id'])
                print('Getting Method..')
                try:
                    if met[0]:
                        it.executed_methods.add(met[0])
                except IndexError:
                    print('New Method!')
                    met = Method()
                    met.method_name = method['method_name']
                    met.class_name = method['class_name']
                    met.class_path = method['class_path']
                    met.save()
                    it.executed_methods.add(met)
            print('Saving Spec!')
            it.save()
        else:
            print('Project not found!')

        return True
    except ValueError as e:
        return False
