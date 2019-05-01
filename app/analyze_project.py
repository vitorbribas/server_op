from app.models import Method, Feature, Spec


def get_methods_without_features(project):
    methods = Method.objects.filter(project=project)
    features = Feature.objects.filter(project=project)

    executed = []
    for feature in features.all():
        for scenario in feature.simple_scenarios.all():
            for met in scenario.executed_methods.all():
                executed.append(met.id)

    executed = set(executed)
    print('Executed:', executed)
    not_executed = set()

    for method in methods.all():
        if method.id not in executed:
            not_executed.add(method.id)

    result = {"executed": executed,
              "not_executed": not_executed}

    return result


def get_all_tested_methods(project):
    methods = Method.objects.filter(project=project)
    specs = Spec.objects.filter(project=project)

    executed = set()
    for spec in specs:
        for met in spec.executed_methods.all():
            executed.add(met.method_id)

    not_executed = []

    for method in methods:
        if method.method_id not in executed:
            not_executed.append(method.method_id)

    result = {"executed": executed,
              "not_executed": not_executed}

    # print(result)
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
