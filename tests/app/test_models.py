import pytest

from app.models import Project


@pytest.mark.django_db
def test_project_create():
  project = Project()
  project.name = 'Exemplo'
  project.description = 'Descrição exemplo'
  project.language = 'Ruby on Rails'
  project.repository = 'git url'

  project.save()

  assert Project.objects.count() == 1
