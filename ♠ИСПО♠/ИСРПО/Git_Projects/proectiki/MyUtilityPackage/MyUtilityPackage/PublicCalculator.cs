namespace MyUtilityPackage
{
    public class PublicCalculator
    {
        public int Add(int a, int b)
        {
            return a + b;
        }

        // Этот метод будет доступен только внутри самой сборки (пакета)
        internal int InternalMultiply(int a, int b)
        {
            return a * b;
        }
    }
}