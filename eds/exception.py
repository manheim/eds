
class EdsError(Exception):
    """EDS base exception."""


class DuplicateIncludeError(Exception):
    """Raised when a duplicate include occurs."""


class PluginNameNotFoundError(EdsError):
    """Raised when a specific plugin is not found."""


class PluginNameMismatchError(EdsError):
    """Raised when a plugin name does not match the 'name' attribute of the object."""


class DuplicatePluginError(EdsError):
    """Raised when a specific name has multiple plugins."""


class NoPluginsFoundError(EdsError):
    """Raised when no template plugins are found."""


class PluginNoNameAttributeError(EdsError):
    """Raised when a plugin has no 'plugin_name' attribute."""
