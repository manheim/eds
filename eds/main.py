
from __future__ import annotations
from eds.interfaces.worker import Worker
from eds.event import Event
from eds.extend import get_plugin
from eds.project import Project


def main(event: Event) -> None:
    """The main routine to process events.  Includes exception logging.

    Args:
        event (Event): The commit event to process.
    """
    try:
        process(event)
    except Exception:
        pass


def process(event: Event) -> None:
    """The main routine to process events.

    Args:
        event (Event): The commit event to process.
    """
    worker = get_plugin(Worker.interface_name, event.worker_plugin)
    if not event.eds_built:
        worker.build_eds(event.eds_version)
        return
    else:
        project = Project(event)
        if not event.eds_plugins_built:
            worker.build_eds(event.eds_version, project.plugin_versions)
            return
        for pipeline in project.pipelines:
            pipeline.build()
