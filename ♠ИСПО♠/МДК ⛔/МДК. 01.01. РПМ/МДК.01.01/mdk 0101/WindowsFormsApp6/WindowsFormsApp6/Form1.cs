using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp6
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button3_MouseClick(object sender, MouseEventArgs e)
        {
            if (sender==button1)
            {
                label1.Left -= 5;
                label1.Top -= 5;
            }

            if (sender == button2)
            {
                label1.Top -= 5;
            }

            if (sender == button3)
            {
                label1.Left += 5;
                label1.Top -= 5;
            }

            if (sender == button4)
            {
                label1.Left -= 5;
            }

            if (sender == button6)
            {
                label1.Left += 5;
            }

            if (sender == button7)
            {
                label1.Left -= 5;
                label1.Top += 5;
            }

            if (sender == button8)
            {
                label1.Top += 5;
            }

            if (sender == button9)
            {
                label1.Left += 5;
                label1.Top += 5;
            }
        }
    }
}
