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
    legend = models.JSONField(help_text="A dictinoary explaining the definitions.")


class Operator2NPWD(Base):
    """Partial wave decomposed two-nucleon operator for external currents pointing to a file.

    The operators are presented in
    <a href="https://arxiv.org/abs/1704.01150">arxiv:1704.01150</a>.
    """

    operator = models.ForeignKey(
        Operator2N,
        on_delete=models.CASCADE,
        help_text="Expression which identifies the operator.",
    )
    args = models.JSONField(help_text="Information about the operator arguments")
    l12_max = models.IntegerField()
    s12_max = models.IntegerField()
    misc = models.JSONField(
        help_text="Miscellaneous information about the operator like quantum channels."
    )
    file = models.ForeignKey(
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
    legend = models.JSONField(help_text="A dictinoary explaining the definitions.")
