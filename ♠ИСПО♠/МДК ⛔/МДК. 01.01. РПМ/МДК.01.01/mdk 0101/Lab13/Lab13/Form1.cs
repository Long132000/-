using System;
using System.Drawing;
using System.Windows.Forms;

namespace Lab13
{
    public partial class Form1 : Form
    {
        // Параметры фигуры
        private int baseWidth = 50, baseHeight = 50;
        private int currentWidth, currentHeight;
        private int x = 100, y = 100;
        private int step = 5;
        private int sizeStep = 2;
        private int maxStretch = 150;

        // Направление и состояние
        private enum Direction { Down, Up, Right, Left };
        private Direction currentDirection = Direction.Down;
        private bool isStretching = true;

        // Цвета и форма
        private Color forwardColor = Color.Green;
        private Color backwardColor = Color.Cyan;
        private int shapeType = 0; // 0-круг, 1-квадрат, 2-ромб
        private int moveMode = 0; // 0-вертикаль, 1-горизонталь

        // Кисть для рисования
        private SolidBrush brush = new SolidBrush(Color.Green);

        public Form1()
        {
            InitializeComponent();
            currentWidth = baseWidth;
            currentHeight = baseHeight;
            this.DoubleBuffered = true;
            this.KeyPreview = true;
        }

        // Свойства для настройки
        public int Speed
        {
            get => 100 - timer1.Interval;
            set => timer1.Interval = Math.Max(1, 100 - value);
        }

        public Color ForwardColor
        {
            get => forwardColor;
            set => forwardColor = value;
        }

        public Color BackwardColor
        {
            get => backwardColor;
            set => backwardColor = value;
        }

        public int ShapeType
        {
            get => shapeType;
            set => shapeType = value;
        }

        public int MoveMode
        {
            get => moveMode;
            set => moveMode = value;
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            // Вертикальный режим (вверх-вниз)
            if (moveMode == 0)
            {
                if (currentDirection == Direction.Down)
                {
                    brush.Color = forwardColor;
                    y += step;

                    if (isStretching)
                    {
                        currentHeight += sizeStep;
                        if (currentHeight >= maxStretch) isStretching = false;
                    }
                    else
                    {
                        currentHeight -= sizeStep;
                        if (currentHeight <= baseHeight) isStretching = true;
                    }

                    if (y + currentHeight >= ClientSize.Height)
                        currentDirection = Direction.Up;
                }
                else
                {
                    brush.Color = backwardColor;
                    y -= step;

                    if (isStretching)
                    {
                        currentHeight += sizeStep;
                        if (currentHeight >= maxStretch) isStretching = false;
                    }
                    else
                    {
                        currentHeight -= sizeStep;
                        if (currentHeight <= baseHeight) isStretching = true;
                    }

                    if (y <= 0)
                        currentDirection = Direction.Down;
                }
            }
            // Горизонтальный режим (влево-вправо)
            else
            {
                if (currentDirection == Direction.Right)
                {
                    brush.Color = forwardColor;
                    x += step;

                    if (isStretching)
                    {
                        currentWidth += sizeStep;
                        if (currentWidth >= maxStretch) isStretching = false;
                    }
                    else
                    {
                        currentWidth -= sizeStep;
                        if (currentWidth <= baseWidth) isStretching = true;
                    }

                    if (x + currentWidth >= ClientSize.Width)
                        currentDirection = Direction.Left;
                }
                else
                {
                    brush.Color = backwardColor;
                    x -= step;

                    if (isStretching)
                    {
                        currentWidth += sizeStep;
                        if (currentWidth >= maxStretch) isStretching = false;
                    }
                    else
                    {
                        currentWidth -= sizeStep;
                        if (currentWidth <= baseWidth) isStretching = true;
                    }

                    if (x <= 0)
                        currentDirection = Direction.Right;
                }
            }

            Invalidate();
        }

        private void Form1_Paint(object sender, PaintEventArgs e)
        {
            // Ограничение координат
            x = Math.Max(0, Math.Min(x, ClientSize.Width - currentWidth));
            y = Math.Max(0, Math.Min(y, ClientSize.Height - currentHeight));

            // Рисование фигуры
            switch (shapeType)
            {
                case 0: // Круг/Эллипс
                    e.Graphics.FillEllipse(brush, x, y, currentWidth, currentHeight);
                    break;
                case 1: // Квадрат/Прямоугольник
                    e.Graphics.FillRectangle(brush, x, y, currentWidth, currentHeight);
                    break;
                case 2: // Ромб
                    Point[] diamond = {
                        new Point(x + currentWidth/2, y),
                        new Point(x + currentWidth, y + currentHeight/2),
                        new Point(x + currentWidth/2, y + currentHeight),
                        new Point(x, y + currentHeight/2)
                    };
                    e.Graphics.FillPolygon(brush, diamond);
                    break;
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (timer1.Enabled)
            {
                timer1.Stop();
                button1.Text = "Старт";
            }
            else
            {
                timer1.Start();
                button1.Text = "Стоп";
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Form2 settings = new Form2(this);
            settings.Show();
        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Escape)
                Close();
        }
    }
}