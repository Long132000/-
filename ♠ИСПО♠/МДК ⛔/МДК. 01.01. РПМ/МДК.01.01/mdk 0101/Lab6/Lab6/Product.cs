// Product.cs
using System;

public class Product : Tovar
{
    private int shelfLife; // срок реализации в днях

    public Product(int code, string name, decimal price, int quantity, int shelfLife)
        : base(code, name, price, quantity)
    {
        this.shelfLife = shelfLife;
    }

    public new void DisplayInfo() // переопределение метода
    {
        base.DisplayInfo();
        Console.WriteLine($"Срок реализации: {shelfLife} дней");
    }
}
