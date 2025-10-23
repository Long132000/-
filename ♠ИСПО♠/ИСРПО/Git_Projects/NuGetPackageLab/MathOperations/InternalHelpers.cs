using System;

namespace MathOperations
{
    internal static class InternalHelpers
    {
        internal static double CalculateCircleArea(double radius)
        {
            return Math.PI * radius * radius;
        }

        internal static double CalculateTriangleArea(double baseLength, double height)
        {
            return 0.5 * baseLength * height;
        }

        internal static bool IsPrime(int number)
        {
            if (number <= 1) return false;
            if (number == 2) return true;
            if (number % 2 == 0) return false;

            var boundary = (int)Math.Floor(Math.Sqrt(number));
            
            for (int i = 3; i <= boundary; i += 2)
                if (number % i == 0)
                    return false;
            
            return true;
        }
    }
}