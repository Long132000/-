using System;
using System.Windows.Forms;

namespace _11
{
    public partial class InputForm : Form
    {
        public Computer Computer { get; set; }

        public InputForm()
        {
            InitializeComponent();
        }

        public InputForm(Computer computer) : this()
        {
            Computer = computer ?? new Computer();
            textBox1.Text = Computer.Name;
            textBox2.Text = Computer.Frequency.ToString();
            textBox3.Text = Computer.RAM.ToString();
        }

        private void buttonOK_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(textBox1.Text) ||
                !double.TryParse(textBox2.Text, out double frequency) ||
                !double.TryParse(textBox3.Text, out double ram) ||
                frequency <= 0 || ram <= 0)
            {
                MessageBox.Show("Пожалуйста, введите корректные данные. Частота и объём ОЗУ должны быть положительными числами.");
                return;
            }

            Computer = new Computer { Name = textBox1.Text, Frequency = frequency, RAM = ram };
            DialogResult = DialogResult.OK;
            Close();
        }

        private void buttonCancel_Click(object sender, EventArgs e)
        {
            DialogResult = DialogResult.Cancel;
            Close();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
