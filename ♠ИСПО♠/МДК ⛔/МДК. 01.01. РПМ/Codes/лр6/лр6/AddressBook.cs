using System;
using System.Collections.Generic;

namespace AddressBookApp
{
    public class AddressBook
    {
        private List<Note> notes;

        public AddressBook()
        {
            notes = new List<Note>();
        }

        public void AddNote(Note note)
        {
            notes.Add(note);
        }

        public void RemoveNote(Note note)
        {
            notes.Remove(note);
        }

        public void ShowAllNotes()
        {
            Console.WriteLine("Список записей:");
            foreach (var note in notes)
            {
                note.Show();
            }
        }
    }
}
