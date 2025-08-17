using System;
using System.Drawing;
using System.Windows.Forms;

namespace Лабораторная__13
{
    public partial class settings : Form {
        private Form1 Form1;
        public settings() {
            InitializeComponent();
        }
        private void settings_Load(object sender, EventArgs e) {
            Form1 = (Form1)Owner;
            numericUpDown1.Value = Form1.MySize;
            trackBar1.Value = Form1.MySpeed;
            label1.BackColor = Form1.MyColor;
            if (Form1.MyDirection) radioButton1.Checked = true;
            else radioButton2.Checked = true;

        }

        private void button1_Click(object sender, EventArgs e) {
            ColorDialog colorDialog = new ColorDialog();
            colorDialog.Color = label1.BackColor;
            if (colorDialog.ShowDialog() == DialogResult.OK) {
                Form1.MyColor = colorDialog.Color;
                label1.BackColor = colorDialog.Color;
            }
        }

        private void numericUpDown1_ValueChanged(object sender, EventArgs e) {
            Form1.MySize = (int)numericUpDown1.Value;
        }

        private void trackBar1_Scroll(object sender, EventArgs e) {
            Form1.MySpeed = trackBar1.Value;
        }
        private void radioButton2_CheckedChanged(object sender, EventArgs e) {
            Form1.MyDirection = radioButton1.Checked;
        }
        private void button2_Click(object sender, EventArgs e) {
            numericUpDown1.Value = 40;
            Form1.MySize = (int)numericUpDown1.Value;
            radioButton1.Checked = true;
            Form1.MyDirection = radioButton1.Checked;
            trackBar1.Value = 100;
            Form1.MySpeed = trackBar1.Value;
            label1.BackColor = Color.Red;
            Form1.MyColor = label1.BackColor;
        }

        private void numericUpDown1_KeyPress(object sender, KeyPressEventArgs e) {
            e.KeyChar = '\0';
        }
    }
}


