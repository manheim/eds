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

    def generate(self) -> None:
        pass

class PipelinePlugin(BasePlugin, Pipeline):

    def generate(self) -> None:
        pass

class TagsPlugin(BasePlugin, Tags):

    def generate(self) -> None:
        pass

class TaskPlugin(BasePlugin, Task):

    def generate(self) -> None:
        pass

class VcsProviderPlugin(BasePlugin, VcsProvider):

    def generate(self) -> None:
        pass

class WorkerPlugin(BasePlugin, Worker):

    def generate(self) -> None:
        pass

def test_config_interface():
    c = ConfigPlugin({})
    assert isinstance(c, Config())

def test_pipeline_provider_interface():
    c = PipelineProviderPlugin({})
    assert isinstance(c, PipelineProvider())

def test_pipeline_interface():
    c = PipelinePlugin({})
    assert isinstance(c, Pipeline())

def test_tags_interface():
    c = TagsPlugin({})
    assert isinstance(c, Tags())

def test_task_interface():
    c = TaskPlugin({})
    assert isinstance(c, Task())

def test_vcs_provider_interface():
    c = VcsProviderPlugin({})
    assert isinstance(c, VcsProvider())

def test_worker_interface():
    c = WorkerPlugin({})
    assert isinstance(c, Worker())
