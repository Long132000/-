using Laba_11;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace UnitTestProject1
{
    [TestClass]
    public class UnitTest1
    {
        [TestMethod]
        public void TestRearrangeArray_PositiveAndNegative()
        {
            int[] myAr = { -1, -2, -3, -4, 1, 2, 3 };
            int[] expected = { 1, 2, 3, -1, -2, -3, -4 };

            MyArray.RearrangeArray(ref myAr);
            CollectionAssert.AreEqual(expected, myAr);
        }

        [TestMethod]
        public void TestRearrangeArray_OnlyPositives()
        {
            int[] myAr = { 1, 2, 3, 4 };
            int[] expected = { 1, 2, 3, 4 };

            MyArray.RearrangeArray(ref myAr);
            CollectionAssert.AreEqual(expected, myAr);
        }

        [TestMethod]
        public void TestRearrangeArray_OnlyNegatives()
        {
            int[] myAr = { -1, -2, -3, -4 };
            int[] expected = { -1, -2, -3, -4 };

            MyArray.RearrangeArray(ref myAr);
            CollectionAssert.AreEqual(expected, myAr);
        }

        [TestMethod]
        public void TestRearrangeArray_OnlyZeros()
        {
            int[] myAr = { 0, 0, 0 };
            int[] expected = { 0, 0, 0 };

            MyArray.RearrangeArray(ref myAr);
            CollectionAssert.AreEqual(expected, myAr);
        }

        [TestMethod]
        public void TestRearrangeArray_Mixed()
        {
            int[] myAr = { 0, -1, 2, 0, -3, 4 };
            int[] expected = { 2, 4, -1, -3, 0, 0 };

            MyArray.RearrangeArray(ref myAr);
            CollectionAssert.AreEqual(expected, myAr);
        }

        [TestMethod]
        public void TestRearrangeArray_EmptyArray()
        {
            int[] myAr = { };
            int[] expected = { };

            MyArray.RearrangeArray(ref myAr);
            CollectionAssert.AreEqual(expected, myAr);
        }
    }
}