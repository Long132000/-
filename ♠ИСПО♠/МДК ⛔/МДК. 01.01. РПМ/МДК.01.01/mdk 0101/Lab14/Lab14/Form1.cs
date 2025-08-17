using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace Lab14
{
    public partial class Form1 : Form
    {
        public delegate void Del(double[] x, double[] y, string title);
        private Del myDelegate;
        private Form2 form2;

        public delegate double Fun(double x);

        public Form1()
        {
            InitializeComponent();
            btnCompute.Enabled = false;
            rbStep.Checked = true;
            txtPoints.Enabled = false;
        }

        private void btnCompute_Click(object sender, EventArgs e)
        {
            try
            {
                double Xn = double.Parse(txtXStart.Text);
                double Xk = double.Parse(txtXEnd.Text);
                double a = double.Parse(txtCoeff.Text);

                Fun selectedFunction = null;
                string title = "";

                if (rbFunc1.Checked)
                {
                    selectedFunction = x => a * Math.Exp(x);
                    title = "a * e^x";
                }
                else if (rbFunc2.Checked)
                {
                    selectedFunction = x => a * Math.Exp(2 * x);
                    title = "a * e^(2x)";
                }
                else if (rbFunc3.Checked)
                {
                    selectedFunction = x => -a * Math.Exp(x);
                    title = "-a * e^x";
                }

                double[] xValues, yValues;

                if (rbStep.Checked)
                {
                    double dX = double.Parse(txtStep.Text);
                    FunctionByStep(selectedFunction, Xn, Xk, dX, out xValues, out yValues);
                }
                else
                {
                    int n = int.Parse(txtPoints.Text);
                    FunctionByPoints(selectedFunction, Xn, Xk, n, out xValues, out yValues);
                }

                if (Application.OpenForms.Count < 2 || form2 == null || form2.IsDisposed)
                {
                    form2 = new Form2();
                    myDelegate = new Del(form2.RefreshDiagram);
                    form2.Show();
                }
                myDelegate(xValues, yValues, title);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка: {ex.Message}", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void FunctionByStep(Fun F, double Xn, double Xk, double dX,
                                   out double[] xValues, out double[] yValues)
        {
            List<double> xList = new List<double>();
            List<double> yList = new List<double>();

            if (dX > 0)
            {
                for (double x = Xn; x <= Xk; x += dX)
                {
                    xList.Add(x);
                    yList.Add(F(x));
                }
            }
            else
            {
                for (double x = Xn; x >= Xk; x += dX)
                {
                    xList.Add(x);
                    yList.Add(F(x));
                }
            }

            xValues = xList.ToArray();
            yValues = yList.ToArray();
        }

        private void FunctionByPoints(Fun F, double Xn, double Xk, int n,
                                    out double[] xValues, out double[] yValues)
        {
            if (n < 1) throw new ArgumentException("Количество точек должно быть ≥1");

            xValues = new double[n];
            yValues = new double[n];

            if (n == 1)
            {
                xValues[0] = Xn;
                yValues[0] = F(Xn);
                return;
            }

            double step = (Xk - Xn) / (n - 1);
            for (int i = 0; i < n; i++)
            {
                xValues[i] = Xn + i * step;
                yValues[i] = F(xValues[i]);
            }
        }

        private void ValidateInputs(object sender, EventArgs e)
        {
            bool stepMode = rbStep.Checked;
            bool pointsMode = rbPoints.Checked;

            bool inputsValid =
                !string.IsNullOrWhiteSpace(txtXStart.Text) &&
                !string.IsNullOrWhiteSpace(txtXEnd.Text) &&
                !string.IsNullOrWhiteSpace(txtCoeff.Text) &&
                (rbFunc1.Checked || rbFunc2.Checked || rbFunc3.Checked);

            if (stepMode)
            {
                inputsValid &= !string.IsNullOrWhiteSpace(txtStep.Text);
            }
            else if (pointsMode)
            {
                inputsValid &= !string.IsNullOrWhiteSpace(txtPoints.Text);
            }

            btnCompute.Enabled = inputsValid;
        }

        private void rbStep_CheckedChanged(object sender, EventArgs e)
        {
            txtStep.Enabled = rbStep.Checked;
            txtPoints.Enabled = rbPoints.Checked;
            ValidateInputs(sender, e);
        }
    }
}