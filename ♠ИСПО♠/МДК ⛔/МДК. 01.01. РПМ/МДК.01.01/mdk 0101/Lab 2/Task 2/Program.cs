using System;

class Program
{
    static void Main()
    {
        // Ввод размеров массива
        Console.Write("Введите количество строк: ");
        int rows = Convert.ToInt32(Console.ReadLine());

        Console.Write("Введите количество столбцов: ");
        int cols = Convert.ToInt32(Console.ReadLine());

        // Создаем и заполняем двумерный массив
        int[,] array = new int[rows, cols];
        Random rand = new Random();

        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                array[i, j] = rand.Next(1, 100); // Заполняем случайными числами от 1 до 99
            }
        }

        // Поиск и вывод элементов
        for (int i = 0; i < rows; i++)
        {
            // Ищем индекс первого кратного 5 в строке
            int firstMultipleOfFiveIndex = -1; // Индекс по умолчанию, если не найдено
            for (int j = 0; j < cols; j++)
            {
                if (array[i, j] % 5 == 0)
                {
                    firstMultipleOfFiveIndex = j; // Сохраняем индекс первого кратного 5
                    break; // Выходим из цикла, так как нашли первое кратное 5
                }
            }

            // Выводим элементы строки с окраской
            for (int j = 0; j < cols; j++)
            {
                if (array[i, j] % 5 == 0 && j == firstMultipleOfFiveIndex)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta; // Устанавливаем малиновый цвет
                    Console.Write(array[i, j] + " ");
                    Console.ResetColor(); // Сбрасываем цвет
                }
                else
                {
                    Console.Write(array[i, j] + " ");
                }
            }
            Console.WriteLine();
        }
    }
}
