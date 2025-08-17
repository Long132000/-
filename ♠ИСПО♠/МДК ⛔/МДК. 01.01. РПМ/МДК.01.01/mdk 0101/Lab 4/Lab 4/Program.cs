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
            public Organization (string name, orgType type, string address, string phone) // Конструктор организации (Конечно, Доппио))
            {
                Name = name;
                Type = type;
                Address = address;
                Phone = phone;
            }
        }

        static void Main()
        {
            List<Organization> organizations = new List<Organization> // Создаём организации (А в какой *непереводимый итальянский фольклор*?*)
            {
                new Organization("RKN", orgType.Неизвестно, "Москва, Ленинский проспект, дом 4, Строение 1А", "8(800)5553535"),
                new Organization("Passione", orgType.ИП, "n/a", "+39(339)7654321"),
                new Organization("AAA", orgType.ПАО, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "8(444)4444444"),
                new Organization("Denis`TablesForSleep", orgType.ИП, "СПб, Мебельная ул., дом 47, корпус 1", "8(812)3469696")
            };

            string search = "8(812)"; 
            var searchRes = organizations.Where(org => org.Phone.StartsWith(search)).ToList(); //Ищем организации с определённым началом номера телефона

            Console.WriteLine("Организации, телефоны которых начинаются на " + search + ":");
            foreach (var org in searchRes)
            {
                Console.WriteLine($"- {org.Name}, Адрес: {org.Address}, Телефон: {org.Phone}");
            }

            orgType searchType = orgType.ИП;
            var specType = organizations.Where(org => org.Type == searchType).ToList(); // Поиск организаций определённого типа

            Console.WriteLine($"Организации типа {searchType}:");
            foreach (var org in specType)
            {
                Console.WriteLine($"- {org.Name}, Адрес: {org.Address}, Телефон: {org.Phone}");
            }
        }
    }
}