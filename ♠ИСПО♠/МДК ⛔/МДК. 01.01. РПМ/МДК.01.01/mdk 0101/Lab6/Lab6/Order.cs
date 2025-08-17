// Order.cs
using System;
using System.Collections.Generic;

public class Order
{
    private int orderNumber;
    private DateTime orderDate;
    private string status;
    private Dictionary<Tovar, int> items;

    public Order(int orderNumber, DateTime orderDate)
    {
        this.orderNumber = orderNumber;
        this.orderDate = orderDate;
        this.status = "Формируется";
        items = new Dictionary<Tovar, int>();
    }

    public void AddItem(Tovar tovar)
    {
        if (items.ContainsKey(tovar))
        {
            items[tovar]++;
        }
        else
        {
            items[tovar] = 1;
        }
    }

    public void IncreaseItem(Tovar tovar)
    {
        if (items.ContainsKey(tovar))
        {
            items[tovar]++;
        }
    }

    public void DecreaseItem(Tovar tovar)
    {
        if (items.ContainsKey(tovar) && items[tovar] > 0)
        {
            items[tovar]--;
        }
    }

    public void RemoveItem(Tovar tovar)
    {
        if (items.ContainsKey(tovar))
        {
            items.Remove(tovar);
        }
    }

    public decimal CalculateTotal()
    {
        decimal total = 0;
        foreach (var item in items)
        {
            total += item.Key.Price * item.Value; // Используем свойство Price
        }
        return total;
    }

    public void DisplayOrder()
    {
        Console.WriteLine($"Заказ номер: {orderNumber}, Дата: {orderDate}, Статус: {status}");
        foreach (var item in items)
        {
            Console.WriteLine($"{item.Key.Name} - {item.Value} шт."); // Используем свойство Name
        }
        Console.WriteLine($"Полная стоимость: {CalculateTotal()}");
    }
}
