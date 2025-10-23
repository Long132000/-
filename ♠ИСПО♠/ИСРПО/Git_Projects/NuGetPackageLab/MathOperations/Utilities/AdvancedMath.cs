using System;

namespace MathOperations.Utilities
{
    public class AdvancedMath
    {
        public double Power(double baseValue, double exponent)
        {
            return Math.Pow(baseValue, exponent);
        }

        public double SquareRoot(double value)
        {
            if (value < 0)
                throw new ArgumentException("Cannot calculate square root of negative number");
            return Math.Sqrt(value);
        }

        public double Logarithm(double value, double baseValue = 10)
        {
            if (value <= 0)
                throw new ArgumentException("Logarithm is defined only for positive numbers");
            return Math.Log(value, baseValue);
        }
    }
}