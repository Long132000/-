using Lab14;
using System;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;

namespace Lab14
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }
}