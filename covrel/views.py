from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from covrel.covrel import group_methods, include_new_spec


def covrel(request, id):
    methods = group_methods(id)
    context = {
        "methods": methods
    }
    return render(request, 'covrel_groups.html', context)


@api_view(["POST"])
def update_spectrum(spec):

    result = include_new_spec(spec)
    return Response(result)
