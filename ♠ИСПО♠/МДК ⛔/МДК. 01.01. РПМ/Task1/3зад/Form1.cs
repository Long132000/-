using System;

namespace _3зад
{
    public partial class Form1 : Form
    {
        private Random random;
        public Form1()
        {
            InitializeComponent();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            double a = 3.2;
            double b = 9.4;
            double area = a * b;
            textBox1.Text = $"{area}";
        }

        private void button2_Click(object sender, EventArgs e)
        {
            random = new Random();
            double a = random.Next(1, 20) + random.NextDouble(); // случайное значение от 1 до 20
            double b = random.Next(1, 20) + random.NextDouble(); // случайное значение от 1 до 20
            double area = a * b;
            textBox2.Text = $"Случайные стороны: a = {a:F2} см, b = {b:F2} см. Площадь: {area:F2} см².";
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
