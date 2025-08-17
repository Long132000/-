using System;

class Program
{
    static void Main()
    {
        Console.Write("Введите сторону a: ");
        double a = double.Parse(Console.ReadLine());
        Console.Write("Введите сторону b: ");
        double b = double.Parse(Console.ReadLine());
        Console.Write("Введите сторону c: ");
        double c = double.Parse(Console.ReadLine());

        if (CanFormTriangle(a, b, c))
        {
            double area = CalculateArea(a, b, c);
            Console.WriteLine($"Площадь треугольника: {area}");
            string type = DetermineTriangleType(a, b, c);
            Console.WriteLine($"Вид треугольника: {type}");
        }
        else
        {
            Console.WriteLine("Треугольник с такими сторонами не может существовать.");
        }
    }

    static bool CanFormTriangle(double a, double b, double c)
    {
        return a + b > c && a + c > b && b + c > a;
    }

    static double CalculateArea(double a, double b, double c)
    {
        double p = (a + b + c) / 2;
        return Math.Sqrt(p * (p - a) * (p - b) * (p - c));
    }

    static string DetermineTriangleType(double a, double b, double c)
    {
        double a2 = a * a, b2 = b * b, c2 = c * c;
        if (a2 + b2 > c2 && a2 + c2 > b2 && b2 + c2 > a2) return "Остроугольный";
        if (a2 + b2 == c2 || a2 + c2 == b2 || b2 + c2 == a2) return "Прямоугольный";
        return "Тупоугольный";
    }
}
