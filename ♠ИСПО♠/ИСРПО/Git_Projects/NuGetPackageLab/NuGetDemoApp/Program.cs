using MathOperations;

class Program
{
    static void Main()
    {
        Console.WriteLine("=== Демонстрация NuGet пакета ===");
        Console.WriteLine("Лабораторная работа №3 - Система управления пакетами NuGet\n");
        
        // 1. Демонстрация работы с public классами
        DemonstratePublicAccess();
        
        // 2. Демонстрация недоступности internal классов
        DemonstrateInternalInaccessibility();
        
        Console.WriteLine("\nДемонстрация завершена!");
        Console.WriteLine("Нажмите любую клавишу для выхода...");
        Console.ReadKey();
    }
    
    static void DemonstratePublicAccess()
    {
        Console.WriteLine("1. РАБОТА С PUBLIC КЛАССАМИ:");
        Console.WriteLine("----------------------------");
        
        // Создаем экземпляр public класса
        var calculator = new PublicCalculator();
        
        // Используем public методы
        Console.WriteLine($"✓ PublicCalculator.Add(5, 3) = {calculator.Add(5, 3)}");
        Console.WriteLine($"✓ PublicCalculator.Subtract(10, 4) = {calculator.Subtract(10, 4)}");
        Console.WriteLine($"✓ PublicCalculator.Multiply(6, 7) = {calculator.Multiply(6, 7)}");
        Console.WriteLine($"✓ PublicCalculator.Divide(15, 3) = {calculator.Divide(15, 3)}");
        
        // Используем public метод, который внутри использует internal логику
        Console.WriteLine($"✓ PublicCalculator.CalculateCircleArea(5) = {calculator.CalculateCircleArea(5):F2}");
        Console.WriteLine($"✓ PublicCalculator.CalculatePower(2, 8) = {calculator.CalculatePower(2, 8)}");
        
        // Используем другой public класс из пакета
        var advancedMath = new MathOperations.Utilities.AdvancedMath();
        Console.WriteLine($"✓ AdvancedMath.SquareRoot(16) = {advancedMath.SquareRoot(16)}");
        Console.WriteLine($"✓ AdvancedMath.Logarithm(100) = {advancedMath.Logarithm(100)}");
    }
    
    static void DemonstrateInternalInaccessibility()
    {
        Console.WriteLine("\n2. ДОСТУП К INTERNAL КЛАССАМ:");
        Console.WriteLine("----------------------------");
        
        Console.WriteLine("❌ Попытка использования internal классов приведет к ошибкам компиляции:");
        Console.WriteLine("   - InternalHelpers - НЕДОСТУПЕН");
        Console.WriteLine("   - InternalHelpers.CalculateTriangleArea() - НЕДОСТУПЕН"); 
        Console.WriteLine("   - InternalHelpers.IsPrime() - НЕДОСТУПЕН");
        
        // Раскомментируйте следующие строки чтобы увидеть ошибки компиляции:
        
        // ❌ ОШИБКА: InternalHelpers - internal класс, недоступен извне
        // var helpers = new InternalHelpers();
        
        // ❌ ОШИБКА: CalculateTriangleArea - internal метод, недоступен извне
        // var area = InternalHelpers.CalculateTriangleArea(10, 5);
        
        // ❌ ОШИБКА: IsPrime - internal метод, недоступен извне  
        // var isPrime = InternalHelpers.IsPrime(17);
        
        Console.WriteLine("\n✓ Internal классы и методы защищены от внешнего доступа");
        Console.WriteLine("✓ Это обеспечивает инкапсуляцию внутренней логики библиотеки");
    }
}