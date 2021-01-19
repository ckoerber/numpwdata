"""Utility functions for current convolutions."""
from typing import Optional, Dict, Any
import pandas as pd

from numpwdata.operators.models import Operator2NPWD, Operator1NPWD
from numpwdata.densities.models import Density2N, Density1N
from numpwdata.convolutions.models import CurrentConvolution


def get_convolution_frame(
    convolution_filter_kwargs: Optional[Dict[str, Any]] = None,
    density_filter_kwargs: Optional[Dict[str, Any]] = None,
    operator_filter_kwargs: Optional[Dict[str, Any]] = None,
    density_fields: Optional[Dict[str, Any]] = None,
    operator_fields: Optional[Dict[str, Any]] = None,
):
    """Find all convolutions for filters and join them with density/operator data."""
    convolution_fields = ["operator__id", "density__id", "q", "value"]
    convolution_filter_kwargs = convolution_filter_kwargs or dict()
    convolutions = CurrentConvolution.objects.filter(
        **convolution_filter_kwargs
    ).to_dataframe(fieldnames=convolution_fields)

    density_fields = density_fields or dict()
    density_filter_kwargs = density_filter_kwargs or dict()
    dens_fields = ["id"] + list(density_fields.keys())
    densities2n = Density2N.objects.filter(**density_filter_kwargs).to_dataframe(
        fieldnames=dens_fields
    )
    densities1n = Density1N.objects.filter(**density_filter_kwargs).to_dataframe(
        fieldnames=dens_fields
    )
    densities = pd.concat([densities1n, densities2n])
    assert densities.duplicated().sum() == 0

    convolutions = pd.merge(
        convolutions, densities, how="inner", left_on="density__id", right_on="id"
    ).drop(columns=["id"])

    operator_filter_kwargs = operator_filter_kwargs or dict()
    operator_fields = operator_fields or dict()
    op_fields = ["id"] + list(operator_fields.keys())
    operator1N = Operator1NPWD.objects.filter(**operator_filter_kwargs).to_dataframe(
        fieldnames=op_fields
    )
    operator2N = Operator2NPWD.objects.filter(**operator_filter_kwargs).to_dataframe(
        fieldnames=op_fields
    )
    operators = pd.concat([operator1N, operator2N])
    assert operators.duplicated().sum() == 0

    convolutions = pd.merge(
        convolutions, operators, how="inner", left_on="operator__id", right_on="id"
    ).drop(columns="id")

    assert convolutions.duplicated().sum() == 0

    return convolutions.rename(columns={**density_fields, **operator_fields})
