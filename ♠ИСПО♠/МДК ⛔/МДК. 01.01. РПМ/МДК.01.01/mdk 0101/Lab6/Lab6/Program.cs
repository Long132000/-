using System;
using System.Collections.Generic;

// Главный класс программы
class Program
{
    static void Main()
    {
        // Создаем список базового типа Tovar
        List<Tovar> items = new List<Tovar>();

        Tovar[] tovars = new Tovar[3];

        Tovar tovar1 = new Tovar(1, "Товар 1", 100m, 10);
        Tovar tovar2 = new Tovar(2, "Товар 2", 150m, 10);
        Tovar tovar3 = new Tovar(3, "Товар 3", 200m, 10);

        Product product1 = new Product(2, "Продукт 1", 150m, 5, 30);

        // Добавляем объекты в список
        items.Add(tovar1);
        items.Add(tovar2);
        items.Add(tovar3);
        items.Add(product1);

        // Демонстрация полиморфизма: вызов метода DisplayInfo для каждого объекта
        foreach (var item in items)
        {
            item.DisplayInfo();
        }

        // Создаем заказ
        Order order = new Order(101, DateTime.Now);

        // Добавляем товары в заказ
        order.AddItem(tovar1);
        order.AddItem(tovar1);
        order.AddItem(tovar2);
        order.AddItem(product1);

        // Отображаем детали заказа
        order.DisplayOrder();

        // Изменяем количество товаров в заказе
        order.IncreaseItem(tovar1);
        order.DecreaseItem(product1);

        Console.WriteLine("Обновленный заказ:");
        order.DisplayOrder();
    }
}
