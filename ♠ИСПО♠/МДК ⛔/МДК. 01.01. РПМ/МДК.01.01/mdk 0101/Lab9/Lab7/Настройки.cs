using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Lab7
{
    public partial class Настройки : Form
    {
        private Form1 mainForm;

        public Настройки(Form1 mainForm)
        {
            InitializeComponent();
            this.mainForm = mainForm;

            // Заполнение ComboBox ДО загрузки настроек
            comboBox1.Items.Add("Стандартный");
            comboBox1.Items.Add("Белый");
            comboBox1.Items.Add("Серый");
            comboBox1.Items.Add("Красный");
            comboBox1.Items.Add("Синий");

            comboBox2.Items.Add("Слева (сверху)");
            comboBox2.Items.Add("Центр(сверху)");
            comboBox2.Items.Add("Справа(сверху)");

            // Установка начального цвета
            ApplyColor();
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            if (mainForm == null) return;

            mainForm.WindowStateForm = checkBox1.Checked ? FormWindowState.Maximized : FormWindowState.Normal;

            Properties.Settings.Default.checkBox1State = checkBox1.Checked;
            Properties.Settings.Default.Save();
        }


        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            ApplyColor();
        }

        private void ApplyColor()
        {
            if (mainForm == null) return;

            switch (comboBox1.SelectedIndex)
            {
                case 0:
                    mainForm.BackColor = Color.Teal;
                    break;
                case 1:
                    mainForm.BackColor = Color.AntiqueWhite;
                    break;
                case 2:
                    mainForm.BackColor = Color.DimGray;
                    break;
                case 3:
                    mainForm.BackColor = Color.IndianRed;
                    break;
                case 4:
                    mainForm.BackColor = Color.AliceBlue;
                    break;
            }

            mainForm.Invalidate();
        }
        private void comboBox1_Click(object sender, EventArgs e)
        {
                
        }

        private void comboBox2_SelectedIndexChanged(object sender, EventArgs e)
        {
            //Изменение положения формы Form1 (с чётом того,что она не в полноэкранном режиме) Слева (сверху) Центр(сверху) Центр Справа(сверху)
            if (mainForm != null && !checkBox1.Checked) // Проверяем, что главная форма доступна и не в полноэкранном режиме
            {
                Rectangle screenBounds = Screen.PrimaryScreen.Bounds; // Получаем размеры основного экрана
                int formWidth = mainForm.Width;
                int formHeight = mainForm.Height;

                switch (comboBox2.SelectedIndex)
                {
                    case 0: // Слева сверху
                        mainForm.Location = new Point(screenBounds.Left, screenBounds.Top);
                        break;
                    case 1: // Центр сверху
                        mainForm.Location = new Point((screenBounds.Width - formWidth) / 2, screenBounds.Top);
                        break;
                    case 2: // Справа сверху
                        mainForm.Location = new Point(screenBounds.Right - formWidth, screenBounds.Top);
                        break;
                }
            }
        }
    }
}


