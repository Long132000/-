using System;
using System.Collections.Generic;
using System.Linq;

public class Program
{
    public enum Пол
    {
        М, // Мужской
        Ж  // Женский
    }

    public enum Должность
    {
        Менеджер,
        Разработчик,
        Тестировщик
    }

    public struct Сотрудник
    {
        public string Фамилия;
        public string Имя;
        public string Отчество;
        public DateTime ДатаРождения;
        public Пол Пол;
        public Должность Должность;
        public int ГодПоступления;

        public Сотрудник(string фамилия, string имя, string отчество, DateTime датаРождения, Пол пол, Должность должность, int годПоступления)
        {
            Фамилия = фамилия;
            Имя = имя;
            Отчество = отчество;
            ДатаРождения = датаРождения;
            Пол = пол;
            Должность = должность;
            ГодПоступления = годПоступления;
        }
    }

    public static void Main()
    {
        List<Сотрудник> сотрудники = new List<Сотрудник>
        {
            new Сотрудник("Иванов", "Иван", "Иванович", new DateTime(1990, 1, 1), Пол.М, Должность.Разработчик, 2015),
            new Сотрудник("Петрова", "Мария", "Сидоровна", new DateTime(1992, 5, 21), Пол.Ж, Должность.Менеджер, 2018),
            new Сотрудник("Сидоров", "Алексей", "Петрович", new DateTime(1985, 3, 15), Пол.М, Должность.Разработчик, 2012),
            new Сотрудник("Кузнецова", "Ольга", "Николаевна", new DateTime(1995, 8, 30), Пол.Ж, Должность.Менеджер, 2021)
        };

        while (true)
        {
            Console.WriteLine("\n** Меню **");
            Console.WriteLine("1. Добавить запись");
            Console.WriteLine("2. Удалить запись");
            Console.WriteLine("3. Вывести весь список");
            Console.WriteLine("4. Корректировать запись");
            Console.WriteLine("5. Отбор записей");
            Console.WriteLine("6. Расчет среднего стажа");
            Console.WriteLine("0. Выход");
            Console.Write("Выберите действие: ");

            int выбор = int.Parse(Console.ReadLine()!);

            switch (выбор)
            {
                case 1:
                    ДобавитьЗапись(сотрудники);
                    break;
                case 2:
                    УдалитьЗапись(сотрудники);
                    break;
                case 3:
                    ВывестиСписок(сотрудники);
                    break;
                case 4:
                    КорректироватьЗапись(сотрудники);
                    break;
                case 5:
                    ОтборЗаписей(сотрудники);
                    break;
                case 6:
                    РасчетСреднегоСтаж(сотрудники);
                    break;
                case 0:
                    return;
                default:
                    Console.WriteLine("Некорректный ввод, попробуйте снова.");
                    break;
            }
        }
    }

    public static void ДобавитьЗапись(List<Сотрудник> сотрудники)
    {
        Console.WriteLine("Введите фамилию: ");
        string фамилия = Console.ReadLine()!;

        Console.WriteLine("Введите имя: ");
        string имя = Console.ReadLine()!;

        Console.WriteLine("Введите отчество: ");
        string отчество = Console.ReadLine()!;

        Console.WriteLine("Введите дату рождения (yyyy-mm-dd): ");
        DateTime датаРождения = DateTime.Parse(Console.ReadLine()!);

        Console.WriteLine("Введите пол (M/Ж): ");
        Пол пол = (Console.ReadLine()!.ToUpper() == "M") ? Пол.М : Пол.Ж;

        Console.WriteLine("Введите должность (Менеджер/Разработчик/Тестировщик): ");
        Должность должность = (Должность)Enum.Parse(typeof(Должность), Console.ReadLine()!);

        Console.WriteLine("Введите год поступления: ");
        int годПоступления = int.Parse(Console.ReadLine()!);
        сотрудники.Add(new Сотрудник(фамилия, имя, отчество, датаРождения, пол, должность, годПоступления));
        Console.WriteLine("Запись добавлена.");
    }

    public static void УдалитьЗапись(List<Сотрудник> сотрудники)
    {
        ВывестиСписок(сотрудники);
        Console.WriteLine("Введите индекс для удаления: ");
        int индекс = int.Parse(Console.ReadLine()!);

        if (индекс >= 0 && индекс < сотрудники.Count)
        {
            сотрудники.RemoveAt(индекс);
            Console.WriteLine("Запись удалена.");
        }
        else
        {
            Console.WriteLine("Некорректный индекс.");
        }
    }

    public static void ВывестиСписок(List<Сотрудник> сотрудники)
    {
        Console.WriteLine("\n** Список сотрудников **");
        for (int i = 0; i < сотрудники.Count; i++)
        {
            var с = сотрудники[i];
            Console.WriteLine($"{i}. {с.Фамилия} {с.Имя} {с.Отчество}, Дата рождения: {с.ДатаРождения.ToShortDateString()}, Пол: {с.Пол}, Должность: {с.Должность}, Год поступления: {с.ГодПоступления}");
        }
    }

    public static void КорректироватьЗапись(List<Сотрудник> сотрудники)
    {
        ВывестиСписок(сотрудники);
        Console.WriteLine("Введите индекс для корректировки: ");
        int индекс = int.Parse(Console.ReadLine()!);

        if (индекс < 0 || индекс >= сотрудники.Count)
        {
            Console.WriteLine("Некорректный индекс.");
            return;
        }

        var с = сотрудники[индекс];
        Console.WriteLine($"Текущие данные: {с.Фамилия} {с.Имя} {с.Отчество}");
        // Здесь можно добавить логику для корректировки отдельных полей
        // Например, изменить имя
        Console.WriteLine("Введите новое имя (или оставьте пустым для пропуска): ");
        string новоеИмя = Console.ReadLine()!;
        if (!string.IsNullOrWhiteSpace(новоеИмя))
        {
            с.Имя = новоеИмя;
        }
        сотрудники[индекс] = с;
        Console.WriteLine("Запись скорректирована.");
    }

    public static void ОтборЗаписей(List<Сотрудник> сотрудники)
    {
        Console.WriteLine("Введите должность для отбора: ");
        Должность должность = (Должность)Enum.Parse(typeof(Должность), Console.ReadLine()!);

        var выбранные = сотрудники.Where(s => s.Должность == должность).ToList();
        if (выбранные.Count == 0)
        {
            Console.WriteLine("Нет записей с данной должностью.");
            return;
        }

        Console.WriteLine("\n** Отобранные записи **");
        foreach (var с in выбранные)
        {
            Console.WriteLine($"{с.Фамилия} {с.Имя} {с.Отчество}");
        }
    }

    public static void РасчетСреднегоСтаж(List<Сотрудник> сотрудники)
    {
        Console.WriteLine("Введите должность для расчета среднего стажа: ");
        Должность должность = (Должность)Enum.Parse(typeof(Должность), Console.ReadLine()!);

        var сотрудникиДолжности = сотрудники.Where(s => s.Должность == должность).ToList();
        if (сотрудникиДолжности.Count == 0)
        {
            Console.WriteLine("Нет сотрудников с данной должностью.");
            return;
        }

        double среднийСтаж = сотрудникиДолжности.Average(s => DateTime.Now.Year - s.ГодПоступления);
        Console.WriteLine($"Средний стаж для должности {должность}: {среднийСтаж} лет");
    }
}
