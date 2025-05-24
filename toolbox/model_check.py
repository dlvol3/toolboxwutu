# toolbox/model_check.py
"""Model readiness decorator

A utility decorator that ensures a scikit‑learn model is a valid estimator **and** has
been fitted before running expensive post‑processing (evaluation, explanation, …).

Usage
-----
>>> from toolbox.model_check import check_model_ready
>>> @check_model_ready
... def evaluate(model, X, y):
...     return model.score(X, y)
"""
from __future__ import annotations

import functools
from typing import Callable, Type

from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

# ---------------------------------------------------------------------------
# Mapping: estimator class -> attribute that should exist **after** fitting.
# ---------------------------------------------------------------------------
_TRAINED_ATTRS: dict[Type[BaseEstimator], str] = {
    LogisticRegression: "coef_",
    RandomForestClassifier: "feature_importances_",
    DecisionTreeClassifier: "tree_",
    SVC: "support_",
    KNeighborsClassifier: "_fit_X",
}


def _find_required_attr(estimator: BaseEstimator) -> str | None:
    """Return the attribute name that proves the estimator was fitted.

    If the estimator class is not in the mapping, return ``None`` so the user
    can decide whether to skip the check or raise.
    """
    for cls, attr in _TRAINED_ATTRS.items():
        if isinstance(estimator, cls):
            return attr
    return None


# ---------------------------------------------------------------------------
# Public decorator
# ---------------------------------------------------------------------------

def check_model_ready(func: Callable) -> Callable:
    """Decorator that verifies *model* argument readiness.

    The decorated function **must** take the estimator/model as its first
    positional argument or as a keyword named ``model``.  If the model is not a
    scikit‑learn estimator, or has not been fitted, the function exits early and
    returns ``None``.
    """

    @functools.wraps(func)
    def wrapper(model: BaseEstimator, *args, **kwargs):  # type: ignore[valid-type]
        # 1) Sanity check – is this a scikit‑learn estimator?
        if not isinstance(model, BaseEstimator):
            print("[❌] Provided object is *not* a scikit‑learn estimator → aborting.")
            return None

        # 2) Check if model appears fitted
        required_attr = _find_required_attr(model)
        if required_attr and not hasattr(model, required_attr):
            print(
                f"[❌] Model of type {type(model).__name__} does not have the "
                f"required attribute '{required_attr}'.  Likely not fitted."
            )
            return None

        # 3) All good → run the original function
        return func(model, *args, **kwargs)

    return wrapper


# ---------------------------------------------------------------------------
# Handy re‑export so users can «from toolbox import check_model_ready»
# ---------------------------------------------------------------------------
__all__ = ["check_model_ready"]
