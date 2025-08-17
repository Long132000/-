using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using Лабораторная__12;

namespace UnitTestProject1
{
    [TestClass]
    public class UnitTest1
    {
        [TestMethod]
        public void TestMethod1()
        {
            double[,] array = {
                { 1.0, 2.0 },
                { 3.0, 4.0 }
            };
            double[] vector = { 1.0, 2.0 };
            int n = 2;
            int m = 2;

            double[] c = MyArray.FindC(array, vector, n, m);
            string s = "";
            for (int i = 0; i < m; i++)
                s += " " + c[i];

            CollectionAssert.AreEqual(new double[] { 4.0, 12.0 }, c, s);
        }
        [TestMethod]
        public void TestMethod2()
        {

            double[,] array = {
                { 1.0, 2.0, 3.0 },
                { 4.0, 5.0, 6.0 },
                { 7.0, 8.0, 9.0 }
            };
            double[] vector = { 1.0, 2.0, 3.0 };
            int n = 3;
            int m = 3;


            double[] c = MyArray.FindC(array, vector, n, m);
            string s = "";
            for (int i = 0; i < m; i++)
                s += " " + c[i];

            CollectionAssert.AreEqual(new double[] { 12.0, 30.0, 54.0 }, c, s);
        }
        [TestMethod]
        public void TestMethod3()
        {

            double[,] array = {
                { 1.0, 1.0, 1.0 },
                { 1.0, 1.0, 1.0 },
                { 1.0, 1.0, 1.0 }
            };
            double[] vector = { 1.0, 2.0, 3.0 };
            int n = 3;
            int m = 3;


            double[] c = MyArray.FindC(array, vector, n, m);
            string s = "";
            for (int i = 0; i < m; i++)
                s += " " + c[i];

            CollectionAssert.AreEqual(new double[] { 3.0, 6.0, 9.0 }, c, s);
        }
    }
}
