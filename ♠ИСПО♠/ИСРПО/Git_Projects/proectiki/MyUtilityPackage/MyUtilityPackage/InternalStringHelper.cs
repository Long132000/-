namespace MyUtilityPackage
{
    // Этот класс не будет виден за пределами сборки (пакета)
    internal class InternalStringHelper
    {
        public static string ReverseString(string s)
        {
            char[] charArray = s.ToCharArray();
            Array.Reverse(charArray);
            return new string(charArray);
        }
    }
}