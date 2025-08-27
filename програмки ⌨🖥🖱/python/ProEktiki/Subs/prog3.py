import requests

url = "https://www.zamzar.com/files/0198e8d8-721d-71ae-a2c7-e798025a07fc/H1_S1E4_IG.srt"
filename = "H1_S1E4_IG.srt"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Referer": "https://www.zamzar.com/"
}

response = requests.get(url, headers=headers, stream=True)

if response.status_code == 200:
    with open(filename, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print(f"Файл успешно сохранён как {filename}")
else:
    print(f"Ошибка: {response.status_code}. Файл, возможно, удалён или ссылка недействительна.")
