"""Extended json encoders."""
import json
import numpy as np
from sympy import Expr


class NympyEncoder(json.JSONEncoder):
    """Extend json encoder to reckognize numpy dtypes.

    See also: https://stackoverflow.com/a/57915246
    """

    def default(self, obj):
        """Extend numpy dtypes."""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, Expr):
            return str(obj)
        else:
            return super().default(obj)
