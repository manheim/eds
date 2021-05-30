import os


class Event():

    def __init__(self, eds_built, eds_plugins_built, url, project_name,
                 project_version):
        self._eds_built = eds_built
        self._eds_plugins_built = eds_plugins_built
        self._url = url
        self._project_name = project_name
        self._project_version = project_version
        self._vcs_provider = self._get_vcs_provider()
        self._eds_yaml = self._get_eds_yaml()

    def _get_vcs_provider(self):
        pass

    def _get_eds_yaml(self):
        pass

    ##############

    @classmethod
    def init_from_webhook(cls, eds_built, eds_plugins_built, webhook_data):
        pass

    @classmethod
    def init_from_include(cls, url, event):
        return Event(event.eds_built, event.eds_plugins_built, url,
                     event.project_name, event.project_version)

    @classmethod
    def init_from_local(cls):
        cwd = os.getcwd()
        project = os.path.basename(cwd)
        return Event(True, True, cwd, project, '.')

    ##############

    @property
    def eds_built(self):
        return self._eds_built

    @property
    def eds_plugins_built(self):
        return self._eds_plugins_built

    @property
    def eds_yaml(self):
        return self._eds_built

    @property
    def eds_version(self):
        return self._eds_yaml['version']

    @property
    def project_name(self):
        return self._project_name

    @property
    def project_version(self):
        return self._project_version
