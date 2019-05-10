from app.models import Method, Feature, Spec


def get_methods_without_features(project):
    methods = Method.objects.filter(project=project)

    f_executed = []
    f_not_executed = []
    t_executed = []
    t_not_executed = []
    for method in methods:
        if method.impacted_features == 0:
            f_not_executed.append(method.id)
        else:
            f_executed.append(method.id)
        if method.number_of_tests == 0:
            t_not_executed.append(method.id)
        else:
            t_executed.append(method.id)

    result = {"f_executed": f_executed,
              "f_not_executed": f_not_executed,
              "t_executed": t_executed,
              "t_not_executed": t_not_executed,
              "number_methods": len(methods)
              }

    return result


def get_all_tested_methods(project):
    methods = Method.objects.filter(project=project)

    executed = []
    not_executed = []
    for method in methods:
        if method.number_of_tests == 0:
            executed.append(method.id)
        else:
            not_executed.append(method.id)

    result = {"executed": executed,
              "not_executed": not_executed}

    return result


def get_features_without_methods(id):
    features = Feature.objects.filter(project=id)

    features_without_methods = set()

    # feature without methods
    flag = 0

    for feature in features:
        for scenario in feature.simple_scenarios.all():
            if len(scenario.executed_methods.all()) > 0:
                flag = 1
        if flag == 0:
            features_without_methods.add(feature)
    return features_without_methods


def distribute_importance_group(methods):
    groups = {
        "low": [],
        "medium": [],
        "high": []
    }

    for method in methods:
        if method.get_probability() < 30:
            groups['low'].append(method)
        elif method.get_probability() < 70:
            groups['medium'].append(method)
        else:
            groups['high'].append(method)

    return groups


def number_tests_by_group(groups):
    result = {
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for method in groups['high']:
        result['high'] += method.get_spec_count_spectra()

    for method in groups['medium']:
        result['medium'] += method.get_spec_count_spectra()

    for method in groups['low']:
        result['low'] += method.get_spec_count_spectra()

    if len(groups['high']) > 0:
        result['high'] = result['high']/len(groups['high'])
    else:
        result['high'] = 0
    if len(groups['medium']) > 0:
        result['medium'] = result['medium'] / len(groups['medium'])
    else:
        result['medium'] = 0
    if len(groups['low']) > 0:
        result['low'] = result['low'] / len(groups['low'])
    else:
        result['low'] = 0

    return result


def get_folders_tested(id):
    methods = Method.objects.filter(project=id)
    folders_bdds = {}
    folders_specs = {}
    folders = {}
    each = {"folder": "", "bdds": 0, "specs": 0}
    result = []
    for method in methods:
        folders[method.folder] = set()
        folders[method.folder] = set()
    for method in methods:
        folders[method.folder].add(method)
        folders[method.folder].add(method)

    print('Número de Folders: ', len(folders))

    for key in folders:
        specs_folder = 0
        folders_specs[key] = 0
        for method in folders[key]:
            specs = method.specs.all()
            specs_folder += len(specs)
        folders_specs[key] += specs_folder

    print('Número de Folders testados: ', len(folders_specs))

    total = 0
    for key in folders_specs:
        print(key, ': ', folders_specs[key])
        total += folders_specs[key]
    # print('Folders: ', folders_specs)
    print('Total: ', total)
    return result
