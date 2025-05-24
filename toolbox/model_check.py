# toolbox/model_check.py
"""Model readiness and utility decorators

Includes:
- check_model_ready: ensures sklearn estimators are fitted before use
- timing: prints function execution time
- catch: catches and reports exceptions from decorated function
- log_args: logs arguments passed into decorated function
- flatten_dict: flattens nested dictionaries into dot-notation keys

Usage
-----
>>> from toolbox.model_check import check_model_ready, timing, catch, log_args, flatten_dict
>>> @check_model_ready
... def evaluate(model, X, y):
...     return model.score(X, y)

>>> @timing
... def run():
...     return sum(range(100000))

>>> @catch
... def risky():
...     return 1 / 0

>>> @log_args
... def greet(name):
...     return f"Hello, {name}"

>>> flatten_dict({"a": {"b": 1}})
... {"a.b": 1}
"""
from __future__ import annotations

import functools
import time
from typing import Callable, Type, Any

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


def check_model_ready(func: Callable) -> Callable:
    """Decorator that verifies *model* argument readiness.

    The decorated function **must** take the estimator/model as its first
    positional argument or as a keyword named ``model``.  If the model is not a
    scikit-learn estimator, or has not been fitted, the function exits early and
    returns ``None``.
    """

    @functools.wraps(func)
    def wrapper(model: BaseEstimator, *args, **kwargs):  # type: ignore[valid-type]
        if not isinstance(model, BaseEstimator):
            print("[❌] Provided object is *not* a scikit-learn estimator → aborting.")
            return None

        required_attr = _find_required_attr(model)
        if required_attr and not hasattr(model, required_attr):
            print(
                f"[❌] Model of type {type(model).__name__} does not have the "
                f"required attribute '{required_attr}'.  Likely not fitted."
            )
            return None

        return func(model, *args, **kwargs)

    return wrapper


def timing(func: Callable) -> Callable:
    """Decorator to measure and print the execution time of a function."""
    @functools.wraps(func)
    def wrap(*args, **kw):
        print(f"<function name: {func.__name__}>")
        time1 = time.time()
        ret = func(*args, **kw)
        time2 = time.time()
        print(f"[timecost: {time2 - time1:.4f} s]")
        return ret
    return wrap


def catch(func: Callable) -> Callable:
    """Decorator to catch and print any exception raised by the function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[⚠️  Caught exception in {func.__name__}]: {e}")
            return None
    return wrapper


def log_args(func: Callable) -> Callable:
    """Decorator to log arguments passed into the function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[🔍 {func.__name__} called with args={args}, kwargs={kwargs}]")
        return func(*args, **kwargs)
    return wrapper


def flatten_dict(d: dict[str, Any], parent_key: str = "", sep: str = ".") -> dict[str, Any]:
    """Flatten nested dictionaries into a single level with dot-separated keys."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


__all__ = ["check_model_ready", "timing", "catch", "log_args", "flatten_dict"]
