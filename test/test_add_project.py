# -*- coding: utf-8 -*-
from model.project import Project


def test_add_project(app, data_projects):
    project = data_projects
    projects_before = app.soap.get_project_list()
    app.project.add_project(project)
    projects_before.append(project)
    projects_after = app.soap.get_project_list()
    assert sorted(projects_before, key=Project.id_or_max) == sorted(projects_after, key=Project.id_or_max)
