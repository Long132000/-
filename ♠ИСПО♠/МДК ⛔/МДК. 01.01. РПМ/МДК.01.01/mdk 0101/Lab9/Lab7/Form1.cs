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
        bool upc = false;
        bool lwc = false;
        bool vow = false;
        bool cns = false;
        public string vowelsList = "";
        public string consonantsList = "";


        public Form1()
        {
            InitializeComponent();
        }
        private Color backColor; // Поле для хранения цвета фона

        public Color BackColor // Публичное свойство для доступа к BackColor
        {
            get { return this.backColor; }
            set
            {
                this.backColor = value;
                base.BackColor = value; // Устанавливаем цвет фона для формы
                this.Invalidate();
            }
        }

        private FormWindowState _windowState; // Приватное поле для хранения состояния

        public FormWindowState WindowStateForm // Публичное свойство для доступа
        {
            get { return _windowState; }
            set
            {
                _windowState = value;
                WindowState = value; // Обновляем WindowState формы
                Size = value == FormWindowState.Maximized ? MaximumSize : new Size(800, 600); // Устанавливаем размер
            }
        }

        private Size size; // Поле для хранения размера окна

        public Size Size // Публичное свойство для доступа к Size
        {
            get { return this.size; }
            set
            {
                this.size = value;
                base.Size = value; // Устанавливаем размер формы
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string text = textBox1.Text;
            int uppercaseCount = 0; int lowercaseCount = 0; int vowels = 0; int consonants = 0;
            foreach (char c in text)
            {
                if (upc == true)
                {
                    if (char.IsUpper(c))
                    {
                        uppercaseCount++;
                    }
                }

                if (lwc == true)
                {
                    if (char.IsLower(c))
                    {
                        lowercaseCount++;
                    }
                }

                
                if (char.IsLetter(c))
                {
                    if (vow == true)
                    {
                        if (vowelsList.Contains(c))
                        {
                            vowels++;
                        }
                    }
                    
                    if (cns == true)
                    {
                        if (consonantsList.Contains(c))
                        {
                            consonants++;
                        }
                    }
                }
            }

            label2.Text =  $"Заглавных букв: {uppercaseCount}";
            label3.Text = $"Строчных букв: {lowercaseCount}";
            label5.Text = $"Гласных букв: {vowels}";
            label6.Text = $"Согласных букв: {consonants}";
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void label7_Click(object sender, EventArgs e)
        {

        }

        private void выводимыеДанныеToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void toolStripLabel1_Click(object sender, EventArgs e)
        {

        }

        private void toolStripLabel1_Click_1(object sender, EventArgs e)
        {
            if (upc == true)
            {
                upc = false;
                toolStripLabel1.ForeColor = Color.Black;
            }
            else
            {
                upc = true;
                toolStripLabel1.ForeColor = Color.Teal;
            }
        }

        private void toolStripLabel2_Click(object sender, EventArgs e)
        {
            if (lwc == true)
            {
                lwc = false;
                toolStripLabel2.ForeColor = Color.Black;
            }
            else
            {
                lwc = true;
                toolStripLabel2.ForeColor = Color.Teal;
            }
        }

        private void toolStripLabel3_Click(object sender, EventArgs e)
        {
            if (vow == true)
            {
                vow = false;
                toolStripLabel3.ForeColor = Color.Black;
            }
            else
            {
                vow = true;
                toolStripLabel3.ForeColor = Color.Teal;
            }
        }

        private void toolStripLabel4_Click(object sender, EventArgs e)
        {
            if (cns == true)
            {
                cns = false;
                toolStripLabel4.ForeColor = Color.Black;
            }
            else
            {
                cns = true;
                toolStripLabel4.ForeColor = Color.Teal;
            }
        }

        private void русскийToolStripMenuItem_Click(object sender, EventArgs e)
        {
            vowelsList = "АОИЫЕУЮЯЁЭаоиыеуюяё";
            consonantsList = "ЙЦКНГШЩЗХЪФВПРЛДЖЧСМТЬБйцкнгшщзхъфвпрлджчсмтьб";

        }

        private void английскийToolStripMenuItem_Click(object sender, EventArgs e)
        {
            vowelsList = "AEOIUYaeoiuy";
            consonantsList = "QWRTPSDFGHJKLZXCVBNMqwrtpsdfghjklzxcvbnm";
        }

        private void настройкиToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Настройки newForm = new Настройки(this);
            newForm.ShowDialog();
        }
    }
}






