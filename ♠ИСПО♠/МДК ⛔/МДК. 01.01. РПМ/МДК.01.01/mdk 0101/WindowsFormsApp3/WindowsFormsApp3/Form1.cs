using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp3
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        uint n = 0;
        ulong p = 1;
        private void button1_Click(object sender, EventArgs e)
        {
            n++;
            p *= 2;
            label2.Text = n.ToString();
            label3.Text = "= " + p.ToString();
            label1.Font = new Font("magneto", 12 + 10*n);

            if (n == 50) 
            {
                label3.Text = "Boo~~~";
            }
        }
    }
}
