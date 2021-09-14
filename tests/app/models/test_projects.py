import pytest

from app.models import Project


class TestProjectInstance:
  @pytest.fixture
  def project(self):
    '''Returns a Project with empty or blank attributes'''
    project = Project()
    project.name = 'Exemplo'
    project.description = 'Descrição exemplo'
    project.language = 'Ruby on Rails'
    project.repository = 'git url'

    return project

  @pytest.mark.django_db
  def test_project_creation(self, project):
    project.save()

    assert Project.objects.count() == 1

  @pytest.mark.django_db
  def test_project_str(self, project):

    assert project.__str__() == 'Exemplo'
