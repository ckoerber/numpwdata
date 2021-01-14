"""Operator models.

The logic of these files is to include the minimal amount of information to identify them
and leave the details unspecified (e.g., JSON format).
This should allow future changes.
"""

from django.db import models
from espressodb.base.models import Base

from numpwdata.utils.fields import SympyField
from numpwdata.files.models import H5File


class Operator(Base):
    """Base implementation of operators."""


class Operator2N(Operator):
    """Partial wave decomposed two-nucleon operator for external currents.

    The operators are presented in
    <a href="https://arxiv.org/abs/1704.01150">arxiv:1704.01150</a>.
    """

    name = models.CharField(max_length=100, help_text="Name of the operator.")
    equation = SympyField(
        encoder="expression",
        null=True,
        blank=True,
        help_text="Nuclear matrix element in relative momentum basis."
        r"$$\langle s_o m_{s_o} \bm p_{12 o} | s_i m_{s_i} \bm p_{12 i} \rangle$$ ",
    )
    args = models.JSONField(help_text="Information about the operator arguments")
    misc = models.JSONField(
        help_text="Miscellaneous information about the operator like quantum channels."
    )
    file = models.ForeignKey(
        H5File, on_delete=models.CASCADE, help_text="File information about operator.",
    )


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
        help_text="Nuclear matrix element in relative momentum basis."
        r"$$\langle s_o m_{s_o} \bm p_{12 o} | s_i m_{s_i} \bm p_{12 i} \rangle$$ ",
    )
    args = models.JSONField(help_text="Information about the operator arguments")
    misc = models.JSONField(
        help_text="Miscellaneous information about the operator like quantum channels."
    )
