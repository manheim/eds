from eds.interfaces.plugin_interface import PluginInterface


class Task(PluginInterface):
    """eds.task interface."""

    interface_name = "eds.task"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.task",
        "title": "Task",
        "type": "object",
        "properties": {}
    }

Task.register(PluginInterface)
assert issubclass(PluginInterface, Task)
