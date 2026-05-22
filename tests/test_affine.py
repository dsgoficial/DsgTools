# -*- coding: utf-8 -*-
import math
import pytest
pytestmark = pytest.mark.unit


from DsgTools.core.GeometricTools.affine import Affine, TransformNotInvertibleError


# ---------------------------------------------------------------------------
# cos_sin_deg
# ---------------------------------------------------------------------------
class TestCosSinDeg:
    def test_0_degrees(self):
        from DsgTools.core.GeometricTools.affine import cos_sin_deg
        c, s = cos_sin_deg(0)
        assert math.isclose(c, 1.0, abs_tol=1e-10)
        assert math.isclose(s, 0.0, abs_tol=1e-10)

    def test_90_degrees(self):
        from DsgTools.core.GeometricTools.affine import cos_sin_deg
        c, s = cos_sin_deg(90)
        assert c == 0.0
        assert s == 1.0

    def test_180_degrees(self):
        from DsgTools.core.GeometricTools.affine import cos_sin_deg
        c, s = cos_sin_deg(180)
        assert c == -1.0
        assert s == 0

    def test_270_degrees(self):
        from DsgTools.core.GeometricTools.affine import cos_sin_deg
        c, s = cos_sin_deg(270)
        assert c == 0
        assert s == -1.0

    def test_45_degrees(self):
        from DsgTools.core.GeometricTools.affine import cos_sin_deg
        c, s = cos_sin_deg(45)
        expected = math.sqrt(2) / 2
        assert math.isclose(c, expected, abs_tol=1e-10)
        assert math.isclose(s, expected, abs_tol=1e-10)

    def test_360_wraps_to_0(self):
        from DsgTools.core.GeometricTools.affine import cos_sin_deg
        c0, s0 = cos_sin_deg(0)
        c360, s360 = cos_sin_deg(360)
        assert math.isclose(c0, c360, abs_tol=1e-10)
        assert math.isclose(s0, s360, abs_tol=1e-10)


# ---------------------------------------------------------------------------
# Affine.identity
# ---------------------------------------------------------------------------
class TestAffineIdentity:
    def test_is_identity(self):
        t = Affine.identity()
        assert t.is_identity

    def test_coefficients(self):
        t = Affine.identity()
        assert t.a == 1.0 and t.b == 0.0 and t.c == 0.0
        assert t.d == 0.0 and t.e == 1.0 and t.f == 0.0

    def test_determinant_is_one(self):
        assert Affine.identity().determinant == 1.0

    def test_is_rectilinear(self):
        assert Affine.identity().is_rectilinear

    def test_is_conformal(self):
        assert Affine.identity().is_conformal

    def test_is_orthonormal(self):
        assert Affine.identity().is_orthonormal

    def test_is_not_degenerate(self):
        assert not Affine.identity().is_degenerate


# ---------------------------------------------------------------------------
# Affine.translation
# ---------------------------------------------------------------------------
class TestAffineTranslation:
    def test_shifts_point(self):
        t = Affine.translation(3.0, 5.0)
        x, y = t * (0.0, 0.0)
        assert math.isclose(x, 3.0)
        assert math.isclose(y, 5.0)

    def test_shifts_non_origin(self):
        t = Affine.translation(1.0, 2.0)
        x, y = t * (4.0, 6.0)
        assert math.isclose(x, 5.0)
        assert math.isclose(y, 8.0)

    def test_not_identity(self):
        t = Affine.translation(1.0, 0.0)
        assert not t.is_identity

    def test_determinant_is_one(self):
        t = Affine.translation(10.0, -7.0)
        assert math.isclose(t.determinant, 1.0)

    def test_zero_translation_is_identity(self):
        t = Affine.translation(0.0, 0.0)
        assert t.is_identity


# ---------------------------------------------------------------------------
# Affine.scale
# ---------------------------------------------------------------------------
class TestAffineScale:
    def test_scales_point(self):
        t = Affine.scale(2.0, 3.0)
        x, y = t * (1.0, 1.0)
        assert math.isclose(x, 2.0)
        assert math.isclose(y, 3.0)

    def test_uniform_scale(self):
        t = Affine.scale(4.0)
        x, y = t * (1.0, 1.0)
        assert math.isclose(x, 4.0)
        assert math.isclose(y, 4.0)

    def test_determinant(self):
        t = Affine.scale(2.0, 3.0)
        assert math.isclose(t.determinant, 6.0)

    def test_unit_scale_is_identity(self):
        t = Affine.scale(1.0, 1.0)
        assert t.is_identity

    def test_is_rectilinear(self):
        assert Affine.scale(2.0, 3.0).is_rectilinear

    def test_zero_scale_is_degenerate(self):
        assert Affine.scale(0.0, 1.0).is_degenerate


# ---------------------------------------------------------------------------
# Affine.rotation
# ---------------------------------------------------------------------------
class TestAffineRotation:
    def test_90_degree_rotation(self):
        t = Affine.rotation(90.0)
        x, y = t * (1.0, 0.0)
        assert math.isclose(x, 0.0, abs_tol=1e-10)
        assert math.isclose(y, 1.0, abs_tol=1e-10)

    def test_180_degree_rotation(self):
        t = Affine.rotation(180.0)
        x, y = t * (1.0, 0.0)
        assert math.isclose(x, -1.0, abs_tol=1e-10)
        assert math.isclose(y, 0.0, abs_tol=1e-10)

    def test_0_degree_rotation_is_identity(self):
        t = Affine.rotation(0.0)
        assert t.is_identity

    def test_determinant_is_one(self):
        t = Affine.rotation(45.0)
        assert math.isclose(t.determinant, 1.0, abs_tol=1e-10)

    def test_is_orthonormal(self):
        assert Affine.rotation(30.0).is_orthonormal

    def test_is_conformal(self):
        assert Affine.rotation(60.0).is_conformal


# ---------------------------------------------------------------------------
# Composition and almost_equals
# ---------------------------------------------------------------------------
class TestAffineComposition:
    def test_translate_then_scale(self):
        t = Affine.translation(1.0, 2.0) * Affine.scale(2.0, 2.0)
        x, y = t * (0.0, 0.0)
        assert math.isclose(x, 2.0, abs_tol=1e-10)
        assert math.isclose(y, 4.0, abs_tol=1e-10)

    def test_almost_equals_same(self):
        t = Affine.rotation(45.0)
        assert t.almost_equals(t)

    def test_almost_equals_different(self):
        assert not Affine.identity().almost_equals(Affine.rotation(1.0))

    def test_inverse_of_translation(self):
        t = Affine.translation(3.0, 4.0)
        inv = ~t
        x, y = inv * (3.0, 4.0)
        assert math.isclose(x, 0.0, abs_tol=1e-10)
        assert math.isclose(y, 0.0, abs_tol=1e-10)

    def test_degenerate_has_no_inverse(self):
        with pytest.raises(TransformNotInvertibleError):
            ~Affine.scale(0.0, 1.0)
