#include "pch.h"
#include "CppUnitTest.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTest1
{
	TEST_CLASS(UnitTest1)
	{
	public:
		
		TEST_METHOD(TestMethod1)
		{
			int num = 69;
			Assert::AreEqual( num + 1, 70);
		}
		TEST_METHOD(TestMethod2)
		{
			int number = 1;
			Assert::AreEqual(number--, 2);
		}
	};
}
