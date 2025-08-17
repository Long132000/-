using System;
using System.Drawing;
using System.Windows.Forms;

namespace Laba_11
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            dataGridView1.RowCount = 1;
            dataGridView1.ColumnHeadersDefaultCellStyle.BackColor = Color.Red;
            for (int i = 0; i < dataGridView1.ColumnCount; i++)
            {
                dataGridView1.Rows[0].Cells[i].Value = 0;
            }
        }

        private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        {
            dataGridView1.RowCount = 1;
            dataGridView1.ColumnCount = (int)numericUpDown1.Value;
            for (int i = 0; i < dataGridView1.ColumnCount; i++)
            {
                dataGridView1.Columns[i].HeaderText = i.ToString();
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            int[] arr = new int[dataGridView1.ColumnCount];
            for (int i = 0; i < arr.Length; i++)
            {
                arr[i] = Convert.ToInt32(dataGridView1.Rows[0].Cells[i].Value);
            }

            // Перестраиваем массив
            int[] rearrangedArray = RearrangeArray(arr);

            // Заполняем ячейки DataGridView новыми значениями
            for (int i = 0; i < rearrangedArray.Length; i++)
            {
                dataGridView1.Rows[0].Cells[i].Value = rearrangedArray[i];
            }

            label2.Text = "Массив перестроен: положительные, затем отрицательные и нули.";
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton2.Checked)
            {
                Random rnd = new Random();
                for (int i = 0; i < dataGridView1.ColumnCount; i++)
                {
                    dataGridView1.Rows[0].Cells[i].Value = rnd.Next(-100, 100);
                }
            }
            else if (radioButton1.Checked)
            {
                for (int i = 0; i < dataGridView1.ColumnCount; i++)
                {
                    dataGridView1.Rows[0].Cells[i].Value = 0;
                }
            }
        }

        private void dataGridView1_KeyPress(object sender, KeyPressEventArgs e)
        {
            System.Windows.Forms.TextBox textBox = sender as System.Windows.Forms.TextBox;
            if ((e.KeyChar >= '0') && (e.KeyChar <= '9')) // цифры разрешены
                return;

            if (e.KeyChar == (char)Keys.Back) return;
            if (e.KeyChar == '-' && textBox.Text == "") return;

            e.KeyChar = '\0'; // остальные символы запрещены (игнорировать)
        }

        private void dataGridView1_EditingControlShowing(object sender, DataGridViewEditingControlShowingEventArgs e)
        {
            System.Windows.Forms.TextBox textBox = e.Control as System.Windows.Forms.TextBox;
            textBox.KeyPress -= new KeyPressEventHandler(dataGridView1_KeyPress);
            textBox.KeyPress += new KeyPressEventHandler(dataGridView1_KeyPress);
        }

        private int[] RearrangeArray(int[] arr)
        {
            int positiveCount = 0;
            int negativeCount = 0;

            // Подсчет количества положительных, отрицательных и нулей
            foreach (var number in arr)
            {
                if (number > 0) positiveCount++;
                else if (number < 0) negativeCount++;
            }

            // Создаем новый массив для распределения значений
            int[] result = new int[arr.Length];
            int index = 0;

            // Сначала положительные
            foreach (var number in arr)
            {
                if (number > 0)
                {
                    result[index++] = number;
                }
            }

            // Затем отрицательные
            foreach (var number in arr)
            {
                if (number < 0)
                {
                    result[index++] = number;
                }
            }

            // Затем нули
            foreach (var number in arr)
            {
                if (number == 0)
                {
                    result[index++] = number;
                }
            }

            return result;
        }
    }
}