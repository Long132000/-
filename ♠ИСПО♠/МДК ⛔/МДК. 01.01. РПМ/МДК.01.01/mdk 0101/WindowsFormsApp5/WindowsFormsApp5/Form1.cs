using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp5
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            System.Drawing.Drawing2D.GraphicsPath Form_Path = new System.Drawing.Drawing2D.GraphicsPath();
            Form_Path.AddEllipse(0, 0, this.Width, this.Height);
            Region Form_Region = new Region(Form_Path);
            this.Region = Form_Region;

            /*Form_Path.AddEllipse(0, 0, this.Width, this.Height);
            Region button_Region = new Region(Form_Path);
            button1.Region = button_Region;*/
        }

        private void Form1_MouseMove(object sender, MouseEventArgs e)
        {
            button1.Size = new Size(e.X, e.Y);
        }

        private void Form1_MouseMove_1(object sender, MouseEventArgs e)
        {
            button1.Location = new Point (e.X, e.Y);
            label1.Text = $"X: {e.X}; Y: {e.Y}";
        }

        private void Form1_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == (char)Keys.Escape)
            { 
                this.Close();
            }
        }
    }
}
