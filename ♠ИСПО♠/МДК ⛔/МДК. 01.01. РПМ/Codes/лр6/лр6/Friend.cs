using System;

namespace AddressBookApp
{
    public class Friend : Note
    {
        private string email; // Электронная почта
        private DateTime birthDate; // Дата рождения

        public string Email
        {
            get => email;
            set => email = value;
        }

        public DateTime BirthDate
        {
            get => birthDate;
            set => birthDate = value;
        }

        public Friend(string fullName, string phoneNumber, string email, DateTime birthDate)
            : base(fullName, phoneNumber)
        {
            this.email = email;
            this.birthDate = birthDate;
        }

        public override void Show()
        {
            base.Show();
            Console.WriteLine($"Электронная почта: {email}, Дата рождения: {birthDate.ToShortDateString()}");
        }
    }
}
