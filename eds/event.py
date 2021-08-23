
from __future__ import annotations
import os

from eds.interfaces.vcs_provider import VcsProvider
from typing import Dict


class Event():
    """A commit event for a project."""

    def __init__(self, eds_built: bool, eds_plugins_built: bool, url: str, project_name: str,
                 project_version: str):
        """Event constructor.

        Args:
            eds_built (bool): Whether EDS is already built.
            eds_plugins_built (bool): Whether EDS is already built with plugins.
            url (str): Project ref URL.
            project_name (str): Project name.
            project_version (str): Project version.
        """
        # todo:
        #   these *_built values need to be determined by the worker
        #   will be implemented in a forthcoming BaseWorker class.
        self._eds_built = eds_built
        self._eds_plugins_built = eds_plugins_built

        self._url = url
        self._project_name = project_name
        self._project_version = project_version
        self._vcs_provider = self._get_vcs_provider()
        self._eds_yaml = self._get_eds_yaml()

    def _get_vcs_provider(self) -> VcsProvider:
        """Get the VCS provider based on the event.

        Returns:
            VcsProvider: The VCS provider class.
        """
        pass

    def _get_eds_yaml(self) -> Dict:
        """Get the yaml from 'eds.yml'.

        Returns:
            Dict: The yaml from 'eds.yml'.
        """
        pass

    @classmethod
    def init_from_webhook(cls, eds_built: bool, eds_plugins_built: bool, webhook_data: str) -> Event:
        """Init Event from webhook data.

        Args:
            eds_built (bool): Whether EDS is already built.
            eds_plugins_built (bool): Whether EDS is already built with plugins.
            webhook_data (str): Webhook data.

        Returns:
            Event: The constructed Event.
        """
        pass

    @classmethod
    def init_from_include(cls, url: str, event: Event) -> Event:
        """Init Event for parent 'eds.yml' projects.

        Args:
            url (str): Project ref url.
            event (Event)): Original Event.

        Returns:
            Event: The constructed Event.
        """
        return Event(event.eds_built, event.eds_plugins_built, url,
                     event.project_name, event.project_version)

    @classmethod
    def init_from_local(cls) -> Event:
        """Init Event for a local execution of 'eds'.

        Returns:
            Event: The constructed Event.
        """
        cwd = os.getcwd()
        project = os.path.basename(cwd)
        return Event(True, True, cwd, project, '.')

    @property
    def eds_built(self) -> bool:
        """Whether EDS is already built.

        Returns:
            bool: Whether EDS is already built.
        """
        return self._eds_built

    @property
    def eds_plugins_built(self) -> bool:
        """Whether EDS is already built with plugins.

        Returns:
            bool: Whether EDS is already built with plugins.
        """
        return self._eds_plugins_built

    @property
    def url(self) -> str:
        """Project ref URL.

        Returns:
            str: Project ref URL.
        """
        return self._url

    @property
    def eds_yaml(self) -> Dict:
        """Yaml from 'eds.yml'.

        Returns:
            Dict: Yaml from 'eds.yml'
        """
        return self._eds_yaml

    @property
    def eds_version(self) -> str:
        """EDS version.

        Returns:
            str: EDS version.
        """
        return self._eds_yaml['version']

    @property
    def project_name(self) -> str:
        """Project name.

        Returns:
            str: Project name.
        """
        return self._project_name

    @property
    def project_version(self) -> str:
        """Project version.

        Returns:
            str: Project version.
        """
        return self._project_version
