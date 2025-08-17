using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
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
            toolStripStatusLabel1.Text = "Готово";
        }

        private void открытьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    currentFile = new TextFile(openFileDialog1.FileName);
                    richTextBox1.Text = currentFile.Text;
                    toolStripStatusLabel1.Text = "Файл открыт: " + currentFile.FileName;
                }
                catch
                {
                    MessageBox.Show("Ошибка при открытии файла!", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
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
                    toolStripStatusLabel1.Text = "Файл сохранён: " + saveFileDialog1.FileName;
                }
                catch
                {
                    MessageBox.Show("Ошибка при сохранении файла!", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void найтиФайлыToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form2 form2 = new Form2();
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

        private void сортировкаПоИмениToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (foundFiles != null)
            {
                foundFiles.Sort();
                UpdateListBox();
            }
        }

        private void сортировкаПоКоличествуСимволовToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (foundFiles != null)
            {
                foundFiles.Sort(new FileLengthComparer());
                UpdateListBox();
            }
        }

        private void сортировкаПоКоличествуСловToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (foundFiles != null)
            {
                foundFiles.Sort(new WordCountComparer());
                UpdateListBox();
            }
        }

        private void UpdateListBox()
        {
            listBox1.Items.Clear();
            foreach (var file in foundFiles)
            {
                listBox1.Items.Add(file.FileName);
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
            if (currentFile != null)
            {
                int wordCount = currentFile.CountWords();
                MessageBox.Show($"Количество слов: {wordCount}", "Результат", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void поискСловСПодстрокойToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (currentFile != null)
            {
                string substring = Microsoft.VisualBasic.Interaction.InputBox("Введите подстроку:", "Поиск слов");
                if (!string.IsNullOrEmpty(substring))
                {
                    List<string> words = currentFile.FindWordsWithSubstring(substring);
                    MessageBox.Show($"Найдено слов: {words.Count}\n\n{string.Join(", ", words)}", "Результат", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
        }

        private void оПрограммеToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Текстовый редактор\nВерсия 1.0", "О программе", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void обАвтореToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Автор: [Ваше имя]\nГруппа: [Ваша группа]", "Об авторе", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
    }
}