from django.contrib import admin

from app.models import Feature, ScenarioOutline, SimpleScenario, Method, Step, Project

admin.site.register(Feature)
admin.site.register(ScenarioOutline)
admin.site.register(SimpleScenario)
admin.site.register(Method)
admin.site.register(Step)
admin.site.register(Project)


