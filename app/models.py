from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from abc import abstractmethod
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=30, blank=True, null=True)
    repository = models.CharField(max_length=200, blank=True, null=True)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.name

    objects = models.Manager()


class Feature(models.Model):

    path_name = models.CharField(max_length=200, blank=True, null=True)
    feature_name = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    user_story = models.CharField(max_length=300, blank=True, null=True)
    background = models.CharField(max_length=300, blank=True, null=True)
    probability = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100)], blank=True,
                                    null=True, default=0)
    project = models.ForeignKey('app.Project', verbose_name='Project', blank=True, related_name='features',
                                on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.feature_name

    def obj_dict(self):
        return self.__dict__

    objects = models.Manager()


class Scenario(models.Model):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def set_line(self):
        pass

    class Meta:
        abstract = True


class SimpleScenario(Scenario):

    feature = models.ForeignKey('app.Feature', verbose_name='Feature', blank=True, related_name='simple_scenarios',
                                on_delete=models.CASCADE)

    scenario_title = models.CharField(max_length=200, blank=True, null=True)
    line = models.IntegerField()
    executed_methods = models.ManyToManyField('app.Method', verbose_name='Metodos', blank=True,
                                              related_name='scenarios')
    probability = models.FloatField('Probabilidade', validators=[MinValueValidator(0.1), MaxValueValidator(100)],
                                    blank=True, null=True, default=0)

    def execute(self):
        pass

    def set_line(self):
        pass

    def __str__(self):
        return self.scenario_title

    objects = models.Manager()


class ScenarioOutline(Scenario):

    feature = models.ForeignKey('app.Feature', verbose_name='Feature', blank=True, related_name='outline_scenarios',
                                on_delete=models.CASCADE)

    scenario_title = models.CharField(max_length=200, blank=True, null=True)
    line = models.IntegerField()
    examples = ArrayField(
        models.CharField(max_length=200, blank=True, null=True))

    # scenario_iterations = ArrayField(
    #     models.CharField(max_length=200, blank=True, null=True))


    # def __init__(self):
    #     self.steps = []
    #     self.scenario_title = ""
    #     self.line = None
    #     self.examples = []
    #     self.scenario_iterations = []

    def execute(self):
        pass

    def set_line(self):
        pass

    def add(self):
        pass

    def remove(self):
        pass

    def execute(self):
        pass

    objects = models.Manager()


class Step(models.Model):
    key_word = models.CharField(max_length=15)
    phrase = models.CharField(max_length=150)
    scenario = models.ForeignKey('app.SimpleScenario', verbose_name='Cenário', related_name='steps',
                                 on_delete=models.CASCADE)

    objects = models.Manager()


class Method(models.Model):
    method_name = models.CharField(max_length=100, blank=True, null=True)
    method_id = models.CharField(max_length=300, blank=False, null=False)
    class_name = models.CharField(max_length=200, blank=True, null=True)
    class_path = models.CharField(max_length=200, blank=True, null=True)
    abc_score = models.FloatField(blank=True, null=True, default=0)

    probability = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100)], blank=True, null=True,
                                    default=0)
    project = models.ForeignKey('app.Project', verbose_name='Project', blank=True, related_name='methods',
                                on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.method_name

    def get_probability(self):
        self.probability = 0
        for scenario in self.scenarios.all():
            self.probability += scenario.probability

        return self.probability

    def get_count_spectra(self):
        return len(self.scenarios.all())

    def get_spec_count_spectra(self):
        return len(self.specs.all())

    objects = models.Manager()


class Spec(models.Model):
    project = models.ForeignKey('app.Project', verbose_name='Project', blank=True, related_name='specs',
                                on_delete=models.CASCADE, null=True)
    key = models.CharField(max_length=300, blank=True, null=True)
    file = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    line = models.IntegerField()
    executed_methods = models.ManyToManyField('app.Method', verbose_name='Metodos', blank=True,
                                              related_name='specs')

    def __str__(self):
        return self.description

    def obj_dict(self):
        return self.__dict__

    objects = models.Manager()
