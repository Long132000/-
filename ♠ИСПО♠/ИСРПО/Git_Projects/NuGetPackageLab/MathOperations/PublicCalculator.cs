using System;
using MathOperations.Utilities;

namespace MathOperations
{
    public class PublicCalculator
    {
        private readonly AdvancedMath _advancedMath;

        public PublicCalculator()
        {
            _advancedMath = new AdvancedMath();
        }

        public double Add(double a, double b) => a + b;
        
        public double Subtract(double a, double b) => a - b;
        
        public double Multiply(double a, double b) => a * b;
        
        public double Divide(double a, double b)
        {
            if (b == 0)
                throw new DivideByZeroException("Division by zero is not allowed");
            return a / b;
        }

        public double CalculateCircleArea(double radius)
        {
            return InternalHelpers.CalculateCircleArea(radius);
        }

        public double CalculatePower(double baseValue, double exponent)
        {
            return _advancedMath.Power(baseValue, exponent);
        }
    }
}