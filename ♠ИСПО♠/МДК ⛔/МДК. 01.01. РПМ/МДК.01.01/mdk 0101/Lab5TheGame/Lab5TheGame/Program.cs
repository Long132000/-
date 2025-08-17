using System;

namespace Lab5TheGame // Note: actual namespace depends on the project name.
{

    class Monster
    {
        private string name;
        private int str;
        private int hp;
        protected enum m_type
        {
            monster,
            demon,
            character
        };

        protected m_type type;

        protected static Random rnd = new Random();

        public Monster(string name)
        {
            this.name = name;
            this.type = m_type.monster;
            this.str = rnd.Next(50, 75);
            this.hp = rnd.Next(100, 150);
        }

        static int buff = rnd.Next(5, 15);

        public virtual void show()
        {
            Console.WriteLine($"name {name}; type {type}; Strenght {str}; Health {hp}");
        }

        public int Str
        {
            get
            {
                return str;
            }
            set
            {
                str = value;
            }
        }

        public int Hp
        {
            get
            {
                return hp;
            }
            set
            {
                hp = value;
            }
        }

        public int Buff
        {
            get
            {
                return buff;
            }
            set 
            { 
                buff = value; 
            }
        }

        public static void attack(Monster A, Monster B)
        {
            if (A.str > B.str)
            {
                B.hp -= A.str;
                A.str += buff;
            }

            else A.hp -= B.str;
        }

        public bool died()
        {
            if (this.hp <= 0) return true; else return false;
        }
    }

    class Demon : Monster
    {
        private int wis;

        public Demon(string name) : base(name) 
        {
            this.wis = rnd.Next(1, 5);
            this.Str = Str * wis;
            this.type = m_type.demon;
        }

        public override void show()
        {
            base.show();
            Console.WriteLine($"Wisdom {wis}");
        }

    }

    class Character : Monster
    {
        private int max_hp;

        protected static Random rnd = new Random();

        public Character(string name) : base(name)
        {
            this.type = m_type.character;
        }

        public virtual void show()
        {
            base.show();
        }
    }

    internal class Program
    {
        static void Main(string[] args)
        {
            Monster[] bots = new Monster[4];
            bots[0] = new Monster("Orc");
            bots[1] = new Monster("Goblin");
            bots[2] = new Demon("Colloseum Dog");
            bots[3] = new Demon("Kapra Demon");

            Console.Write("Write your character`s name: ");
            string playerName = Console.ReadLine();
            Character player = new Character(playerName);

            player.show();

            Console.WriteLine("\nMonsters:");
            foreach (var bot in bots)
            {
                bot.show();
            }

            while (true)
            {
                Console.Write("\n Who will be your opponent? ");
                int fighterId = int.Parse(Console.ReadLine());

                if (bots[fighterId-1].died()) {
                    Console.WriteLine("\nHe is dead");
                    continue;
                }

                Monster.attack(player, bots[fighterId - 1]);

                Console.WriteLine("\nAfter the fight:");
                Console.ForegroundColor = ConsoleColor.DarkYellow;
                player.show();
                Console.ForegroundColor = ConsoleColor.White;
                foreach (var bot in bots)
                {
                    bot.show();
                }

                if (player.died())
                {
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine("\nYou died!");
                    Console.ForegroundColor = ConsoleColor.White;
                    break;
                }
            };
        }
    }
}
