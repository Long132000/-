using System;

namespace AddressBookApp
{
    class Program
    {
        static void Main(string[] args)
        {
            AddressBook addressBook = new AddressBook();

            Note note1 = new Note("Иванов И.И.", "+7 123 456 78 90");
            Friend friend1 = new Friend("Петров П.П.", "+7 098 765 43 21", "petrov@mail.com", new DateTime(1990, 5, 20));

            addressBook.AddNote(note1);
            addressBook.AddNote(friend1);

            addressBook.ShowAllNotes();

            addressBook.RemoveNote(note1);
            Console.WriteLine("\nПосле удаления записи:");
            addressBook.ShowAllNotes();
        }
    }
}
