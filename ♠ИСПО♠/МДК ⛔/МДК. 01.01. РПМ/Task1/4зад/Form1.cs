using System;
using System.Drawing;
using System.Windows.Forms;

namespace _4зад
{
    public partial class Form1 : Form
    {

        
        
        private int clickCount = 0;
        private int labelOffset = 0;
        public Form1()
        {
            button1 = new Button();
            label1 = new Label();

            button1.Text = "Нажми меня";
            button1.Location = new Point(10, 10);
            button1.Click += new EventHandler(button1_Click);

            label1.Text = "Количество нажатий: 0";
            label1.Location = new Point(10, 50);
            label1.AutoSize = true;

            Controls.Add(button1);
            Controls.Add(label1);

        }

        private void button1_Click(object? sender, EventArgs e)
        {
            clickCount++;
            labelOffset += 5;

            label1.Text = "Количество нажатий: " + clickCount;
            label1.Location = new Point(10, 50 + labelOffset);
            label1.ForeColor = (clickCount % 2 == 0) ? Color.Red : Color.Blue;
        }

        
    }
}