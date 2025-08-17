namespace _6зад
{
    using System;
    using System.Drawing;
    using System.Windows.Forms;

    public partial class Form1 : Form
    {
        private int X = 1; // Начальное значение
        private int fontSize = 8; // Начальный размер шрифта
        private const int maxFontSize = 20; // Максимальный размер шрифта
        public Form1()
        {
            InitializeComponent();
            label1.Text = "Нажмите кнопку, чтобы получить степень двойки:";
            label1.AutoSize = true;
            label1.Location = new Point(10, 10);
            Controls.Add(label1);

            label3.AutoSize = true;
            label3.Size = new Size(200, 50);
            label3.Location = new Point(10, 50);
            label3.Font = new Font(label3.Font.FontFamily, fontSize);
            Controls.Add(label3);

            button1.Text = "Удвоить";
            button1.Location = new Point(10, 100);
            button1.Click += button1_Click;
            Controls.Add(button1);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            X *= 2; // Удвоение значения X
            label3.Text = X.ToString(); // Вывод нового значения в label3

            // Увеличение размера шрифта
            if (fontSize < maxFontSize)
            {
                fontSize += 2;
                label3.Font = new Font(label3.Font.FontFamily, fontSize);
            }
        }

        private void label3_Click(object sender, EventArgs e)
        {

        }
    }
}
