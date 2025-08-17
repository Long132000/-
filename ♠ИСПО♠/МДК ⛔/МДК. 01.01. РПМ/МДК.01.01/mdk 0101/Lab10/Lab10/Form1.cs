using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Lab10
{
    public partial class Form1 : Form
    {
        private List<Car> cars = new List<Car>();
        private string filePath = @"C:\Users\Egor\Documents\save.txt";

        public Form1()
        {
            InitializeComponent();
        }

        // Класс для хранения информации об автомобиле
        public class Car
        {
            public string Brand { get; set; }
            public int Power { get; set; }
            public double FuelConsumption { get; set; }

            public override string ToString()
            {
                return $"{Brand} - Мощность: {Power}, Расход топлива: {FuelConsumption}";
            }
        }

        // Метод для обновления отображения списка автомобилей
        private void UpdateComboBox()
        {
            comboBox1.Items.Clear();
            foreach (var car in cars)
            {
                comboBox1.Items.Add(car);
            }
        }

        // Добавление нового автомобиля в список
        private void button1_Click(object sender, EventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(textBox1.Text) && !string.IsNullOrWhiteSpace(textBox2.Text) && !string.IsNullOrWhiteSpace(textBox3.Text))
            {
                try
                {
                    var brand = textBox1.Text.Trim();
                    var power = int.Parse(textBox2.Text.Trim());
                    var fuelConsumption = double.Parse(textBox3.Text.Trim());

                    cars.Add(new Car { Brand = brand, Power = power, FuelConsumption = fuelConsumption });
                    UpdateComboBox();

                    ClearInputFields();
                }
                catch (FormatException ex)
                {
                    MessageBox.Show("Ошибка ввода данных.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            else
            {
                MessageBox.Show("Все поля должны быть заполнены.", "Предупреждение", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        // Изменение выбранного автомобиля
        private void button2_Click(object sender, EventArgs e)
        {
            if (comboBox1.SelectedItem is Car selectedCar)
            {
                if (!string.IsNullOrWhiteSpace(textBox1.Text) && !string.IsNullOrWhiteSpace(textBox2.Text) && !string.IsNullOrWhiteSpace(textBox3.Text))
                {
                    try
                    {
                        var brand = textBox1.Text.Trim();
                        var power = int.Parse(textBox2.Text.Trim());
                        var fuelConsumption = double.Parse(textBox3.Text.Trim());

                        selectedCar.Brand = brand;
                        selectedCar.Power = power;
                        selectedCar.FuelConsumption = fuelConsumption;

                        UpdateComboBox();

                        ClearInputFields();
                    }
                    catch (FormatException ex)
                    {
                        MessageBox.Show("Ошибка ввода данных.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
                else
                {
                    MessageBox.Show("Все поля должны быть заполнены.", "Предупреждение", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
            }
            else
            {
                MessageBox.Show("Сначала выберите автомобиль для редактирования.", "Предупреждение", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        // Удаление выбранного автомобиля
        private void button3_Click(object sender, EventArgs e)
        {
            if (comboBox1.SelectedItem is Car selectedCar)
            {
                cars.Remove(selectedCar);
                UpdateComboBox();
            }
            else
            {
                MessageBox.Show("Сначала выберите автомобиль для удаления.", "Предупреждение", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        // Загрузка списка из файла
        private void button4_Click(object sender, EventArgs e)
        {
            if (File.Exists(filePath))
            {
                try
                {
                    cars.Clear();
                    using (StreamReader reader = new StreamReader(filePath))
                    {
                        while (!reader.EndOfStream)
                        {
                            var line = reader.ReadLine().Split(',');
                            cars.Add(new Car { Brand = line[0], Power = int.Parse(line[1]), FuelConsumption = double.Parse(line[2]) });
                        }
                    }
                    UpdateComboBox();
                }
                catch (IOException ex)
                {
                    MessageBox.Show($"Ошибка чтения файла: {ex.Message}", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                catch (FormatException ex)
                {
                    MessageBox.Show($"Ошибка формата данных в файле: {ex.Message}", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            else
            {
                MessageBox.Show("Файл не найден.", "Предупреждение", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        // Сохранение списка в файл
        private void button5_Click(object sender, EventArgs e)
        {
            if (cars.Count > 0)
            {
                try
                {
                    using (StreamWriter writer = new StreamWriter(filePath))
                    {
                        foreach (var car in cars)
                        {
                            writer.WriteLine($"{car.Brand},{car.Power},{car.FuelConsumption}");
                        }
                    }
                    MessageBox.Show("Данные успешно сохранены.", "Успех", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                catch (IOException ex)
                {
                    MessageBox.Show($"Ошибка записи в файл: {ex.Message}", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            else
            {
                MessageBox.Show("Нет данных для сохранения.", "Предупреждение", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        // Сброс списка
        private void button6_Click(object sender, EventArgs e)
        {
            cars.Clear();
            UpdateComboBox();
            ClearInputFields();
        }

        // Поиск автомобиля с максимальной мощностью и минимальным расходом
        private void button7_Click(object sender, EventArgs e)
        {
            if (cars.Count > 0)
            {
                var maxPowerCar = cars.OrderByDescending(c => c.Power).First();
                var minFuelCar = cars.OrderBy(c => c.FuelConsumption).First();

                label5.Text = $"Автомобиль с максимальной мощностью: {maxPowerCar.ToString()}" +
                             Environment.NewLine +
                             $"Автомобиль с минимальным расходом топлива: {minFuelCar.ToString()}";
            }
            else
            {
                MessageBox.Show("Нет данных для анализа.", "Предупреждение", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        // Очистка полей ввода
        private void ClearInputFields()
        {
            textBox1.Clear();
            textBox2.Clear();
            textBox3.Clear();
        }
    }
}