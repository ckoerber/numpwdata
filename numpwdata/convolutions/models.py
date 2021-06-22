"""Models of convolutions."""

from django.db import models
from espressodb.base.models import Base

from numpwdata.densities.models import Density
from numpwdata.operators.models import OperatorPWD


class CurrentConvolution(Base):
    """Convolution of operator and density."""

    operator = models.ForeignKey(
        OperatorPWD,
        on_delete=models.CASCADE,
        help_text="Operator used in computation.",
    )
    density = models.ForeignKey(
        Density, on_delete=models.CASCADE, help_text="Density used in computation.",
    )
    q = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        help_text="Momentum transfer from operator to density.",
    )
    angle = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Scattering angle of initial to final scattering momentum in degerees.",
    )
    mj_tot_i_x2 = models.IntegerField(
        help_text="Incoming total spin polarization of nucleus.", null=True, blank=True
    )
    mj_tot_o_x2 = models.IntegerField(
        help_text="Outgoing total spin polarization of nucleus.", null=True, blank=True
    )
    value = models.FloatField(help_text="Value of the matrix element.")
    value_imag = models.FloatField(
        null=True, blank=True, help_text="Imaginary value of the matrix element."
    )

    date = models.DateTimeField(auto_now=True, help_text="Date last modified.")

    class Meta:
        unique_together = [
            "operator",
            "density",
            "q",
            "angle",
            "mj_tot_i_x2",
            "mj_tot_o_x2",
        ]
