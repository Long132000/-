using System;

class Monster
{
    private string name;
    private int power;
    private int heals;

    protected static Random rnd = new Random();

    public string Name => name;
    public int Power => power;
    public int Heals => heals;

    public Monster(string name)
    {
        this.name = name;
        this.power = rnd.Next(10, 50);
        this.heals = rnd.Next(100, 500);
    }

    public virtual void Show()
    {
        Console.ForegroundColor = ConsoleColor.DarkYellow; // Устанавливаем цвет для здоровья
        Console.WriteLine($"Персонаж: {name} Вид персонажа: {this.GetType().Name} Сила: {power} Здоровье: {heals}");
        Console.ResetColor(); // Сброс цвета обратно на стандартный
    }

    public static void Attack(Monster attacker, Monster defender)
    {
        if (attacker.power > defender.power)
        {
            int damage = attacker.power;
            if (defender is Demon demon) // если защитник - демон
            {
                damage *= demon.GetBrain(); // увеличить урон на коэффициент ума
                demon.IncreaseBrain(); // увеличить ум демона
            }
            defender.heals -= damage; // Уменьшаем здоровье защитника
            attacker.power += 10; // увеличиваем силу атакующего
            Console.WriteLine($"{attacker.Name} атакует {defender.Name} и наносит {damage} урона.");
        }
        else
        {
            // Если атакующий слабее или равен защитнику, просто выводим сообщение
            Console.WriteLine($"{attacker.Name} не смог атаковать {defender.Name}, так как его сила меньше или равна.");
        }

        if (defender.Die())
        {
            Console.WriteLine($"{defender.Name} погиб!");
        }
    }

    public bool Die()
    {
        return this.heals <= 0;
    }
}

class Demon : Monster
{
    private int brain; // Ум

    public int GetBrain() => brain; // Метод для получения значения ума

    public void IncreaseBrain() // Метод для увеличения значения ума
    {
        brain++;
    }

    public Demon(string name) : base(name)
    {
        this.brain = rnd.Next(1, 5);
    }

    public override void Show()
    {
        base.Show();
        Console.ForegroundColor = ConsoleColor.DarkYellow; // Устанавливаем цвет для здоровья
        Console.WriteLine($"Ум: {brain}");
        Console.ResetColor(); // Сброс цвета обратно на стандартный
    }
}

class Program
{
    static void Main(string[] args)
    {
        Console.Write("Введите имя вашего персонажа: ");
        string playerName = Console.ReadLine();

        Monster player = new Demon(playerName); // Игрок - демон
        Monster[] bots = new Monster[4];
        bots[0] = new Monster("Халк");
        bots[1] = new Monster("Титан");
        bots[2] = new Demon("Хитрый");
        bots[3] = new Demon("Ящер");

        bool playerIsAlive = true;

        while (playerIsAlive && bots.Length > 0)
        {
            int enemyIndex = new Random().Next(bots.Length);
            Monster enemy = bots[enemyIndex];

            Console.WriteLine($"\nСражение: {player.Name} (здоровье: {player.Heals}) против {enemy.Name} (здоровье: {enemy.Heals})");

            // Бой до тех пор, пока оба персонажа живы
            while (playerIsAlive && enemy.Heals > 0)
            {
                // Игрок атакует противника
                Monster.Attack(player, enemy);
                if (!enemy.Die())
                {
                    // Противник атакует игрока только если он еще жив
                    Monster.Attack(enemy, player);
                }

                // Проверка на жизнь игрока
                playerIsAlive = !player.Die();

                if (!playerIsAlive)
                {

                    Console.ForegroundColor = ConsoleColor.Red; // Устанавливаем цвет сообщения о поражении
                    Console.WriteLine($"{player.Name} погиб. Вы проиграли!");
                    Console.ResetColor(); // Сброс цвета обратно на стандартный
                }
            }

            // Проверяем, убит ли противник и удаляем его из массива
            if (enemy.Die())
            {
                Console.WriteLine($"{enemy.Name} уничтожен.");
                bots[enemyIndex] = bots[bots.Length - 1]; // переместить последнего бота на место убитого
                Array.Resize(ref bots, bots.Length - 1); // уменьшить размер массива на 1
            }
            else
            {
                Console.WriteLine($"{enemy.Name} выжил после сражения.");
            }
        }

        if (playerIsAlive)
        {
            Console.ForegroundColor = ConsoleColor.Green; // Устанавливаем цвет сообщения о победе
            Console.WriteLine("Поздравляем! Вы победили всех врагов!");
            Console.ResetColor(); // Сброс цвета обратно на стандартный
        }
    }
}
