import os


class Paths:
    def __init__(self):
        self.path_separator = os.path.sep
        self.path_project = os.path.abspath(os.path.join(os.path.dirname(__file__), f"..{self.path_separator}.."))
        self.datas = "Datas"
        self.reports = "Reports"
        self.drivers = "Drivers"
        self.libraries = "Libraries"
        self.datas_compare_image = "Image_Compare"

    def get_path_project(self):
        return self.path_project

    def get_path_drivers(self):
        return os.path.join(self.path_project, self.drivers)

    def get_path_libraries(self):
        return os.path.join(self.path_project, self.libraries)

    def get_path_datas(self):
        return os.path.join(self.path_project, self.datas)

    def get_path_reports(self):
        return os.path.join(self.path_project, self.reports)

    def get_path_compare_image(self):
        return os.path.join(self.get_path_datas(), self.datas_compare_image)


if __name__ == "__main__":
    paths = Paths()
    print(paths.get_path_datas())
