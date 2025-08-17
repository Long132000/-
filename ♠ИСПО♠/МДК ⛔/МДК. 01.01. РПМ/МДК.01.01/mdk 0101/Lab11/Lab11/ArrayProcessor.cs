using System.Collections.Generic;

namespace Lab11
{
    public static class ArrayProcessor
    {
        public static double[] ReversePositiveElements(double[] array)
        {
            // Создаем копию массива для работы
            double[] result = (double[])array.Clone();

            // Собираем индексы положительных элементов
            List<int> positiveIndices = new List<int>();
            for (int i = 0; i < result.Length; i++)
            {
                if (result[i] > 0)
                {
                    positiveIndices.Add(i);
                }
            }

            // Переставляем положительные элементы в обратном порядке
            int left = 0;
            int right = positiveIndices.Count - 1;

            while (left < right)
            {
                int leftIndex = positiveIndices[left];
                int rightIndex = positiveIndices[right];

                // Меняем местами
                double temp = result[leftIndex];
                result[leftIndex] = result[rightIndex];
                result[rightIndex] = temp;

                left++;
                right--;
            }

            return result;
        }
    }
}