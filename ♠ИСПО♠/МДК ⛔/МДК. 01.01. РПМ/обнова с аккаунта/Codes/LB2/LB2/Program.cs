using System;

class Program
{
    static void Main()
    {
        // Ввод размерности массива
        Console.Write("Введите размер массива: ");
        int size = Convert.ToInt32(Console.ReadLine());

        // Проверка на корректность
        if (size <= 0)
        {
            Console.WriteLine("Размер массива должен быть положительным.");
            return;
        }

        int[] mas = new int[size];
        Random rnd = new Random();
        int sumPositive = 0;

        // Заполнение массива случайными числами и вычисление суммы положительных
        for (int i = 0; i < mas.Length; i++)
        {
            mas[i] = rnd.Next(-1000, 1000);
            Console.Write("{0,8}", mas[i]);
            if (mas[i] > 0)
            {
                sumPositive += mas[i];
            }
        }

        Console.WriteLine();
        Console.WriteLine($"Сумма положительных элементов: {sumPositive}");

        // Подсчет четных или нечетных элементов
        int count = 0;
        if (sumPositive % 2 == 0) // Четная сумма
        {
            foreach (var item in mas)
            {
                if (item % 2 == 0)
                {
                    count++;
                }
            }
            Console.WriteLine($"Количество четных элементов: {count}");
        }
        else // Нечетная сумма
        {
            foreach (var item in mas)
            {
                if (item % 2 != 0)
                {
                    count++;
                }
            }
            Console.WriteLine($"Количество нечетных элементов: {count}");
        }
    }
}
