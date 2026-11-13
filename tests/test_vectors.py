import math

import pytest

from vector_utils import cosine, dot, norm, normalize


def test_dot_product_basic():
    assert dot([1, 2], [3, 4]) == 11.0
    assert dot([0, 0], [1, 5]) == 0.0


def test_dot_product_floats():
    # Ensure float precision is handled
    result = dot([1.5, 2.0], [2.0, 0.5])
    assert math.isclose(result, 4.0)


def test_norm_edge_cases():
    assert norm([3, 4]) == 5.0
    assert norm([]) == 0.0
    assert norm([0, 0, 0]) == 0.0


def test_normalize_direction():
    v = [3, 4]
    n = normalize(v)
    # Magnitude should be 1
    assert math.isclose(norm(n), 1.0)
    # Direction should be preserved (ratios)
    assert math.isclose(n[0] / n[1], 3 / 4)


def test_normalize_zero_empty():
    assert normalize([0, 0]) == [0.0, 0.0]
    assert normalize([]) == []


def test_cosine_similarity_ortho_opposite():
    v1 = [1, 0]
    v2 = [0, 1]
    v3 = [-1, 0]
    assert math.isclose(cosine(v1, v2), 0.0, abs_tol=1e-9)
    assert math.isclose(cosine(v1, v3), -1.0, abs_tol=1e-9)


def test_cosine_zero_handling():
    # Cosine with a zero vector is undefined, usually handled as 0.0 to avoid NaN
    assert cosine([0, 0], [1, 1]) == 0.0
