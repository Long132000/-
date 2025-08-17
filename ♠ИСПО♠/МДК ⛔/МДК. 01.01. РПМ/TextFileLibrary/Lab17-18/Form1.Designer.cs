namespace Lab17_18
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.файлToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.открытьToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.сохранитьКакToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.найтиФайлыToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.сортировкаПоИмениToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.сортировкаПоКоличествуСимволовToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.сортировкаПоКоличествуСловToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.выходToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.параметрыToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.шрифтToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.показатьСкрытьПанельИнструментовToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.поискToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.подсчитатьСловаToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.поискСловСоСкрытымСловомToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.справкаToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.оПрограммеToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.обАвтореToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStrip1 = new System.Windows.Forms.ToolStrip();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.toolStripStatusLabel1 = new System.Windows.Forms.ToolStripStatusLabel();
            this.richTextBox1 = new System.Windows.Forms.RichTextBox();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.fontDialog1 = new System.Windows.Forms.FontDialog();
            this.listBox1 = new System.Windows.Forms.ListBox();
            this.menuStrip1.SuspendLayout();
            this.statusStrip1.SuspendLayout();
            this.SuspendLayout();

            // menuStrip1
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.файлToolStripMenuItem,
            this.параметрыToolStripMenuItem,
            this.поискToolStripMenuItem,
            this.справкаToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(800, 24);
            this.menuStrip1.TabIndex = 0;
            this.menuStrip1.Text = "menuStrip1";

            // файлToolStripMenuItem
            this.файлToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.открытьToolStripMenuItem,
            this.сохранитьКакToolStripMenuItem,
            this.найтиФайлыToolStripMenuItem,
            this.выходToolStripMenuItem});
            this.файлToolStripMenuItem.Name = "файлToolStripMenuItem";
            this.файлToolStripMenuItem.Size = new System.Drawing.Size(48, 20);
            this.файлToolStripMenuItem.Text = "Файл";

            // открытьToolStripMenuItem
            this.открытьToolStripMenuItem.Name = "открытьToolStripMenuItem";
            this.открытьToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.открытьToolStripMenuItem.Text = "Открыть";
            this.открытьToolStripMenuItem.Click += new System.EventHandler(this.открытьToolStripMenuItem_Click);

            // сохранитьКакToolStripMenuItem
            this.сохранитьКакToolStripMenuItem.Name = "сохранитьКакToolStripMenuItem";
            this.сохранитьКакToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.сохранитьКакToolStripMenuItem.Text = "Сохранить как";
            this.сохранитьКакToolStripMenuItem.Click += new System.EventHandler(this.сохранитьКакToolStripMenuItem_Click);

            // найтиФайлыToolStripMenuItem
            this.найтиФайлыToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.сортировкаПоИмениToolStripMenuItem,
            this.сортировкаПоКоличествуСимволовToolStripMenuItem,
            this.сортировкаПоКоличествуСловToolStripMenuItem});
            this.найтиФайлыToolStripMenuItem.Name = "найтиФайлыToolStripMenuItem";
            this.найтиФайлыToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.найтиФайлыToolStripMenuItem.Text = "Найти файлы";
            this.найтиФайлыToolStripMenuItem.Click += new System.EventHandler(this.найтиФайлыToolStripMenuItem_Click);

            // сортировкаПоИмениToolStripMenuItem
            this.сортировкаПоИмениToolStripMenuItem.Name = "сортировкаПоИмениToolStripMenuItem";
            this.сортировкаПоИмениToolStripMenuItem.Size = new System.Drawing.Size(240, 22);
            this.сортировкаПоИмениToolStripMenuItem.Text = "Сортировка по имени";
            this.сортировкаПоИмениToolStripMenuItem.Click += new System.EventHandler(this.сортировкаПоИмениToolStripMenuItem_Click);

            // сортировкаПоКоличествуСимволовToolStripMenuItem
            this.сортировкаПоКоличествуСимволовToolStripMenuItem.Name = "сортировкаПоКоличествуСимволовToolStripMenuItem";
            this.сортировкаПоКоличествуСимволовToolStripMenuItem.Size = new System.Drawing.Size(240, 22);
            this.сортировкаПоКоличествуСимволовToolStripMenuItem.Text = "Сортировка по количеству символов";
            this.сортировкаПоКоличествуСимволовToolStripMenuItem.Click += new System.EventHandler(this.сортировкаПоКоличествуСимволовToolStripMenuItem_Click);

            // сортировкаПоКоличествуСловToolStripMenuItem
            this.сортировкаПоКоличествуСловToolStripMenuItem.Name = "сортировкаПоКоличествуСловToolStripMenuItem";
            this.сортировкаПоКоличествуСловToolStripMenuItem.Size = new System.Drawing.Size(240, 22);
            this.сортировкаПоКоличествуСловToolStripMenuItem.Text = "Сортировка по количеству слов";
            this.сортировкаПоКоличествуСловToolStripMenuItem.Click += new System.EventHandler(this.сортировкаПоКоличествуСловToolStripMenuItem_Click);

            // выходToolStripMenuItem
            this.выходToolStripMenuItem.Name = "выходToolStripMenuItem";
            this.выходToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.выходToolStripMenuItem.Text = "Выход";
            this.выходToolStripMenuItem.Click += new System.EventHandler(this.выходToolStripMenuItem_Click);

            // параметрыToolStripMenuItem
            this.параметрыToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.шрифтToolStripMenuItem,
            this.показатьСкрытьПанельИнструментовToolStripMenuItem});
            this.параметрыToolStripMenuItem.Name = "параметрыToolStripMenuItem";
            this.параметрыToolStripMenuItem.Size = new System.Drawing.Size(83, 20);
            this.параметрыToolStripMenuItem.Text = "Параметры";

            // шрифтToolStripMenuItem
            this.шрифтToolStripMenuItem.Name = "шрифтToolStripMenuItem";
            this.шрифтToolStripMenuItem.Size = new System.Drawing.Size(273, 22);
            this.шрифтToolStripMenuItem.Text = "Шрифт";
            this.шрифтToolStripMenuItem.Click += new System.EventHandler(this.шрифтToolStripMenuItem_Click);

            // показатьСкрытьПанельИнструментовToolStripMenuItem
            this.показатьСкрытьПанельИнструментовToolStripMenuItem.Name = "показатьСкрытьПанельИнструментовToolStripMenuItem";
            this.показатьСкрытьПанельИнструментовToolStripMenuItem.Size = new System.Drawing.Size(273, 22);
            this.показатьСкрытьПанельИнструментовToolStripMenuItem.Text = "Показать/Скрыть панель инструментов";
            this.показатьСкрытьПанельИнструментовToolStripMenuItem.Click += new System.EventHandler(this.показатьСкрытьПанельИнструментовToolStripMenuItem_Click);

            // поискToolStripMenuItem
            this.поискToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.подсчитатьСловаToolStripMenuItem,
            this.поискСловСоСкрытымСловомToolStripMenuItem});
            this.поискToolStripMenuItem.Name = "поискToolStripMenuItem";
            this.поискToolStripMenuItem.Size = new System.Drawing.Size(54, 20);
            this.поискToolStripMenuItem.Text = "Поиск";

            // подсчитатьСловаToolStripMenuItem
            this.подсчитатьСловаToolStripMenuItem.Name = "подсчитатьСловаToolStripMenuItem";
            this.подсчитатьСловаToolStripMenuItem.Size = new System.Drawing.Size(234, 22);
            this.подсчитатьСловаToolStripMenuItem.Text = "Подсчитать слова";
            this.подсчитатьСловаToolStripMenuItem.Click += new System.EventHandler(this.подсчитатьСловаToolStripMenuItem_Click);

            // поискСловСоСкрытымСловомToolStripMenuItem
            this.поискСловСоСкрытымСловомToolStripMenuItem.Name = "поискСловСоСкрытымСловомToolStripMenuItem";
            this.поискСловСоСкрытымСловомToolStripMenuItem.Size = new System.Drawing.Size(234, 22);
            this.поискСловСоСкрытымСловомToolStripMenuItem.Text = "Поиск слов со скрытым словом";
            this.поискСловСоСкрытымСловомToolStripMenuItem.Click += new System.EventHandler(this.поискСловСоСкрытымСловомToolStripMenuItem_Click);

            // справкаToolStripMenuItem
            this.справкаToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.оПрограммеToolStripMenuItem,
            this.обАвтореToolStripMenuItem});
            this.справкаToolStripMenuItem.Name = "справкаToolStripMenuItem";
            this.справкаToolStripMenuItem.Size = new System.Drawing.Size(65, 20);
            this.справкаToolStripMenuItem.Text = "Справка";

            // оПрограммеToolStripMenuItem
            this.оПрограммеToolStripMenuItem.Name = "оПрограммеToolStripMenuItem";
            this.оПрограммеToolStripMenuItem.Size = new System.Drawing.Size(149, 22);
            this.оПрограммеToolStripMenuItem.Text = "О программе";
            this.оПрограммеToolStripMenuItem.Click += new System.EventHandler(this.оПрограммеToolStripMenuItem_Click);

            // обАвтореToolStripMenuItem
            this.обАвтореToolStripMenuItem.Name = "обАвтореToolStripMenuItem";
            this.обАвтореToolStripMenuItem.Size = new System.Drawing.Size(149, 22);
            this.обАвтореToolStripMenuItem.Text = "Об авторе";
            this.обАвтореToolStripMenuItem.Click += new System.EventHandler(this.обАвтореToolStripMenuItem_Click);

            // toolStrip1
            this.toolStrip1.Location = new System.Drawing.Point(0, 24);
            this.toolStrip1.Name = "toolStrip1";
            this.toolStrip1.Size = new System.Drawing.Size(800, 25);
            this.toolStrip1.TabIndex = 1;
            this.toolStrip1.Text = "toolStrip1";

            // statusStrip1
            this.statusStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripStatusLabel1});
            this.statusStrip1.Location = new System.Drawing.Point(0, 428);
            this.statusStrip1.Name = "statusStrip1";
            this.statusStrip1.Size = new System.Drawing.Size(800, 22);
            this.statusStrip1.TabIndex = 2;
            this.statusStrip1.Text = "statusStrip1";

            // toolStripStatusLabel1
            this.toolStripStatusLabel1.Name = "toolStripStatusLabel1";
            this.toolStripStatusLabel1.Size = new System.Drawing.Size(47, 17);
            this.toolStripStatusLabel1.Text = "Готово";

            // richTextBox1
            this.richTextBox1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.richTextBox1.Location = new System.Drawing.Point(0, 49);
            this.richTextBox1.Name = "richTextBox1";
            this.richTextBox1.Size = new System.Drawing.Size(600, 379);
            this.richTextBox1.TabIndex = 3;
            this.richTextBox1.Text = "";

            // openFileDialog1
            this.openFileDialog1.FileName = "openFileDialog1";
            this.openFileDialog1.Filter = "Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*";

            // saveFileDialog1
            this.saveFileDialog1.Filter = "Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*";

            // listBox1
            this.listBox1.Dock = System.Windows.Forms.DockStyle.Right;
            this.listBox1.FormattingEnabled = true;
            this.listBox1.Location = new System.Drawing.Point(600, 49);
            this.listBox1.Name = "listBox1";
            this.listBox1.Size = new System.Drawing.Size(200, 379);
            this.listBox1.TabIndex = 4;

            // Form1
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.richTextBox1);
            this.Controls.Add(this.listBox1);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.toolStrip1);
            this.Controls.Add(this.menuStrip1);
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "Form1";
            this.Text = "Текстовый редактор (Вариант 6)";
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.statusStrip1.ResumeLayout(false);
            this.statusStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        #endregion

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem файлToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem открытьToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem сохранитьКакToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem найтиФайлыToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem сортировкаПоИмениToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem сортировкаПоКоличествуСимволовToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem сортировкаПоКоличествуСловToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem выходToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem параметрыToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem шрифтToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem показатьСкрытьПанельИнструментовToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem поискToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem подсчитатьСловаToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem поискСловСоСкрытымСловомToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem справкаToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem оПрограммеToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem обАвтореToolStripMenuItem;
        private System.Windows.Forms.ToolStrip toolStrip1;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel1;
        private System.Windows.Forms.RichTextBox richTextBox1;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
        private System.Windows.Forms.FontDialog fontDialog1;
        private System.Windows.Forms.ListBox listBox1;
    }
}