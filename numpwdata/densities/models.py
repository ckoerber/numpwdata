"""Models for densities and interactions."""

from django.db import models
from espressodb.base.models import Base
from numpwdata.files.models import H5File, DatFile


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
        help_text="Miscellaneous information about the interaction."
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

    name = models.CharField(
        max_length=200, help_text="Name of the interaction.", unique=True
    )
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
        help_text="Miscellaneous information about the interaction."
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
        decimal_places=4,
        help_text="Value of momentum transfer in inverse fermi.",
    )
    thetaval = models.DecimalField(max_digits=8, decimal_places=4, help_text="?")
    momentum_info = models.JSONField(
        help_text="Momentum mesh used for density representing the matrix.",
    )
    channel_info = models.JSONField(help_text="Information about quantum channels.")
    mesh_info = models.JSONField(
        help_text=r"Internal mesh information used to obtain the density"
    )
    file = models.OneToOneField(
        H5File,
        on_delete=models.CASCADE,
        help_text="File information about density.",
        unique=True,
    )


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
        decimal_places=4,
        help_text="Value of momentum transfer in inverse fermi.",
    )
    thetaval = models.DecimalField(max_digits=8, decimal_places=4, help_text="?")
    momentum_info = models.JSONField(
        help_text="Momentum mesh used for density representing the matrix.",
    )
    channel_info = models.JSONField(help_text="Information about quantum channels.")
    mesh_info = models.JSONField(
        help_text=r"Internal mesh information used to obtain the density"
        ", e.g., in integrations.",
    )
    file = models.OneToOneField(
        DatFile, on_delete=models.CASCADE, help_text="File information about density.",
    )
