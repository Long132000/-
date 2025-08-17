using System;

class Program
{
    static void Main()
    {
        // Ввод размерностей массива
        Console.Write("Введите количество строк: ");
        int rows = Convert.ToInt32(Console.ReadLine());
        Console.Write("Введите количество столбцов: ");

        int cols = Convert.ToInt32(Console.ReadLine());

        // Проверка на корректность
        if (rows <= 0 || cols <= 0)
        {
            Console.WriteLine("Размеры массива должны быть положительными.");
            return;
        }

        int[,] mas = new int[rows, cols];
        Random rnd = new Random();

        // Заполнение массива случайными числами
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                mas[i, j] = rnd.Next(-1000, 1000);
                Console.Write("{0,8}", mas[i, j]);
            }
            Console.WriteLine();
        }

        int countNoZero = 0;
        int countMoreOneZero = 0;

        // Подсчет строк без нулей и с более чем 1 нулем
        for (int i = 0; i < rows; i++)
        {
            int zeroCount = 0;
            for (int j = 0; j < cols; j++)
            {
                if (mas[i, j] == 0)
                {
                    zeroCount++;
                }
            }
            if (zeroCount == 0)
            {
                countNoZero++;
            }
            else if (zeroCount > 1)
            {
                countMoreOneZero++;
            }
        }

        Console.WriteLine($"Количество строк без нулей: {countNoZero}");
        Console.WriteLine($"Количество строк с более чем 1 нулем: {countMoreOneZero}");
    }
}
