from eds.interfaces.plugin import Plugin


class VcsProvider(Plugin):

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.vcs_provider",
        "title": "VCS Provider",
        "type": "object",
        "properties": {}
    }

    def test_hook_event(self):
        pass

    def parse_hook_event(self):
        pass

    def get_project(self):
        pass

    def create_project(self):
        pass

    def delete_project(self):
        pass


class VcsProject():

    def checkout(self):
        pass

    def commit(self):
        pass

    def push(self):
        pass
