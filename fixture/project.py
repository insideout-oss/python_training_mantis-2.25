from model.project import Project
from selenium.webdriver.support.select import Select


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_my_view_page(self):
        wd = self.app.wd
        if not(wd.current_url.endswith("/my_view_page.php")):
            wd.get(self.app.base_url + "/my_view_page.php")

    def select_sidebar(self):
        wd = self.app.wd
        base_url = self.app.base_url.split("/")[3]
        wd.find_element_by_xpath("//a[@href='/%s/manage_overview_page.php']" % base_url).click()

    def select_manage_projects(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Manage Projects").click()

    def press_create_new_project(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//button[@type='submit']").click()

    def change_select_value(self, field_name, value):
        wd = self.app.wd
        if value is not None:
            wd.find_element_by_name(field_name).click()
            Select(wd.find_element_by_name(field_name)).select_by_visible_text(value)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def fill_project_info(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_select_value("status", project.status)
        if project.enabled:
            wd.find_element_by_xpath(
                "//form[@id='manage-project-create-form']/div/div[2]/div/div/table/tbody/tr[3]/td[2]/label/span").click()
        self.change_select_value("view_state", project.view_status)
        self.change_field_value("description", project.description)

    def submit_submit(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Add Project']").click()

    def open_project_page_by_id(self, project_id):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[@href='manage_proj_edit_page.php?project_id=%s']" % str(project_id)).click()

    def submit_delete(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()

    def open_manage_projects_page(self):
        self.open_my_view_page()
        self.select_sidebar()
        self.select_manage_projects()

    def add_project(self, project):
        self.open_manage_projects_page()
        self.press_create_new_project()
        self.fill_project_info(project)
        self.submit_submit()
        self.select_manage_projects()
        self.project_cache = None

    def delete_project_by_id(self, project):
        self.open_manage_projects_page()
        self.open_project_page_by_id(project.id)
        self.submit_delete()
        self.project_cache = None

    project_cache = None

    def count(self):
        wd = self.app.wd
        self.open_manage_projects_page()
        tables = wd.find_elements_by_class_name("table-responsive")
        num = len(tables[0].find_elements_by_css_selector("tbody tr"))
        return len(tables[0].find_elements_by_css_selector("tbody tr"))

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_manage_projects_page()
            self.project_cache = []
            tables = wd.find_elements_by_css_selector(".table-responsive")
            for row in tables[0].find_elements_by_css_selector("tbody tr"):
                elem = row.find_elements_by_tag_name("td")
                if len(elem) > 0:
                    href = row.find_element_by_css_selector("a").get_attribute("href")
                    project_id = str(href).split('=')[1]
                    project = Project(name=elem[0].text, status=elem[1].text,
                                      enabled=elem[2].text, view_status=elem[3].text,
                                      description=elem[4].text, id=project_id)
                    self.project_cache.append(project)
        return list(self.project_cache)
