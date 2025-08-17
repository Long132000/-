using System;
using System.Windows.Forms;

namespace Lab11
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void btnCreateArray_Click(object sender, EventArgs e)
        {
            if (int.TryParse(txtArraySize.Text, out int size) && size > 0)
            {
                dataGridView1.ColumnCount = size;
                dataGridView1.RowCount = 1;

                for (int i = 0; i < size; i++)
                {
                    dataGridView1.Columns[i].Name = $"Элемент {i + 1}";
                    dataGridView1.Rows[0].Cells[i].Value = "0";
                }
            }
            else
            {
                MessageBox.Show("Пожалуйста, введите корректный размер массива (целое число > 0)");
            }
        }

        private void btnProcessArray_Click(object sender, EventArgs e)
        {
            try
            {
                int size = dataGridView1.ColumnCount;
                double[] array = new double[size];

                for (int i = 0; i < size; i++)
                {
                    array[i] = Convert.ToDouble(dataGridView1.Rows[0].Cells[i].Value);
                }

                double[] processedArray = ArrayProcessor.ReversePositiveElements(array);

                dataGridView2.ColumnCount = size;
                dataGridView2.RowCount = 1;

                for (int i = 0; i < size; i++)
                {
                    dataGridView2.Columns[i].Name = $"Элемент {i + 1}";
                    dataGridView2.Rows[0].Cells[i].Value = processedArray[i].ToString();
                }
            }
            catch (FormatException)
            {
                MessageBox.Show("Пожалуйста, введите корректные числовые значения для всех элементов массива");
            }
        }
    }
}