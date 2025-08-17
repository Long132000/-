using System;

class Program
{
    static void Main()
    {
        int totalAttempts = 0;
        int correctAnswers = 0;

        Console.WriteLine("Введите количество символов в слове: ");
        int wordLength = int.Parse(Console.ReadLine());

        Console.WriteLine("Введите букву, с которой должно начинаться слово: ");
        char startingLetter = Console.ReadLine()[0];

        while (true)
        {
            Console.Write($"Введите слово из {wordLength} символов, начинающееся на '{startingLetter}': ");
            string inputWord = Console.ReadLine();

            // Проверка на окончание работы
            if (string.IsNullOrEmpty(inputWord))
            {
                break;
            }

            totalAttempts++;

            // Проверка правильности ввода
            if (inputWord.Length == wordLength && inputWord[0] == startingLetter)
            {
                Console.WriteLine("Правильный ответ!");
                correctAnswers++;
            }
            else
            {
                Console.WriteLine("Неправильный ответ. Попробуйте снова.");
            }
        }

        // Вывод результатов
        Console.Clear();
        Console.WriteLine($"Всего попыток: {totalAttempts}");
        Console.WriteLine($"Правильных ответов: {correctAnswers}");

        // Расчёт баллов по стобалльной системе
        int score = totalAttempts > 0 ? (correctAnswers * 100) / totalAttempts : 0;
        Console.WriteLine($"Ваши баллы: {score}/100");

        Console.ReadKey();
    }
}
