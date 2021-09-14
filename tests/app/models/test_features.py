import pytest

from app.models import Project, Feature


class TestFeatureInstance:
  @pytest.fixture
  def project(self):
    '''Returns a Project'''
    project = Project()
    project.name = 'Exemplo'
    project.description = 'Descrição exemplo'
    project.language = 'Ruby on Rails'
    project.repository = 'git url'
    project.save()

    return project

  @pytest.fixture
  def feature(self, project):
    '''Returns a Feature'''
    feature = Feature()
    feature.path_name = 'home/projects/example'
    feature.feature_name = 'Aspect navigation on the left menu'
    feature.language = 'Ruby on Rails'
    feature.user_story = 'First story'
    feature.background = 'Background example'
    feature.probability = 75.0
    feature.project = project

    return feature

  @pytest.mark.django_db
  def test_feature_creation(self, feature):
    feature.save()

    assert Feature.objects.count() == 1

  @pytest.mark.django_db
  def test_feature_creation_of_project(self, project, feature):
    feature.save()

    assert project.features.filter(pk=feature.pk).exists()

  @pytest.mark.django_db
  def test_project_str(self, feature):

    assert feature.__str__() == 'Aspect navigation on the left menu'

  @pytest.mark.django_db
  def test_project_obj_dict(self, feature):

    assert feature.obj_dict() == feature.__dict__
