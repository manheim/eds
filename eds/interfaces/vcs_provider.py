from eds.interfaces.plugin import Plugin


class VcsProvider(Plugin):

    interface_name = "eds.vcs_provider"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.vcs_provider",
        "title": "VCS Provider",
        "type": "object",
        "properties": {}
    }

    def parse_webhook_event(self):
        pass

    def create_project(self):
        pass

    def delete_project(self):
        pass

    def get_project(self):
        pass
