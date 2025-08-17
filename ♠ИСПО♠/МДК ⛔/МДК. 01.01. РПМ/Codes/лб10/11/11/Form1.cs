using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace _11
{
    public partial class Form1 : Form
    {
        private List<Computer> computers = new List<Computer>();
        private string filename = "computers.txt";

        public Form1()
        {
            InitializeComponent();
            LoadComputers();
        }

        private void LoadComputers()
        {
            if (File.Exists(filename))
            {
                try
                {
                    string[] lines = File.ReadAllLines(filename);
                    computers = lines.Select(line =>
                    {
                        string[] parts = line.Split(',');
                        return new Computer { Name = parts[0], Frequency = double.Parse(parts[1]), RAM = double.Parse(parts[2]) };
                    }).ToList();
                    UpdateListBox();
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка загрузки данных: {ex.Message}");
                }
            }
        }

        private void SaveComputers()
        {
            try
            {
                string[] lines = computers.Select(c => $"{c.Name},{c.Frequency},{c.RAM}").ToArray();
                File.WriteAllLines(filename, lines);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка сохранения данных: {ex.Message}");
            }
        }

        private void UpdateListBox()
        {
            listBox1.Items.Clear();
            listBox1.Items.AddRange(computers.ToArray());
        }

        private void buttonAdd_Click(object sender, EventArgs e)
        {
            InputForm inputForm = new InputForm();
            if (inputForm.ShowDialog() == DialogResult.OK)
            {
                computers.Add(inputForm.Computer);
                UpdateListBox();
            }
        }

        private void buttonDelete_Click(object sender, EventArgs e)
        {
            if (listBox1.SelectedItem != null)
            {
                computers.Remove((Computer)listBox1.SelectedItem);
                UpdateListBox();
            }
        }

        private void buttonEdit_Click(object sender, EventArgs e)
        {
            if (listBox1.SelectedItem != null)
            {
                Computer selectedComputer = (Computer)listBox1.SelectedItem;
                InputForm inputForm = new InputForm(selectedComputer);
                if (inputForm.ShowDialog() == DialogResult.OK)
                {
                    computers[computers.IndexOf(selectedComputer)] = inputForm.Computer;
                    UpdateListBox();
                }
            }
        }

        private void buttonSave_Click(object sender, EventArgs e)
        {
            SaveComputers();
        }

        private void buttonFind_Click(object sender, EventArgs e)
        {
            if (computers.Count == 0)
            {
                MessageBox.Show("Список компьютеров пуст.");
                return;
            }

            var minFrequencyComputer = computers.OrderBy(c => c.Frequency).First();
            var maxRAMComputer = computers.OrderByDescending(c => c.RAM).First();

            MessageBox.Show($"Компьютер с минимальной частотой: {minFrequencyComputer}\nКомпьютер с максимальным объемом ОЗУ: {maxRAMComputer}");
        }

        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            // Этот обработчик можно использовать для дополнительной логики, например, отображения выбранного компьютера в отдельных текстовых полях.
        }
    }

    public class Computer
    {
        public string Name { get; set; }
        public double Frequency { get; set; }
        public double RAM { get; set; }

        public override string ToString()
        {
            return $"Название: {Name}, Тактовая частота: {Frequency:F2} ГГц, ОЗУ: {RAM:F2} ГБ";
        }
    }
}
