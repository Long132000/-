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
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string text = textBox1.Text;
            int uppercaseCount = 0; int lowercaseCount = 0; int vowels = 0; int consonants = 0;
            string vowelsList = "АОИЫЕУЮЯЁЭAEOIUаоиыеуюяёaeoiu"; 

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

                if (char.IsLetter(c))
                {
                    if (vowelsList.Contains(c))
                    {
                        vowels++;
                    }
                    else { consonants++; }
                }
            }

            label2.Text =  $"Заглавных букв: {uppercaseCount}";
            label3.Text = $"Строчных букв: {lowercaseCount}";
            label5.Text = $"Гласных букв: {vowels}";
            label6.Text = $"Согласных букв: {consonants}";
        }
    }
}






