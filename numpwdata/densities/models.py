"""Models for densities and interactions."""
import re
from socket import gethostname

from numpy import array

from django.db import models
from espressodb.base.models import Base

from numpwdata.utils.encoders import NympyEncoder
from numpwdata.utils.parsing import parse_fortran_funny
from numpwdata.files.models import H5File, DatFile

from numpwd.densities.base import Density as N_Density
from numpwd.densities.h5 import read_h5


class Interaction(Base):
    """Nuclear interaction."""


class Phenemenological(Interaction):
    """Phenemenological nuclear interaction."""

    name = models.CharField(max_length=200, help_text="Name of the interaction.")
    publication = models.TextField(
        null=True, blank=True, help_text="Publication associated with the interaction."
    )
    em_potential = models.BooleanField(
        help_text="Interaction includes electromagnetic potential."
    )
    three_nuc_force = models.CharField(
        max_length=200, help_text="Three-nucleon force used with interaction.",
    )
    misc = models.JSONField(
        help_text="Miscellaneous information about the interaction.",
        encoder=NympyEncoder,
    )

    class Meta:
        unique_together = [
            "name",
            "em_potential",
            "three_nuc_force",
        ]

    def __str__(self):
        return (
            f"Interaction("
            f"{self.name},"
            f" three_nuc_force={self.three_nuc_force}, em_potential={self.em_potential})"
        )


CHIRAL_ORDERS = [
    ("LO", "LO"),
    ("NLO", "NLO"),
    ("N2LO", "N2LO"),
    ("N3LO", "N3LO"),
    ("N4LO", "N4LO"),
    ("N4LO+", "N4LO+"),
]


class Chiral(Interaction):
    """Chiral nuclear interaction."""

    name = models.CharField(max_length=200, help_text="Name of the interaction.")
    order = models.CharField(
        max_length=10, help_text="Chiral order.", choices=CHIRAL_ORDERS
    )
    regulator = models.CharField(
        max_length=200,
        help_text="Regulator used in computation. See comment for cutoff type.",
    )
    em_potential = models.BooleanField(
        help_text="Interaction includes electromagnetic potential."
    )
    publication = models.TextField(
        null=True, blank=True, help_text="Publication associated with the interaction."
    )
    misc = models.JSONField(
        null=True,
        blank=True,
        help_text="Miscellaneous information about the interaction.",
        encoder=NympyEncoder,
    )

    class Meta:
        unique_together = [
            "name",
            "order",
            "regulator",
            "em_potential",
        ]

    def __str__(self):
        return (
            f"Interaction("
            f"{self.name}, {self.order},"
            f" regulator={self.regulator}, em_potential={self.em_potential})"
        )


class Density(Base):
    """Base implementation of density."""


class Density2N(Density):
    """Nucleus density used for two-nucleon matrix elements."""

    verbose_name = "Two nucleon density file"

    nucleus = models.CharField(max_length=10, help_text="Name of the nucleus.")
    n_nuc = models.PositiveIntegerField(
        help_text="Number of nucleons inside the nucleus."
    )
    interaction = models.ForeignKey(
        Interaction,
        on_delete=models.CASCADE,
        help_text="Interaction used to compute nucleus.",
    )
    qval = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        help_text="Value of momentum transfer in inverse fermi.",
    )
    thetaval = models.DecimalField(max_digits=5, decimal_places=2, help_text="?")
    momentum_info = models.JSONField(
        null=True,
        blank=True,
        help_text="Momentum mesh used for density representing the matrix.",
        encoder=NympyEncoder,
    )
    channel_info = models.JSONField(
        null=True,
        blank=True,
        help_text="Information about quantum channels.",
        encoder=NympyEncoder,
    )
    mesh_info = models.JSONField(
        null=True,
        blank=True,
        help_text=r"Internal mesh information used to obtain the density",
        encoder=NympyEncoder,
    )
    file = models.OneToOneField(
        H5File,
        on_delete=models.CASCADE,
        help_text="File information about density.",
        unique=True,
    )

    def read_h5(self, check_host: bool = True) -> N_Density:
        """Read the density from h5 File if existent."""
        if check_host and gethostname() != self.file.hostname:
            raise RuntimeError(
                "Operator stored on different host: {self.file.hostname}"
            )
        return read_h5(self.file.path)


class Density1N(Density):
    """Nucleus density used for one-nucleon matrix elements."""

    verbose_name = "Two nucleon density file"

    nucleus = models.CharField(max_length=10, help_text="Name of the nucleus.")
    n_nuc = models.PositiveIntegerField(
        help_text="Number of nucleons inside the nucleus."
    )
    interaction = models.ForeignKey(
        Interaction,
        on_delete=models.CASCADE,
        help_text="Interaction used to compute nucleus.",
    )
    qval = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        help_text="Value of momentum transfer in inverse fermi.",
    )
    thetaval = models.DecimalField(max_digits=5, decimal_places=2, help_text="?")
    momentum_info = models.JSONField(
        null=True,
        blank=True,
        help_text="Momentum mesh used for density representing the matrix.",
        encoder=NympyEncoder,
    )
    channel_info = models.JSONField(
        null=True,
        blank=True,
        help_text="Information about quantum channels.",
        encoder=NympyEncoder,
    )
    mesh_info = models.JSONField(
        null=True,
        blank=True,
        help_text=r"Internal mesh information used to obtain the density"
        ", e.g., in integrations.",
        encoder=NympyEncoder,
    )
    file = models.OneToOneField(
        DatFile, on_delete=models.CASCADE, help_text="File information about density.",
    )

    def read_dat(self, check_host: bool = True):
        """Read in one-body density files."""

        if check_host and gethostname() != self.file.hostname:
            raise RuntimeError(
                "Operator stored on different host: {self.file.hostname}"
            )

        pattern = r"MAXRHO1BINDEX\s+\=\s+(?P<max_rho_index>[0-9]+)"
        pattern += r".*"
        pattern += r"RHO1BINDX\s+\=(?P<rho_index>[0-9\*\,\-\s]+)"
        pattern += r".*"
        pattern += r"\/\s+(?P<om_theta>[0-9\.\-\+E ]+\n)"
        pattern += r"\s+(?P<rho>[0-9\.\-\+E\s]+\n)"

        dtypes = {
            "max_rho_index": int,
            "om_theta": lambda el: array([float(ee) for ee in el.split(" ") if ee]),
            "rho": lambda el: array([float(ee) for ee in el.split(" ") if ee]),
            "rho_index": parse_fortran_funny,
        }

        with open(self.file.path, "r") as inp:
            t = inp.read()
        dd = re.search(pattern, t, re.MULTILINE | re.DOTALL).groupdict()
        for key, val in dtypes.items():
            dd[key] = val(dd[key])

        channels = dd["rho_index"].copy()
        channels["rho"] = dd["rho"]
        dd["channels"] = channels
        return dd
