using System;

namespace AddressBookApp
{
    public class Note
    {
        private string fullName; // ФИО человека
        private string phoneNumber; // Номер телефона

        public string FullName
        {
            get => fullName;
            set => fullName = value;
        }

        public string PhoneNumber
        {
            get => phoneNumber;
            set => phoneNumber = value;
        }

        public Note(string fullName, string phoneNumber)
        {
            this.fullName = fullName;
            this.phoneNumber = phoneNumber;
        }

        public virtual void Show()
        {
            Console.WriteLine($"ФИО: {fullName}, Телефон: {phoneNumber}");
        }
    }
}
