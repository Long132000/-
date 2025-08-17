using System;

public class Parallelogram
{
    public static double CalculatePerimeter(double a, double b)
    {
        return 2 * (a + b);
    }

    public static double CalculateArea(double a, double b, double angle)
    {
        return a * b * Math.Sin(angle * Math.PI / 180); // Преобразование градусов в радианы
    }

    public static double CalculateDiagonal(double a, double b, double angle)
    {
        return Math.Sqrt(a * a + b * b - 2 * a * b * Math.Cos(angle * Math.PI / 180));
    }

    public static void Main(string[] args)
    {
        Console.WriteLine("Введите длину стороны a:");
        double a = double.Parse(Console.ReadLine());

        Console.WriteLine("Введите длину стороны b:");
        double b = double.Parse(Console.ReadLine());

        Console.WriteLine("Введите угол при основании (в градусах):");
        double angle = double.Parse(Console.ReadLine());

        double perimeter = CalculatePerimeter(a, b);
        double area = CalculateArea(a, b, angle);
        double diagonal = CalculateDiagonal(a, b, angle);

        Console.WriteLine($"Периметр: {perimeter}");
        Console.WriteLine($"Площадь: {area}");
        Console.WriteLine($"Длина диагонали: {diagonal}");
    }
}