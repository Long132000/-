using System;
using System.Collections.Generic;
using System.Text;
using System.Windows.Forms;
using TextFileLibrary;

namespace Lab17_18
{
    public partial class Form1 : Form
    {
        private TextFile currentFile;
        private List<TextFile> foundFiles;

        public Form1()
        {
            InitializeComponent();
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            currentFile = new TextFile("", "");
            toolStripStatusLabel1.Text = "Готово";
            SetupToolbarButtons();
        }

        private void SetupToolbarButtons()
        {
            toolStrip1.Items.Clear();

            // Кнопка Открыть
            var btnOpen = new ToolStripButton("Открыть");
            btnOpen.Click += открытьToolStripMenuItem_Click;
            toolStrip1.Items.Add(btnOpen);

            // Кнопка Сохранить
            var btnSave = new ToolStripButton("Сохранить");
            btnSave.Click += сохранитьКакToolStripMenuItem_Click;
            toolStrip1.Items.Add(btnSave);

            // Кнопка Поиск файлов
            var btnSearch = new ToolStripButton("Поиск файлов");
            btnSearch.Click += найтиФайлыToolStripMenuItem_Click;
            toolStrip1.Items.Add(btnSearch);

            // Кнопка Подсчет слов
            var btnCount = new ToolStripButton("Подсчет слов");
            btnCount.Click += подсчитатьСловаToolStripMenuItem_Click;
            toolStrip1.Items.Add(btnCount);
        }

        private void выходToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void открытьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    currentFile = new TextFile(openFileDialog1.FileName);
                    richTextBox1.Text = currentFile.Text;
                    toolStripStatusLabel1.Text = $"Файл открыт: {currentFile.FileName}";
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка при открытии файла: {ex.Message}",
                        "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void сохранитьКакToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (saveFileDialog1.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    currentFile.Text = richTextBox1.Text;
                    currentFile.SaveFile(saveFileDialog1.FileName);
                    toolStripStatusLabel1.Text = $"Файл сохранён: {saveFileDialog1.FileName}";
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка при сохранении: {ex.Message}",
                        "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void найтиФайлыToolStripMenuItem_Click(object sender, EventArgs e)
        {
            using (var form2 = new Form2())
            {
                if (form2.ShowDialog() == DialogResult.OK)
                {
                    foundFiles = TextFile.FindFiles(form2.SelectedDirectory, "*.txt");
                    listBox1.Items.Clear();
                    foreach (var file in foundFiles)
                    {
                        listBox1.Items.Add(file.FileName);
                    }
                    toolStripStatusLabel1.Text = $"Найдено файлов: {foundFiles.Count}";
                }
            }
        }

        private void сортировкаПоИмениToolStripMenuItem_Click(object sender, EventArgs e)
        {
            foundFiles?.Sort();
            UpdateListBox();
        }

        private void сортировкаПоКоличествуСимволовToolStripMenuItem_Click(object sender, EventArgs e)
        {
            foundFiles?.Sort(new FileLengthComparer());
            UpdateListBox();
        }

        private void сортировкаПоКоличествуСловToolStripMenuItem_Click(object sender, EventArgs e)
        {
            foundFiles?.Sort(new WordCountComparer());
            UpdateListBox();
        }

        private void UpdateListBox()
        {
            listBox1.Items.Clear();
            if (foundFiles != null)
            {
                foreach (var file in foundFiles)
                {
                    listBox1.Items.Add(file.FileName);
                }
            }
        }

        private void шрифтToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (fontDialog1.ShowDialog() == DialogResult.OK)
            {
                richTextBox1.Font = fontDialog1.Font;
            }
        }

        private void показатьСкрытьПанельИнструментовToolStripMenuItem_Click(object sender, EventArgs e)
        {
            toolStrip1.Visible = !toolStrip1.Visible;
        }

        private void подсчитатьСловаToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show($"Количество слов: {currentFile.CountWords()}",
                "Результат", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void поискСловСоСкрытымСловомToolStripMenuItem_Click(object sender, EventArgs e)
        {
            string pattern = Microsoft.VisualBasic.Interaction.InputBox("Введите слово-шаблон:", "Поиск слов");
            if (!string.IsNullOrEmpty(pattern))
            {
                var words = currentFile.FindWordsContainingPattern(pattern);
                MessageBox.Show($"Найдено слов: {words.Count}\n\n{string.Join(", ", words)}",
                    "Результат", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void оПрограммеToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Текстовый редактор\nВерсия 1.0",
                "О программе", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void обАвтореToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Автор: [Ваше имя]\nГруппа: [Ваша группа]",
                "Об авторе", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
    }
}