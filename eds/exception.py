
class EdsError(Exception):
    """EDS base exception."""


class DuplicateIncludeError(Exception):
    """Raised when a duplicate include occurs."""


class PluginNameNotFoundError(EdsError):
    """Raised when a specific plugin is not found."""


class PluginNameMismatchError(EdsError):
    """Raised when a plugin name does not match the 'plugin_name' attribute of the object."""


class UnknownPluginIntefaceError(EdsError):
    """Raised when a plugin group or interface is unknown."""


class PluginInterfaceNotImplementedError(EdsError):
    """Raised when a plugin does not implement the expected interface."""


class DuplicatePluginError(EdsError):
    """Raised when a specific name has multiple plugins."""


class NoPluginsFoundError(EdsError):
    """Raised when no template plugins are found."""


class PluginNoNameAttributeError(EdsError):
    """Raised when a plugin has no 'plugin_name' attribute."""
