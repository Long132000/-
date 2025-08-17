using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Security.Cryptography; //Библиотека криптографии

namespace WindowsFormsApp2
{
    public partial class Form1 : Form
    {
        Aes aes; //Экземпляр Aes для работы с шифрованием
        byte[] key;
        public Form1()
        {
            InitializeComponent();
            key = GenerateCode();
            aes = new AesCryptoServiceProvider();

        }

        private byte[] GenerateCode()
        {
            using (var aes = new AesCryptoServiceProvider())
            {
                aes.GenerateKey();
                return aes.Key;
            }
        }

        private string EncryptString(string plainText, byte[] key)//шифровка
        {
            using (var encryptor = aes.CreateEncryptor(key, aes.IV))
            {
                byte[] encryptedData;

                using (var msEncrypt = new System.IO.MemoryStream())
                {
                    using (var csEncrypt = new CryptoStream(msEncrypt, encryptor, CryptoStreamMode.Write))
                    using (var swEncrypt = new System.IO.StreamWriter(csEncrypt))
                    {
                        swEncrypt.Write(plainText);
                    }

                    encryptedData = msEncrypt.ToArray();
                }

                byte[] result = new byte[aes.IV.Length + encryptedData.Length];
                Array.Copy(aes.IV, 0, result, 0, aes.IV.Length);
                Array.Copy(encryptedData, 0, result, aes.IV.Length, encryptedData.Length);

                return Convert.ToBase64String(result);
            }
        }

        private string DecryptString(string cipherText, byte[] key)//дешифровка
        {
            cipherText = cipherText.Replace(" ", "");
            byte[] encryptedData = Convert.FromBase64String(cipherText);

            byte[] iv = new byte[aes.IV.Length];
            Array.Copy(encryptedData, 0, iv, 0, aes.IV.Length);

            byte[] data = new byte[encryptedData.Length - aes.IV.Length];
            Array.Copy(encryptedData, aes.IV.Length, data, 0, data.Length);

            using (var decryptor = aes.CreateDecryptor(key, iv))
            using (var ms = new System.IO.MemoryStream(data))
            using (var cs = new CryptoStream(ms, decryptor, CryptoStreamMode.Read))
            using (var sr = new System.IO.StreamReader(cs))
            {
                return sr.ReadToEnd();
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void Button1_Click(object sender, EventArgs e)
        {
            label1.Text = EncryptString(maskedTextBox1.Text, key);
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            label1.Text = DecryptString(label1.Text, key);
        }

        private void textBox1(object sender, EventArgs e)
        {

        }
    }
}