from unittest import TestCase
from triangle import area_of_a_triangle

class TestAreaOfTriangle(TestCase):

    def test_float_values(self):
        """Prueba áreas cuando los valores son flotantes"""
        self.assertAlmostEqual(area_of_a_triangle(3.4556, 8.3567), 14.43870626)
        self.assertEqual(area_of_a_triangle(2.3, 5.7), 6.555)

    def test_integer_values(self):
        """Prueba áreas cuando los valores son enteros"""
        self.assertEqual(area_of_a_triangle(2, 5), 5.0)
        self.assertEqual(area_of_a_triangle(4, 6), 12.0)

    def test_zero_base(self):
        """Prueba áreas cuando la base es cero"""
        self.assertEqual(area_of_a_triangle(0, 5), 0.0)

    def test_zero_height(self):
        """Prueba áreas cuando la altura es cero"""
        self.assertEqual(area_of_a_triangle(2, 0), 0.0)

    def test_zero_values(self):
        """Prueba áreas cuando la base y la altura son cero"""
        self.assertEqual(area_of_a_triangle(0, 0), 0.0)

    def test_negative_base(self):
        """Prueba que se lance ValueError cuando la base es negativa"""
        self.assertRaises(ValueError, area_of_a_triangle, -2, 5)

    def test_negative_height(self):
        """Prueba que se lance ValueError cuando la altura es negativa"""
        self.assertRaises(ValueError, area_of_a_triangle, 2, -5)

    def test_negative_values(self):
        """Prueba que se lance ValueError cuando ambos son negativos"""
        self.assertRaises(ValueError, area_of_a_triangle, -2, -5)

    def test_with_boolean(self):
        """Prueba que se lance TypeError con tipos booleanos"""
        self.assertRaises(TypeError, area_of_a_triangle, True, 5)   # prueba con booleanos
        self.assertRaises(TypeError, area_of_a_triangle, 2, True)

    def test_with_string(self):
        """Prueba que se lance TypeError con tipos string"""
        self.assertRaises(TypeError, area_of_a_triangle, "base", 5) # prueba con strings
        self.assertRaises(TypeError, area_of_a_triangle, 2, "altura")

    def test_with_nulls(self):
        """Prueba que se lance TypeError con tipos nulos"""
        self.assertRaises(TypeError, area_of_a_triangle, None, 5) # prueba con nulos
        self.assertRaises(TypeError, area_of_a_triangle, 2, None)
