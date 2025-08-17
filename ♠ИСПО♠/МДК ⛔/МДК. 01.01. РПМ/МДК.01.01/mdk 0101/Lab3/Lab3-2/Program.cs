using System;

public class Arrays
{
    public static void InputArray(int[] arr)
    {
        Console.WriteLine("Введите элементы массива:");
        for (int i = 0; i < arr.Length; i++)
        {
            arr[i] = int.Parse(Console.ReadLine());
        }
    }

    public static void OutputArray(int[] arr)
    {
        Console.WriteLine("Массив:");
        foreach (int num in arr)
        {
            Console.Write(num + " ");
        }
        Console.WriteLine();
    }

    public static int CountMaxElements(int[] arr)
    {
        if (arr.Length == 0) return 0;
        int max = arr[0];
        int count = 1;
        for (int i = 1; i < arr.Length; i++)
        {
            if (arr[i] > max)
            {
                max = arr[i];
                count = 1;
            }
            else if (arr[i] == max)
            {
                count++;
            }
        }
        return count;
    }

    public static void OutputArrayWithColoredMax(int[] arr)
    {
        int max = arr.Max();
        int count = arr.Count(x => x == max);

        Console.WriteLine("Массив с выделенными максимальными элементами:");
        foreach (int num in arr)
        {
            if (num == max && count > 1)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.Write(num + " ");
                Console.ResetColor();
            }
            else
            {
                Console.Write(num + " ");
            }
        }
        Console.WriteLine();

    }

    public static void Main(string[] args)
    {
        Console.WriteLine("Введите размер первого массива:");
        int size1 = int.Parse(Console.ReadLine());
        int[] arr1 = new int[size1];
        InputArray(arr1);
        OutputArray(arr1);
        Console.WriteLine($"Количество максимальных элементов: {CountMaxElements(arr1)}");
        OutputArrayWithColoredMax(arr1);


        Console.WriteLine("Введите размер второго массива:");
        int size2 = int.Parse(Console.ReadLine());
        int[] arr2 = new int[size2];
        InputArray(arr2);
        OutputArray(arr2);
        Console.WriteLine($"Количество максимальных элементов: {CountMaxElements(arr2)}");
        OutputArrayWithColoredMax(arr2);


        Console.WriteLine("Введите размер третьего массива:");
        int size3 = int.Parse(Console.ReadLine());
        int[] arr3 = new int[size3];
        InputArray(arr3);
        OutputArray(arr3);
        Console.WriteLine($"Количество максимальных элементов: {CountMaxElements(arr3)}");
        OutputArrayWithColoredMax(arr3);

    }
}
