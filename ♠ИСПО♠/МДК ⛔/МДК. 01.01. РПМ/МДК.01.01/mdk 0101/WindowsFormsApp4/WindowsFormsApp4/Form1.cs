using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp4
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (button1.Text == "Lightbulb (Turn on)")
            {
                pictureBox1.Image = Properties.Resources.Лампочка2;
                button1.Text = "Lightbulb (Turn off)";
                timer1.Enabled = true;
            }

            else
            {
                pictureBox1.Image = Properties.Resources.Лампочка1;
                button1.Text = "Lightbulb (Turn on)";
                timer1.Enabled = false;
                s = 0;
            }

        }

        uint s = 0;
        private void timer1_Tick(object sender, EventArgs e)
        {
            s++;
            label1.Text = "Lightbulb is turned on for " + s.ToString() + " seconds";
        }
    }
}
