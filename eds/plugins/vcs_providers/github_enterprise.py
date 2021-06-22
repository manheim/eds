from typing import Dict

from eds.interfaces.vcs_provider import VcsProvider


class GithubEnterpriseProvider(VcsProvider):
    
    @property
    def children(self) -> List[Plugin]:
        """The list of child plugins.

        Returns:
            List[Plugin]: The list of child plugins.
        """
        return []

    def validate(self) -> None:
        """Validate the plugin."""
        pass

    def parse_event(self) -> Dict:
        return super().parse_event()

    def get_files(self) -> Dict:
        return super().get_files()

    def create_project(self) -> None:
        return super().create_project()

    def delete_project(self) -> None:
        return super().delete_project()

    def update_project(self) -> None:
        return super().update_project()

VcsProvider.register(GithubEnterpriseProvider)
