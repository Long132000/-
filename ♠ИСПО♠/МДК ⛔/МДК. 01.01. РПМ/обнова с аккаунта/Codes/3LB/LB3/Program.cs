using System;

class Program
{
    static void Main()
    {
        int[] array1 = InputArray("Введите размер первого массива: ");
        int[] array2 = InputArray("Введите размер второго массива: ");

        Console.WriteLine("Первый массив:");
        PrintArray(array1);
        Console.WriteLine("Второй массив:");
        PrintArray(array2);

        int sum1 = SumNotDivisibleBy5(array1);
        int sum2 = SumNotDivisibleBy5(array2);

        Console.WriteLine($"Сумма элементов первого массива, не кратных 5: {sum1}");
        Console.WriteLine($"Сумма элементов второго массива, не кратных 5: {sum2}");

        if (sum1 < sum2)
        {
            SwapHalves(array1);
            Console.WriteLine("Поменяна местами первая и вторая половины первого массива:");
            PrintArray(array1);
        }
        else
        {
            SwapHalves(array2);
            Console.WriteLine("Поменяна местами первая и вторая половины второго массива:");
            PrintArray(array2);
        }
    }

    static int[] InputArray(string prompt)
    {
        Console.Write(prompt);
        int size = int.Parse(Console.ReadLine());
        int[] array = new int[size];
        for (int i = 0; i < size; i++)
        {
            Console.Write($"Введите элемент {i + 1}: ");
            array[i] = int.Parse(Console.ReadLine());
        }
        return array;
    }

    static void PrintArray(int[] array)
    {
        foreach (int element in array)
        {
            Console.Write(element + " ");
        }
        Console.WriteLine();
    }

    static int SumNotDivisibleBy5(int[] array)
    {
        int sum = 0;
        foreach (int element in array)
        {
            if (element % 5 != 0)
                sum += element;
        }
        return sum;
    }

    static void SwapHalves(int[] array)
    {
        int mid = array.Length / 2;
        int[] temp = new int[mid];
        Array.Copy(array, 0, temp, 0, mid);
        Array.Copy(array, mid, array, 0, array.Length - mid);
        Array.Copy(temp, 0, array, array.Length - mid, mid);
    }
}
