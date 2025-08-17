using System;

class Program
{
    static void Main()
    {
        // Ввод четырёх целых чисел
        Console.WriteLine("Введите четыре целых числа:");
        int[] numbers = new int[4];

        for (int i = 0; i < 4; i++)
        {
            Console.Write($"Число {i + 1}: ");
            numbers[i] = int.Parse(Console.ReadLine());
        }

        // Проверяем, есть ли хотя бы одно четное число
        bool hasEven = false;
        foreach (int number in numbers)
        {
            if (number % 2 == 0)
            {
                hasEven = true;
                break;
            }
        }

        Console.Clear();

        if (hasEven)
        {
            // Вывод четных и нечетных чисел с цветовым кодированием
            foreach (int number in numbers)
            {
                if (number % 2 == 0)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine(number);
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine(number);
                }
            }
        }
        else
        {
            // Если все числа нечётные, рассчитываем их произведение
            int product = 1;
            foreach (int number in numbers)
            {
                product *= number;
            }

            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("Произведение нечётных чисел: " + product);
        }

        // Сброс цвета консоли
        Console.ResetColor();
        Console.ReadKey();
    }
}
