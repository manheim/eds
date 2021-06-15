from eds.interfaces.plugin import Plugin


class Task(Plugin):
    """eds.task interface."""

    interface_name = "eds.task"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.task",
        "title": "Task",
        "type": "object",
        "properties": {}
    }
