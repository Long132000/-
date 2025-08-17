using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Windows.Forms;

namespace Лабораторная__12
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        int countOfColumns = 1;
        int countOfRows = 1;
        int vectorCountOfRows = 1;

        private void button1_Click(object sender, EventArgs e)
        {
            int n = (int)numericUpDown1.Value;
            int m = (int)numericUpDown2.Value;
            double[,] array = new double[n, m];
            double[] vector = new double[m];
            for (int i = 0; i < countOfRows; i++)
            {
                for (int j = 0; j < countOfColumns; j++)
                {
                    if (dataGridView1.Rows[i].Cells[j].Value == null || double.Parse(dataGridView1.Rows[i].Cells[j].Value.ToString()) == 0)
                        array[i, j] = 0;
                    else
                        array[i, j] = double.Parse(dataGridView1.Rows[i].Cells[j].Value.ToString());
                }
            }
            for (int i = 0; i < countOfColumns; i++)
            {
                if (dataGridView2.Rows[i].Cells[0].Value == null || double.Parse(dataGridView2.Rows[i].Cells[0].Value.ToString()) == 0)
                    vector[i] = 0;
                else
                    vector[i] = double.Parse(dataGridView2.Rows[i].Cells[0].Value.ToString());
            }

            //Функция
            double[] C = MyArray.FindC(array, vector, (int)numericUpDown1.Value, (int)numericUpDown2.Value);

            for (int i = 0; i < countOfColumns; i++)
            {
                    dataGridView3.Rows[i].Cells[0].Value = C[i];
            }
            dataGridView3.Visible = true;
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton1.Checked)
            {
                for (int i = 0; i < countOfRows; i++)
                {
                    for (int j = 0; j < countOfColumns; j++)
                    {
                        dataGridView1.Rows[i].Cells[j].Value = 0;
                    }
                }
                for (int i = 0; i < countOfColumns; i++)
                {
                    dataGridView2.Rows[i].Cells[0].Value = 0;
                    dataGridView3.Rows[i].Cells[0].Value = 0;
                }
            }
            else if (radioButton2.Checked)
            {
                Random random = new Random();
                for (int i = 0; i < countOfRows; i++)
                {
                    for (int j = 0; j < countOfColumns; j++)
                    {
                        dataGridView1.Rows[i].Cells[j].Value = random.Next(-100, 100);
                    }
                }
                for (int i = 0; i < countOfColumns; i++)
                {
                    dataGridView2.Rows[i].Cells[0].Value = random.Next(-100, 100);
                    dataGridView3.Rows[i].Cells[0].Value = 0;
                }
            }
            else if (radioButton3.Checked && sender == radioButton3)
            {
                if (openFileDialog1.ShowDialog() == DialogResult.OK)
                {
                    string inFile = File.ReadAllText(openFileDialog1.FileName);
                    string[] rows = inFile.Split(new char[2] { '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
                    string[] inRows = rows[0].Split(' ');

                    dataGridView1.Rows.Clear();
                    dataGridView1.Columns.Clear();

                    countOfRows = rows.Length;
                    countOfColumns = inRows.Length;

                    numericUpDown1.Value = countOfRows;
                    numericUpDown2.Value = countOfColumns;

                    dataGridView1.RowCount = countOfRows;
                    dataGridView1.ColumnCount = countOfColumns;
                    dataGridView2.RowCount = countOfColumns;
                    dataGridView3.RowCount = countOfColumns;

                    for (int i = 0; i < countOfRows; i++)
                    {
                        string[] inRow = rows[i].Split(' ');

                        for (int j = 0; j < countOfColumns; j++)
                        {
                            try
                            {
                                dataGridView1.Rows[i].Cells[j].Value = double.Parse(inRow[j]);
                            }
                            catch (Exception ex)
                            {
                                MessageBox.Show($"Ошибка при парсинге данных: {ex.Message}");
                            }
                        }
                    }

                    for (int i = 0; i < countOfRows; i++)
                    {
                        string[] inRow = rows[i].Split(' ');
                        try
                        {
                            dataGridView2.Rows[i].Cells[0].Value = double.Parse(inRow[i]);
                            dataGridView3.Rows[i].Cells[0].Value = 0;
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show($"Ошибка при парсинге данных: {ex.Message}");
                        }
                    }
                }
            }
        }

        private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        {

            if (numericUpDown1.Value > countOfRows)
            {
                dataGridView1.RowCount++;
                countOfRows++;
                if (radioButton1.Checked)
                {
                    for (int i = 0; i < countOfColumns; i++)
                    {
                        dataGridView1.Rows[countOfRows - 1].Cells[i].Value = 0;
                    }
                }
                else if (radioButton2.Checked)
                {
                    Random random = new Random();
                    for (int i = 0; i < countOfColumns; i++)
                    {
                        dataGridView1.Rows[countOfRows - 1].Cells[i].Value = random.Next(-100, 100);
                    }
                }
            }
            else if (numericUpDown1.Value < countOfRows)
            {
                countOfRows--;
                dataGridView1.RowCount--;
            }
        }

        private void numericUpDown2_ValueChanged(object sender, EventArgs e)
        {
            if (numericUpDown2.Value > countOfColumns)
            {
                dataGridView1.ColumnCount++;
                dataGridView2.RowCount++;
                dataGridView3.RowCount++;
                countOfColumns++;
                if (radioButton1.Checked)
                {
                    for (int i = 0; i < countOfRows; i++)
                    {
                        dataGridView1.Rows[i].Cells[countOfColumns - 1].Value = 0;
                    }
                    for (int i = countOfColumns - 1; i < countOfColumns; i++)
                    {
                        dataGridView2.Rows[i].Cells[0].Value = 0;
                        dataGridView3.Rows[i].Cells[0].Value = 0;
                    }
                }
                else if (radioButton2.Checked)
                {
                    Random random = new Random();
                    for (int i = 0; i < countOfRows; i++)
                    {
                        dataGridView1.Rows[i].Cells[countOfColumns - 1].Value = random.Next(-100, 100);
                    }
                    for (int i = countOfColumns - 1; i < countOfColumns; i++)
                    {
                        dataGridView2.Rows[i].Cells[0].Value = random.Next(-100, 100);
                        dataGridView3.Rows[i].Cells[0].Value = 0;
                    }
                }
                }
                else if (numericUpDown2.Value < countOfColumns)
                {
                    countOfColumns--;
                    dataGridView2.RowCount--;
                    dataGridView3.RowCount--;
                    dataGridView1.ColumnCount--;
                }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            dataGridView1.ColumnCount = countOfColumns;
            dataGridView1.RowCount = countOfRows;
            dataGridView1.Rows[countOfRows - 1].Cells[countOfColumns - 1].Value = 0;

            dataGridView2.RowCount = countOfColumns;
            dataGridView2.Rows[countOfRows - 1].Cells[0].Value = 0;
            dataGridView3.RowCount = countOfColumns;
            dataGridView3.Rows[countOfRows - 1].Cells[0].Value = 0;
        }

        private void dataGridView1_EditingControlShowing(object sender, DataGridViewEditingControlShowingEventArgs e)
        {
            e.Control.KeyPress += new KeyPressEventHandler(dataGridView1_KeyPress);
        }

        private void dataGridView1_KeyPress(object sender, KeyPressEventArgs e)
        {
            string tx = dataGridView1.EditingControl.Text; // это текст ячейки
            if (e.KeyChar == (char)Keys.Back)
                return;
            if ((e.KeyChar >= '0') && (e.KeyChar <= '9')) // цифры разрешены
                return;
            if (e.KeyChar == '-' && tx.Length == 0) // минус разрешён в начале строки
                return;
            if (e.KeyChar == ',' && !tx.Contains(","))
                return;

            e.KeyChar = '\0';
        }

        private void dataGridView2_KeyPress(object sender, KeyPressEventArgs e)
        {
            string tx = dataGridView2.EditingControl.Text; // это текст ячейки
            if (e.KeyChar >= '0' && e.KeyChar <= '9') return;
            if (e.KeyChar == ',' && (dataGridView2.EditingControl).Text != "" && (dataGridView2.EditingControl).Text != "-" && (dataGridView2.EditingControl).Text.IndexOf(',') == -1) return;
            if (e.KeyChar == '-' && (dataGridView2.EditingControl).Text.Length == 0) return;
            if (e.KeyChar == (char)Keys.Back) return;

            e.KeyChar = '\0';
        }

        private void dataGridView2_EditingControlShowing(object sender, DataGridViewEditingControlShowingEventArgs e)
        {
            e.Control.KeyPress += new KeyPressEventHandler(dataGridView2_KeyPress);
        }
    }
}
