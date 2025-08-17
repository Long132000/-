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
    public partial class Form1 : Form
    {
        public string vowelsList = "";
        public string consList = "";

        public Form1()
        {
            InitializeComponent();
            consList = ""; // Initialize consList here
        }
        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            UpdateVowelsList();
        }

        private void checkBox2_CheckedChanged(object sender, EventArgs e)
        {
            UpdateVowelsList();
        }

        private void UpdateVowelsList()
        {
            vowelsList = "";
            consList = ""; // Reset consList to avoid appending multiple times

            if (checkBox1.Checked)
            {
                vowelsList += "АОИЫЕУЮЯЁЭЫаоиыеуюяёэы";
                consList += "ЙйЦцКкНнГгШшЩщЗзХхЪъФфВвПпРрЛлДдЖжЧчСсМмТтЬьБб";
            }

            if (checkBox2.Checked)
            {
                vowelsList += "AEOIUYaeoiuy";
                consList += "QqWwRrTtPpSsDdFfGgHhJjKkLlZzXxCcVvBbNnMm";
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string text = textBox1.Text;
            int uppercaseCount = 0;
            int lowercaseCount = 0;
            int vowels = 0;
            int consonants = 0;

            foreach (char c in text)
            {
                if (char.IsUpper(c))
                {
                    uppercaseCount++;
                }

                if (char.IsLower(c))
                {
                    lowercaseCount++;
                }

                if (vowelsList.Contains(c))
                {
                    vowels++;
                }
                if (consList.Contains(c))
                {
                    consonants++;
                }
            }

            label2.Text = $"Заглавных букв: {uppercaseCount}";
            label3.Text = $"Строчных букв: {lowercaseCount}";
            label5.Text = $"Гласных букв: {vowels}";
            label6.Text = $"Согласных букв: {consonants}";
        }

        private void checkBox1_Click(object sender, EventArgs e)
        {

        }

        private void label7_Click(object sender, EventArgs e)
        {

        }

    }
}
