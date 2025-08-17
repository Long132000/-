using System;
using System.Collections.Generic;

namespace Laba_11
{
    public class MyArray
    {
        public static void RearrangeArray(ref int[] array)
        {
            // Создаем три списка для положительных, отрицательных и нулей
            var positiveList = new List<int>();
            var negativeList = new List<int>();
            var zeroList = new List<int>();

            foreach (var num in array)
            {
                if (num > 0)
                {
                    positiveList.Add(num);
                }
                else if (num < 0)
                {
                    negativeList.Add(num);
                }
                else
                {
                    zeroList.Add(num);
                }
            }

            // Собираем результат
            int index = 0;
            foreach (var num in positiveList)
            {
                array[index++] = num;
            }
            foreach (var num in negativeList)
            {
                array[index++] = num;
            }
            foreach (var num in zeroList)
            {
                array[index++] = num;
            }
        }
    }
}