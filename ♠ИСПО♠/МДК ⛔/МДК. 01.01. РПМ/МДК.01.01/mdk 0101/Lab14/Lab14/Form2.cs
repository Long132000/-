using System;
using System.Drawing;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using System.IO;

namespace Lab14
{
    public partial class Form2 : Form
    {
        public Form2()
        {
            InitializeComponent();
        }

        public void RefreshDiagram(double[] xValues, double[] yValues, string title)
        {
            chart1.Series.Clear();
            chart1.Titles.Clear();
            chart1.Legends.Clear();

            Series series = new Series(title)
            {
                ChartType = SeriesChartType.Spline,
                BorderWidth = 2,
                Color = Color.Red
            };

            chart1.Series.Add(series);
            chart1.ChartAreas[0].BackColor = Color.White;
            chart1.Legends.Add(title);
            chart1.Legends[0].Font = new Font("Tahoma", 10);
            chart1.Titles.Add(title);
            chart1.Titles[0].Font = new Font("Tahoma", 12, FontStyle.Bold);

            chart1.Series[title].Points.DataBindXY(xValues, yValues);
            chart1.Series[title].ToolTip = "X = #VALX, Y = #VALY";
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveDialog = new SaveFileDialog
            {
                Filter = "PNG Image|*.png",
                Title = "Сохранить график как PNG"
            };

            if (saveDialog.ShowDialog() == DialogResult.OK)
            {
                using (MemoryStream ms = new MemoryStream())
                {
                    chart1.SaveImage(ms, ChartImageFormat.Png);
                    byte[] data = ms.ToArray();
                    File.WriteAllBytes(saveDialog.FileName, data);
                }
                MessageBox.Show("График успешно сохранен!", "Сохранение",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void btnSettings_Click(object sender, EventArgs e)
        {
            Form3 settingsForm = new Form3(chart1);
            settingsForm.Show();
        }
    }
}