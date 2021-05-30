from eds.event import Event
from eds.main import main


def cli():
    main(Event.init_from_local())
