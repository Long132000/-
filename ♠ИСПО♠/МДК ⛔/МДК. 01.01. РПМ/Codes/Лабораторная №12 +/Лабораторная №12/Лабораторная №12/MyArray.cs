using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Лабораторная__12
{
    public class MyArray
    {
        public static double[] FindC(double[,] array, double[] vector, int n, int m)
        {
            // Вектор C размерностью 1 x m
            double[] C = new double[m];

            // Вычисление вектора C
            for (int k = 0; k < m; k++)
            {
                double sum = 0.0;
                for (int i = 0; i < n; i++)
                {
                    sum += array[i, k];
                }
                C[k] = vector[k] * sum;
            }
            return C;
        }
    }
}
