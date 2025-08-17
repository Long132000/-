using System;
using System.Drawing;
using System.Windows.Forms;

namespace Лабораторная__13 {
    public partial class Form1 : Form {
        public Form1() {
            InitializeComponent();
        }

        int bigRadius = 170;   // Радиус большой окружности
        int smallRadius = 20;  // Радиус маленького кружка
        double angle = 0;       // Начальный угол (в радианах)
        double angleSpeed = 0.05f;  // Скорость изменения угла (угловая скорость)
        bool isClockwise = true;    // Направление движения: true — по часовой, false — против часовой
        int centerX, centerY; // Центр большой окружности

        SolidBrush brush = new SolidBrush(Color.Red); // Кисть для маленького кружка
        Rectangle rc; // Прямоугольная область для рисования маленького кружка

        public int MySpeed {
            get { return timer1.Interval; }
            set { timer1.Interval = value; }
        }

        public Color MyColor {
            get { return brush.Color; }
            set { brush.Color = value; }
        }

        public int MySize {
            get { return smallRadius * 2; }
            set { smallRadius = value / 2; }
        }

        public bool MyDirection {
            get { return isClockwise; }
            set { isClockwise = value; }
        }

        private void Form1_Paint(object sender, PaintEventArgs e) {
            // Центр большой окружности
            centerX = this.ClientSize.Width / 2;
            centerY = this.ClientSize.Height / 2;

            // Рисуем большую окружность
            e.Graphics.DrawEllipse(Pens.Black, centerX - bigRadius, centerY - bigRadius, bigRadius * 2, bigRadius * 2);

            // Смещённый радиус для движения маленького кружка внутри
            int innerRadius = bigRadius - smallRadius;

            // Рассчитываем координаты маленького кружка на внутренней дуге
            int x = (int)(centerX + innerRadius * Math.Cos(angle) - smallRadius);
            int y = (int)(centerY + innerRadius * Math.Sin(angle) - smallRadius);

            // Рисуем маленький кружок
            rc = new Rectangle(x, y, smallRadius * 2, smallRadius * 2);
            e.Graphics.FillEllipse(brush, rc);
        }

        private void timer1_Tick(object sender, EventArgs e) {
            // Увеличиваем или уменьшаем угол в зависимости от направления
            if (isClockwise) angle += angleSpeed;
            else angle -= angleSpeed;

            // Ограничиваем угол в пределах 0–2π
            if (angle >= 2 * Math.PI)
                angle -= 2 * Math.PI;
            else if (angle < 0)
                angle += 2 * Math.PI;

            // Перерисовываем форму
            this.Invalidate();
        }

        bool sleep = true;
        private void button1_Click(object sender, EventArgs e) {
            if (sleep) {
                timer1.Start();
                button1.Text = "Стоп";
                button1.ForeColor = Color.Red;
                sleep = false;
            }
            else {
                timer1.Stop();
                button1.Text = "Старт";
                button1.ForeColor = Color.Green;
                sleep = true;
            }
        }

        private void button2_Click(object sender, EventArgs e) {
            if (Application.OpenForms.Count == 1) {
                settings settingsForm = new settings();
                settingsForm.Owner = this;
                settingsForm.Show();
            }
            
        }

        private void Form1_KeyDown(object sender, KeyEventArgs e) {
            if (e.KeyCode == Keys.Escape)
                this.Close();
        }
    }
}
