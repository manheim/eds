"""eds.cli module."""

from eds.event import Event
from eds.main import main


def cli() -> None:
    """CLI entry point to main."""
    main(Event.init_from_local())
