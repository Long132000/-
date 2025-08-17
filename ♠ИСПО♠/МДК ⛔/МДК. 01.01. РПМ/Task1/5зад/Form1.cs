namespace _5зад
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            button1.Text = "Левая кнопка";
            button1.Location = new Point(10, 70);
            Controls.Add(button1);

            button2.Text = "Правая кнопка";
            button2.Location = new Point(200, 70);
            Controls.Add(button2);

            label1.AutoSize = false;
            label1.Size = new Size(400, 50);
            label1.Location = new Point(10, 10);
            Controls.Add(label1);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            label1.Text = "Сработала левая кнопка";
            label1.ForeColor = Color.Blue;
            label1.TextAlign = ContentAlignment.MiddleLeft;
        }

        private void label1_Click(object sender, EventArgs e)
        {
            
        }

        private void button2_Click(object sender, EventArgs e)
        {
            label1.Text = "Сработала правая кнопка";
            label1.ForeColor = Color.Red;
            label1.TextAlign = ContentAlignment.MiddleRight;
        }
    }
}
