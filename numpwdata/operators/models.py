"""Operator models.

The logic of these files is to include the minimal amount of information to identify them
and leave the details unspecified (e.g., JSON format).
This should allow future changes.
"""
from socket import gethostname

from django.db import models
from espressodb.base.models import Base

from numpwd.operators import Operator as N_Operator
from numpwd.operators.h5 import read

from numpwdata.utils.fields import SympyField
from numpwdata.utils.encoders import NympyEncoder
from numpwdata.files.models import H5File


class Operator(Base):
    """Base implementation of operators."""


class Operator2N(Operator):
    """Equation representing a two-nucleon operator."""

    name = models.CharField(
        max_length=100, help_text="Name of the operator.", unique=True
    )
    equation = SympyField(
        encoder="expression",
        null=True,
        blank=True,
        help_text="Describes the operator as a function of in- and outgoing"
        " nucleon momenta and Pauli spin and isospin matrices"
        " as well as external current information.",
        unique=True,
    )
    legend = models.JSONField(
        null=True,
        blank=True,
        help_text="A dictinoary explaining the definitions.",
        encoder=NympyEncoder,
    )


class OperatorPWD(Base):
    """Base implementation of operator partial wave decompositions."""


class Operator2NPWD(OperatorPWD):
    """Partial wave decomposed two-nucleon operator for external currents pointing to a file.

    The operators are presented in
    <a href="https://arxiv.org/abs/1704.01150">arxiv:1704.01150</a>.
    """

    operator = models.ForeignKey(
        Operator2N,
        on_delete=models.CASCADE,
        help_text="Expression which identifies the operator.",
    )
    args = models.JSONField(
        null=True,
        blank=True,
        help_text="Information about the operator arguments",
        encoder=NympyEncoder,
    )
    misc = models.JSONField(
        null=True,
        blank=True,
        help_text="Miscellaneous information about the operator like quantum channels.",
        encoder=NympyEncoder,
    )
    mesh_info = models.JSONField(
        null=True,
        blank=True,
        help_text="Information about the operator integration meshes.",
        encoder=NympyEncoder,
    )
    file = models.OneToOneField(
        H5File, on_delete=models.CASCADE, help_text="File information about operator.",
    )

    class Meta:
        unique_together = ["operator", "file"]

    def read_h5(self) -> N_Operator:
        """Read the operator from h5 File if existent."""
        if gethostname() != self.file.hostname:
            raise RuntimeError(
                "Operator stored on different host: {self.file.hostname}"
            )
        return read(self.file.path)

    def __str__(self):
        return f"Operator2NPWD({self.operator.name}, {self.file.path})"


class Operator1N(Operator):
    """Partial wave decomposed one-nucleon operator for external currents.

    The operators are presented in
    <a href="https://arxiv.org/abs/1704.01150">arxiv:1704.01150</a>.
    """

    name = models.CharField(max_length=100, help_text="Name of the operator.")
    equation = SympyField(
        encoder="expression",
        null=True,
        blank=True,
        help_text="Describes the operator as a function of in- and outgoing"
        " nucleon momenta and Pauli spin and isospin matrices"
        " as well as external current information.",
    )
    legend = models.JSONField(
        null=True,
        blank=True,
        help_text="A dictinoary explaining the definitions.",
        encoder=NympyEncoder,
    )
