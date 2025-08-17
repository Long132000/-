using System;
using System.Drawing;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;

namespace Lab14
{
    public partial class Form3 : Form
    {
        private Chart targetChart;

        public Form3(Chart chart)
        {
            InitializeComponent();
            targetChart = chart;
            LoadCurrentSettings();
        }

        private void LoadCurrentSettings()
        {
            if (targetChart.Series.Count > 0)
            {
                numLineWidth.Value = targetChart.Series[0].BorderWidth;
                btnLineColor.BackColor = targetChart.Series[0].Color;
                btnBgColor.BackColor = targetChart.ChartAreas[0].BackColor;
                cbShowLegend.Checked = targetChart.Legends.Count > 0;
                cbShowTitle.Checked = targetChart.Titles.Count > 0;

                if (targetChart.Series[0].ChartType == SeriesChartType.Spline)
                    rbSpline.Checked = true;
                else
                    rbPoint.Checked = true;
            }
        }

        private void btnLineColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog
            {
                Color = btnLineColor.BackColor
            };

            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                btnLineColor.BackColor = colorDialog.Color;
                ApplySettings();
            }
        }

        private void btnBgColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog
            {
                Color = btnBgColor.BackColor
            };

            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                btnBgColor.BackColor = colorDialog.Color;
                ApplySettings();
            }
        }

        private void ApplySettings()
        {
            if (targetChart.Series.Count > 0)
            {
                targetChart.Series[0].BorderWidth = (int)numLineWidth.Value;
                targetChart.Series[0].Color = btnLineColor.BackColor;
                targetChart.Series[0].ChartType = rbSpline.Checked ?
                    SeriesChartType.Spline : SeriesChartType.Point;
                targetChart.ChartAreas[0].BackColor = btnBgColor.BackColor;

                if (cbShowLegend.Checked && targetChart.Legends.Count == 0)
                {
                    targetChart.Legends.Add(new Legend());
                }
                else if (!cbShowLegend.Checked && targetChart.Legends.Count > 0)
                {
                    targetChart.Legends.Clear();
                }

                if (cbShowTitle.Checked && targetChart.Titles.Count == 0)
                {
                    targetChart.Titles.Add(new Title());
                }
                else if (!cbShowTitle.Checked && targetChart.Titles.Count > 0)
                {
                    targetChart.Titles.Clear();
                }
            }
        }

        private void SettingChanged(object sender, EventArgs e)
        {
            ApplySettings();
        }
    }
}