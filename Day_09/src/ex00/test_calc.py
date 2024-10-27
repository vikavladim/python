import unittest
import calc as calculator

class TestCalc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculator.add(2, 2), 4)
        self.assertEqual(calculator.add(-2, 2), 0)
        self.assertEqual(calculator.add(-2, -2), -4)
        self.assertEqual(calculator.add(2.5, 2.5), 5.0)
        self.assertEqual(calculator.add(-2.5, 2.5), 0.0)
        self.assertEqual(calculator.add(10, -5), 5)
        self.assertEqual(calculator.add(-10, 5), -5)
        self.assertEqual(calculator.add(0, 0), 0)

    def test_sub(self):
        self.assertEqual(calculator.sub(2, 2), 0)
        self.assertEqual(calculator.sub(-2, 2), -4)
        self.assertEqual(calculator.sub(-2, -2), 0)
        self.assertEqual(calculator.sub(2.5, 2.5), 0.0)
        self.assertEqual(calculator.sub(-2.5, 2.5), -5.0)
        self.assertEqual(calculator.sub(10, -5), 15)
        self.assertEqual(calculator.sub(-10, 5), -15)
        self.assertEqual(calculator.sub(0, 0), 0)

    def test_mul(self):
        self.assertEqual(calculator.mul(2, 2), 4)
        self.assertEqual(calculator.mul(-2, 2), -4)
        self.assertEqual(calculator.mul(-2, -2), 4)
        self.assertEqual(calculator.mul(2.5, 2.5), 6.25)
        self.assertEqual(calculator.mul(-2.5, 2.5), -6.25)
        self.assertEqual(calculator.mul(10, -5), -50)
        self.assertEqual(calculator.mul(-10, 5), -50)
        self.assertEqual(calculator.mul(0, 0), 0)

    def test_div(self):
        self.assertEqual(calculator.div(2, 2), 1)
        self.assertEqual(calculator.div(-2, 2), -1)
        self.assertEqual(calculator.div(-2, -2), 1)
        self.assertEqual(calculator.div(2.5, 2.5), 1.0)
        self.assertEqual(calculator.div(-2.5, 2.5), -1.0)
        self.assertEqual(calculator.div(10, 2), 5)
        self.assertEqual(calculator.div(-9, 2), -4.5)
        with self.assertRaises(ZeroDivisionError):
            calculator.div(2, 0)
        with self.assertRaises(ZeroDivisionError):
            calculator.div(2.5, 0)

if __name__ == '__main__':
    unittest.main()