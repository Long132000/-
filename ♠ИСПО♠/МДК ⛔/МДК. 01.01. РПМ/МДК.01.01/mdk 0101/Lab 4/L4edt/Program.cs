using System;
using System.Collections.Generic;
using System.Linq;

namespace l4
{
    class Program
    {
        public enum orgType // Создание перечисления типов организаций
        {
            Неизвестно,
            ООО,
            ОАО,
            ЗАО,
            ПАО,
            ИП
        }

        public struct Organization // Создание структуры организации (Босс, а я состою в организации?)
        {
            public string Name;
            public orgType Type;
            public string Address;
            public string Phone;
            public Organization(string name, orgType type, string address, string phone) // Конструктор организации (Конечно, Доппио))
            {
                Name = name;
                Type = type;
                Address = address;
                Phone = phone;
            }
        }

        static List<Organization> organizations = new List<Organization> // Создаём организации (А в какой *непереводимый итальянский фольклор*?*)
        {
            new Organization("RKN", orgType.Неизвестно, "Москва, Ленинский проспект, дом 4, Строение 1А", "8(800)5553535"),
            new Organization("Passione", orgType.ИП, "n/a", "+39(339)7654321"),
            new Organization("AAA", orgType.ПАО, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "8(444)4444444"),
            new Organization("Denis' TablesForSleep", orgType.ИП, "СПб, Мебельная ул., дом 47, корпус 1", "8(812)3469696")
        };

        static void Main()
        {
            while (true)
            {
                Console.WriteLine("\n--- Меню ---");
                Console.WriteLine("1. Добавить организацию");
                Console.WriteLine("2. Удалить организацию по индексу");
                Console.WriteLine("3. Вывести все организации");
                Console.WriteLine("4. Изменить организацию по имени");
                Console.WriteLine("5. Поиск по номеру телефона");
                Console.WriteLine("6. Поиск по типу организации");
                Console.WriteLine("7. Выход");
                Console.Write("Выберите действие: ");
                var choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        AddOrganization();
                        break;

                    case "2":
                        RemoveOrganization();
                        break;

                    case "3":
                        DisplayOrganizations();
                        break;

                    case "4":
                        ModifyOrganization();
                        break;

                    case "5":
                        SearchByPhone();
                        break;

                    case "6":
                        SearchByType();
                        break;

                    case "7":
                        return;

                    default:
                        Console.WriteLine("Неверный выбор. Попробуйте снова.");
                        break;
                }
            }
        }

        static void AddOrganization()
        {
            Console.Write("Введите название: ");
            string name = Console.ReadLine();
            Console.Write("Введите тип (неизвестно, ооо, оао, зао, пао, ип): ");
            string typeInput = Console.ReadLine();
            Enum.TryParse(typeInput, true, out orgType type);
            Console.Write("Введите адрес: ");
            string address = Console.ReadLine();
            Console.Write("Введите телефон: ");
            string phone = Console.ReadLine();
            organizations.Add(new Organization(name, type, address, phone));
            Console.WriteLine("Организация добавлена.");
        }

        static void RemoveOrganization()
        {
            Console.Write("Введите индекс для удаления: ");
            if (int.TryParse(Console.ReadLine(), out int index) && index >= 0 && index < organizations.Count)
            {
                organizations.RemoveAt(index);

                Console.WriteLine("Организация удалена.");
            }
            else
            {
                Console.WriteLine("Ошибка: индекс вне диапазона.");
            }
        }

        static void DisplayOrganizations()
        {
            if (organizations.Count == 0)
            {
                Console.WriteLine("Список организаций пуст.");
                return;
            }

            for (int i = 0; i < organizations.Count; i++)
            {
                var org = organizations[i];
                Console.WriteLine($"{i}. {org.Name}, Тип: {org.Type}, Адрес: {org.Address}, Телефон: {org.Phone}");
            }
        }

        static void ModifyOrganization()
        {
            Console.Write("Введите название организации для изменения: ");
            string name = Console.ReadLine();

            var organization = organizations.FirstOrDefault(org => org.Name.Equals(name, StringComparison.OrdinalIgnoreCase));

            if (organization.Equals(default(Organization)))
            {
                Console.WriteLine("Организация не найдена.");
                return;
            }

            Console.Write("Введите новый тип (неизвестно, ооо, оао, зао, пао, ип): ");
            string typeInput = Console.ReadLine();
            Enum.TryParse(typeInput, true, out orgType type);
            Console.Write("Введите новый адрес: ");
            string address = Console.ReadLine();
            Console.Write("Введите новый телефон: ");
            string phone = Console.ReadLine();

            organization.Type = type;
            organization.Address = address;
            organization.Phone = phone;

            int index = organizations.IndexOf(organization);
            organizations[index] = organization;

            Console.WriteLine("Организация изменена.");
        }

        static void SearchByPhone()
        {
            Console.Write("Введите начальную часть номера телефона: ");
            string search = Console.ReadLine();
            var searchRes = organizations.Where(org => org.Phone.StartsWith(search)).ToList();

            if (searchRes.Any())
            {
                Console.WriteLine("Организации, телефоны которых начинаются на " + search + ":");
                foreach (var org in searchRes)
                {
                    Console.WriteLine($"- {org.Name}, Адрес: {org.Address}, Телефон: {org.Phone}");
                }
            }
            else
            {
                Console.WriteLine("Организаций с таким номером не найдено.");
            }
        }

        static void SearchByType()
        {
            Console.Write("Введите тип организации (неизвестно, ооо, оао, зао, пао, ип): ");
            string typeInput = Console.ReadLine();
            orgType searchType;

            if (Enum.TryParse(typeInput, true, out searchType))
            {
                var specType = organizations.Where(org => org.Type == searchType).ToList();

                if (specType.Any())
                {
                    Console.WriteLine($"Организации типа {searchType}:");
                    foreach (var org in specType)
                    {
                        Console.WriteLine($"- {org.Name}, Адрес: {org.Address}, Телефон: {org.Phone}");
                    }
                }
                else
                {
                    Console.WriteLine("Организаций данного типа не найдено.");
                }
            }
            else
            {
                Console.WriteLine("Неверный тип организации.");
            }
        }
    }
}
