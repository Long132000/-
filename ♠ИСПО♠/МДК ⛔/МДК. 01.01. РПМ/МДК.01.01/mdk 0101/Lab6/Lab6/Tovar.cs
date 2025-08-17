// Tovar.cs
using System;

public class Tovar
{
    private int code;
    private string name;
    private decimal price;
    private int quantity;

    public Tovar(int code, string name, decimal price, int quantity)
    {
        this.code = code;
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }

    public void DisplayInfo()
    {
        Console.WriteLine($"Код товара: {code}, Название: {name}, Цена: {price}, Количество: {quantity}");
    }

    public void IncreaseQuantity()
    {
        quantity++;
    }

    public void DecreaseQuantity()
    {
        if (quantity > 0)
        {
            quantity--;
        }
    }

    // Свойство для получения цены
    public decimal Price
    {
        get { return price; }
    }

    // Свойство для получения названия
    public string Name
    {
        get { return name; }
    }
}
