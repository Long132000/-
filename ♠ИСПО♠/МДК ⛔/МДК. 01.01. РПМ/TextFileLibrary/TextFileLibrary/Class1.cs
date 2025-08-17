using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace TextFileLibrary
{
    /// <summary>
    /// Класс для работы с текстовыми файлами
    /// </summary>
    public class TextFile : IComparable<TextFile>
    {
        public string FileName { get; set; }
        public string Text { get; set; }
        public string Path { get; set; }

        /// <summary>
        /// Конструктор класса TextFile
        /// </summary>
        /// <param name="path">Путь к файлу</param>
        public TextFile(string path)
        {
            Path = path;
            FileName = System.IO.Path.GetFileName(path);
            OpenFile();
        }

        /// <summary>
        /// Конструктор класса TextFile (для тестов)
        /// </summary>
        /// <param name="name">Имя файла</param>
        /// <param name="text">Текст файла</param>
        public TextFile(string name, string text)
        {
            FileName = name;
            Text = text;
        }

        /// <summary>
        /// Открытие файла
        /// </summary>
        public void OpenFile()
        {
            using (StreamReader sr = new StreamReader(Path, System.Text.Encoding.GetEncoding(1251)))
            {
                Text = sr.ReadToEnd();
            }
        }

        /// <summary>
        /// Сохранение файла
        /// </summary>
        /// <param name="path">Путь для сохранения</param>
        public void SaveFile(string path)
        {
            using (StreamWriter sw = new StreamWriter(path, false, System.Text.Encoding.GetEncoding(1251)))
            {
                sw.Write(Text);
            }
        }

        /// <summary>
        /// Подсчёт количества слов в тексте
        /// </summary>
        /// <returns>Количество слов</returns>
        public int CountWords()
        {
            if (string.IsNullOrEmpty(Text)) return 0;
            char[] delimiters = new char[] { ' ', '\r', '\n', '\t', '.', ',', ';', '!', '?', ':', '(', ')' };
            return Text.Split(delimiters, StringSplitOptions.RemoveEmptyEntries).Length;
        }

        /// <summary>
        /// Перегрузка операции равенства (==)
        /// </summary>
        public static bool operator ==(TextFile f1, TextFile f2)
        {
            return f1.Text.Length == f2.Text.Length;
        }

        /// <summary>
        /// Перегрузка операции неравенства (!=)
        /// </summary>
        public static bool operator !=(TextFile f1, TextFile f2)
        {
            return !(f1 == f2);
        }

        /// <summary>
        /// Поиск файлов в указанном каталоге
        /// </summary>
        /// <param name="directory">Директория для поиска</param>
        /// <param name="extension">Расширение файла (например, "*.txt")</param>
        /// <returns>Список найденных файлов</returns>
        public static List<TextFile> FindFiles(string directory, string extension)
        {
            List<TextFile> files = new List<TextFile>();
            foreach (string filePath in Directory.GetFiles(directory, extension))
            {
                files.Add(new TextFile(filePath));
            }
            return files;
        }

        /// <summary>
        /// Реализация интерфейса IComparable для сортировки
        /// </summary>
        public int CompareTo(TextFile other)
        {
            return FileName.CompareTo(other.FileName);
        }

        /// <summary>
        /// Поиск слов, содержащих все буквы заданного слова в том же порядке
        /// </summary>
        /// <param name="pattern">Заданное слово-шаблон</param>
        /// <returns>Список найденных слов</returns>
        public List<string> FindWordsContainingPattern(string pattern)
        {
            List<string> result = new List<string>();
            char[] delimiters = new char[] { ' ', '\r', '\n', '\t', '.', ',', ';', '!', '?', ':', '(', ')' };
            string[] words = Text.Split(delimiters, StringSplitOptions.RemoveEmptyEntries);

            foreach (string word in words)
            {
                if (ContainsPattern(word, pattern))
                {
                    result.Add(word);
                }
            }
            return result;
        }

        /// <summary>
        /// Проверяет, содержит ли слово все буквы шаблона в том же порядке
        /// </summary>
        private bool ContainsPattern(string word, string pattern)
        {
            if (string.IsNullOrEmpty(pattern)) return false;

            int patternIndex = 0;
            string wordLower = word.ToLower();
            string patternLower = pattern.ToLower();

            for (int i = 0; i < wordLower.Length && patternIndex < patternLower.Length; i++)
            {
                if (wordLower[i] == patternLower[patternIndex])
                {
                    patternIndex++;
                }
            }

            return patternIndex == patternLower.Length;
        }
    }

    /// <summary>
    /// Класс для сортировки файлов по количеству символов
    /// </summary>
    public class FileLengthComparer : IComparer<TextFile>
    {
        public int Compare(TextFile x, TextFile y)
        {
            return x.Text.Length.CompareTo(y.Text.Length);
        }
    }

    /// <summary>
    /// Класс для сортировки файлов по количеству слов
    /// </summary>
    public class WordCountComparer : IComparer<TextFile>
    {
        public int Compare(TextFile x, TextFile y)
        {
            return x.CountWords().CompareTo(y.CountWords());
        }
    }
}