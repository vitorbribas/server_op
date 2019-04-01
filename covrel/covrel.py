from app.models import Project, Method, Feature


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
    methods.sort(key=lambda x: x.get_count_spectra(), reverse=True)

    part = int(len(methods)/3)

    groups = {
        "high": methods[:part],
        "medium": methods[part:(part+part)],
        "low": methods[(part+part):]
    }
    return groups
