from eds.exception import EdsError
from eds.interfaces.worker import Worker
from eds.plugin import get_plugin
from eds.project import Project


def main(event):
    try:
        process(event)
    except EdsError:
        pass


def process(event):
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
