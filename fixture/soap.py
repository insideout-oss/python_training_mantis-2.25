from suds.client import  Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def create_clien(self):
        base_url = self.app.base_url.split("/")[3]
        return Client("http://localhost/%s/api/soap/mantisconnect.php?wsdl" % base_url)

    def can_login(self, username, password):
        client = self.create_clien()
        try:
            client.service.mc_login
            return True
        except WebFault:
            return False

    def get_project_list(self):
        project_list = []
        client = self.create_clien()
        projects = client.service.mc_projects_get_user_accessible(self.app.config['webadmin']['username'],
                                                                      self.app.config['webadmin']['password'])
        for project in projects:
            project_list.append(Project(name=project.name, status=project.status, enabled=project.enabled,
                                        view_status=project.view_state, description=project.description,
                                        id=project.id))
        return project_list
