# -*- coding: utf-8 -*-
import random

from model.project import Project


def test_add_project(app):
    if app.project.count() == 0:
        app.project.add_project(name="First-project-1234567899090", description="f p description")
    projects_before = app.project.get_project_list()
    project = random.choice(projects_before)
    print(project)
    app.project.delete_project_by_id(project)
    assert len(projects_before) - 1 == app.project.count()
    projects_after = app.project.get_project_list()
    projects_before.remove(project)
    assert sorted(projects_before, key=Project.id_or_max) == sorted(projects_after, key=Project.id_or_max)
