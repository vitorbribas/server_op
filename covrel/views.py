from django.shortcuts import render

from covrel.covrel import group_methods


def covrel(request, id):
    methods = group_methods(id)
    context = {
        "methods": methods
    }
    return render(request, 'covrel_groups.html', context)
