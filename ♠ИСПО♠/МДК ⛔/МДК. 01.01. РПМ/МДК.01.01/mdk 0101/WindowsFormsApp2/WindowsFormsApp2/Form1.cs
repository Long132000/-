using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp2
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            label1.Text = "Right button workd";
            label1.ForeColor = Color.DarkRed;
            label1.TextAlign = ContentAlignment.MiddleRight;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (sender == button1)
            {
                label1.Text = "Left button workd";
                label1.ForeColor = Color.DarkBlue;
                label1.TextAlign = ContentAlignment.MiddleLeft;
            }
            else 
            {
                label1.Text = "Right button workd";
                label1.ForeColor = Color.DarkRed;
                label1.TextAlign = ContentAlignment.MiddleRight;
            }
        }
    }
}
