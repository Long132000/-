using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        private int _clr = -1;
        private string _str;
        const string userRoot = "HKEY_CURRENT_USER";
        const string subkey = "RegistrySetValueExample";
        const string keyName = userRoot + "\\" + subkey;
        public Form1()
        {
            InitializeComponent();

            RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Deniska");
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            if ((int)Registry.GetValue(keyName, "clr", "-1") == 0)
                Collor(Color.DarkSlateGray, Color.Gray);
            if ((int)Registry.GetValue(keyName, "clr", "-1") == 1)
                Collor(Color.WhiteSmoke, Color.White);
            maskedTextBox1.Text = (string)Registry.GetValue(keyName, "text", "");
            Size = new Size((int)Registry.GetValue(keyName, "y", "808"), (int)Registry.GetValue(keyName, "x", "477"));
        }
        private void button1_Click(object sender, EventArgs e)//DeepPink цвет
        {
            RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Deniska");

            key.SetValue("Color", "DeepPink");
            key.Close();
            BackColor = System.Drawing.Color.DeepPink;
        }
        private void button2_Click(object sender, EventArgs e)//DarkBlue цвет
        {
            RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Deniska");

            key.SetValue("Color", "DarkBlue");
            key.Close();
            BackColor = System.Drawing.Color.DarkBlue;
        }
        private void button3_Click(object sender, EventArgs e)//PaleVioletRed цвет
        {
            RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Deniska");

            key.SetValue("Color", "PaleVioletRed");
            key.Close();
            BackColor = System.Drawing.Color.PaleVioletRed;
        }
        private void button4_Click(object sender, EventArgs e)//размер окна
        {
            string hght = textBox2.Text;
            string wdth = textBox3.Text;

            this.Height = Convert.ToInt32(hght);
            this.Width = Convert.ToInt32(wdth);
        }
        private void button5_Click(object sender, EventArgs e)//чтение из реестра и вывод на экран
        {
            RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Deniska");

            if (key != null)
            {
                int Height = int.Parse(key.GetValue("Height").ToString());
                int Width = int.Parse(key.GetValue("Width").ToString());
                this.Size = new Size(Width, Height);


                string color = (string)key.GetValue("Color");
                if (color == "Pink")
                    BackColor = System.Drawing.Color.Pink;
                else if (color == "IndianRed")
                    BackColor = System.Drawing.Color.IndianRed;
                if (color == "White")
                    BackColor = System.Drawing.Color.White;
            }
        }

        private void button6_click(object sender, EventArgs e)//сохранение
        {
            RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Deniska");

            key.SetValue("Height", this.Height);
            key.SetValue("Width", this.Width);
            key.Close();
        }
        private void Collor(Color buttonc, Color backgroundc)
        {
            button1.BackColor = buttonc;
            button2.BackColor = buttonc;
            button3.BackColor = buttonc;
            listBox1.BackColor = buttonc;
            this.BackColor = backgroundc;
            maskedTextBox1.BackColor = buttonc;
        }
        private void maskedTextBox1_TextChanged(object sender, EventArgs e)
        {
            _str = maskedTextBox1.Text;
            Registry.SetValue(keyName, "text", _str);
        }
    }
}
