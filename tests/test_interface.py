from typing import Dict
from eds.plugin import BasePlugin
from eds.interfaces.config import Config
from eds.interfaces.pipeline_provider import PipelineProvider
from eds.interfaces.pipeline import Pipeline
from eds.interfaces.tags import Tags
from eds.interfaces.task import Task
from eds.interfaces.vcs_provider import VcsProvider
from eds.interfaces.worker import Worker

class ConfigPlugin(BasePlugin, Config):

    def generate(self) -> None:
        pass

class PipelineProviderPlugin(BasePlugin, PipelineProvider):

    def create_pipeline(self) -> None:
        pass

    def update_pipeline(self) -> None:
        pass

    def delete_pipeline(self) -> None:
        pass

class PipelinePlugin(BasePlugin, Pipeline):

    def build(self) -> None:
        pass

class TagsPlugin(BasePlugin, Tags):

    def generate(self) -> None:
        pass

class TaskPlugin(BasePlugin, Task):

    def generate(self) -> None:
        pass

class VcsProviderPlugin(BasePlugin, VcsProvider):

    def parse_event(self) -> None:
        pass

    def get_files(self) -> Dict:
        pass

    def create_project(self) -> None:
        pass

    def delete_project(self) -> None:
        pass

    def update_project(self) -> None:
        pass

class WorkerPlugin(BasePlugin, Worker):

    def build_eds(self) -> None:
        pass


def test_config_interface():
    plugin = ConfigPlugin({})

def test_pipeline_provider_interface():
    plugin = PipelineProviderPlugin({})

def test_pipeline_interface():
    plugin = PipelinePlugin({})

def test_tags_interface():
    plugin = TagsPlugin({})

def test_task_interface():
    plugin = TaskPlugin({})

def test_vcs_provider_interface():
    plugin = VcsProviderPlugin({})

def test_worker_interface():
    plugin = WorkerPlugin({})
