"""File models."""
from socket import gethostname
from importlib import import_module

from django.db import models
from espressodb.base.models import Base


class File(Base):
    """File storage infromation."""


class H5File(File):
    """File storage infromation for HDF5 files."""

    path = models.TextField(help_text="File path address to the HDF5 file.")
    h5_path = models.TextField(
        default="/", help_text="Group path address within the HDF5 file."
    )
    hostname = models.TextField(
        default=gethostname, help_text="Name of the (remote) host of the file."
    )

    class Meta:
        unique_together = [
            "path",
            "h5_path",
            "hostname",
        ]


class DatFile(File):
    """File storage infromation for dat files."""

    path = models.TextField(help_text="File path address to the HDF5 file.")
    hostname = models.TextField(
        default=gethostname, help_text="Name of the (remote) host of the file."
    )

    class Meta:
        unique_together = [
            "path",
            "hostname",
        ]


class ModuleFunction(File):
    """Function inside a Python module."""

    module_name = models.TextField(help_text="Python module import name (using '.')")
    function_name = models.TextField(
        help_text="Name of the function inside the module."
    )
    version = models.TextField(
        null=True,
        blank=True,
        help_text="Tag defining the version of the function used."
        " Not yet used on import",
    )

    def __init__(self, *args, **kwargs):
        """Add empty _fcn attribute."""
        super().__init__(*args, **kwargs)
        self._fcn = None

    @property
    def function(self):
        """Import the function from module."""
        if self._fcn is None:
            module = import_module(self.module_name)
            self._fcn = getattr(module, self.function_name)
        return self._fcn

    def call(self, *args, **kwargs):
        """Call the linked function."""
        return self.function(*args, **kwargs)

    def __str__(self):
        """Return name as a python import string."""
        version = f" @{self.version}" if self.version else ""
        return f"{self.module_name}.{self.function_name}{version}"
