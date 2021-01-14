"""File models."""
from socket import gethostname

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
