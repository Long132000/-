import requests

url = "https://www.zamzar.com/files/0198e8d8-721d-71ae-a2c7-e798025a07fc/?from=mp4&to=srt"

headers = {
    # Вставьте сюда ВСЕ заголовки из команды fetch
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "_ga=GA1.1.1643975984.1756253124; PHPSESSID=be0p7fghka0s1a8rhch9a07bvr; cooktest=ok; cookieconsent_dismissed=yes; zamzar_jobs=eyJpdiI6InZsekgyNDBGWHdhRlIwencrS0Zjd1E9PSIsInZhbHVlIjoiS2tkY2FcL2ZUZkhhR3N5WE1tZFVTZ2dMTFFDTzRDZFF4R3h4ZUk2cXpwUmc9IiwibWFjIjoiY2U1MDM2YTgxZWFkNWNlYjRhOTlhMjRhNjFhMjI1ZDM4Yzg5MTg5MzhjMzU5MDVlNWI5OGM1OTJmNjU3MWVmNyJ9; _omappvp=uWTAPXYOHLBJ8i4EtTVV6CCWKZ89x9ceNBHFGjgKlpbvWBtx6XRQVSejm3LG4Hjgflx8zuHOvRvDeJ8VzUDPcFl9xSZ7tzbp; omSeen-gipkwhrov2mh6tlp4yhp=1756253865347; om-gipkwhrov2mh6tlp4yhp=1756253866444; _gcl_au=1.1.407630934.1756253124.1532460397.1756253818.1756253874; zamzar_ga={\"clientId\":\"1643975984.1756253124\",\"sessionId\":1756256756}; XSRF-TOKEN=eyJpdiI6InBiQ2p5cExqa2tTTERoQXhwa0hWR2c9PSIsInZhbHVlIjoiN3NzS2dxK1c3bmI1YzNKVldaY0pLeW8vOFlLWUNLTjgxTXcvQjdKRU9MSEdYSVBGR24zODhsUjQrQmZpMC94QXRpQTlnZjVqakt6cCtWZDgzN0traEl6Wi9IM0YzbXR1Tk1qTWRTbk1ITmdpNVB5ZXhvMHErOUsyVXdKckQ3UU8iLCJtYWMiOiI5ZmM5MmMzOTNlZGIzOGFkOGI0ZDEyYmQyNWU2ZmQ1YWEzYjhlNjMzNzU2ZGI1YTllZGNjNmNkOGQwNjk1MTFlIiwidGFnIjoiIn0%3D; zamzar_session=eyJpdiI6IkVTdEl0VWU5b3podWE0Q0NNb2J6bFE9PSIsInZhbHVlIjoidW5HZ05UM3ZPeE9JOWtiWmRENnkxWHk2MGgzbXBMUTIrZVRjaHB6SnE1V3Y2cG1HNmIwaUtkNnNwWXJ2K3ByTTQ3WWQ1SVJUOG4vU2s1aFlLWnpzb3JpTS9DVEJCYXQ5aUxOMnZjRGw3VHVHOVVlQ2NWMHBPdGRWTXZaK3hucWciLCJtYWMiOiJjZGMzY2ViMGExOTFiNDU2MzE3ZWVmZTRmMjExOWVjOWQzYWI4MGZjY2M4NDVkZTk5NmEyMDFhZDMxZjNhOTFlIiwidGFnIjoiIn0%3D; pnsgv6s0NLThUUdlzNksN1GERtfYTqrGo0Uw7fep=eyJpdiI6IjN5OTJXbmFxaWZubUNGdXNZbEJtakE9PSIsInZhbHVlIjoiR1cySTdFRWMwUGdnamRxOG96eXBjSXczOXc4bWV4cE5VTXpvWFJPeWJHSy9ocEIvbUZVSjBzMmV0N3RXaDFMb2hneHllNTdLYzMxd3ZPZnpXdHIzRDFMcUFTaEdzVjRTWXBoZDRCeHhoTlNVcnhPN0VBMDVhZE1OZE9lbWZyclVrMGhER0d5OXdLbjIyMUpURXN0emhoQThOZkhpTTlKNlRGMncwNi9IVTFNMnk2RnVUbnZ5bm13T3pFbUJZMlVQdmpWMzlGcFRDdG1RT3FWNCtXa2hQUTFJT2dIMjludGhwUEpwZDhPczMzV0U3SjR1NDVsVWdGMCt3cGl0VjZhV0p6SThEK3h2UUJnc2UvWkhOOWVEUlJTb3Ezd2t3N1h3bWVGbUVRcFo0bjZQRWxKSDIvdndxbzhGVmdEc0d0UWpJRTkraVFzU29qY3JyVWFZaDVUcXVhMlMvNTdtUWxmTDNqYmk4dGVYOHZyVzJXa0Q0NCtKYzJWaldTTThwZUJPTTFTVHY5d3lFaWdOR2V5ZzhOc2g4cUVRdFVNQy9yZnNFV291d3Y5V0s3SnhDNVZtd3psbGxScWhLcjlMdkFya2p1cllSeFpDbk9jNEgrb0JRbHFxV2ZNVkowdzd0L0k3b3B4dlM5ZTJVakE9IiwibWFjIjoiNTI0YzI0NjY5NGE3NzkyYjcyMGM1NWRhMWVhZTcyYTNiMGJlNzkxNTUzNzU0ZGFjZGVmMmJhMjhjODk0MDExZCIsInRhZyI6IiJ9; _ga_M4CENLE5VL=GS2.1.s1756256756$o2$g1$t1756256843$j41$l0$h0",
    "Referer": "https://www.zamzar.com/files/0198e8d8-721d-71ae-a2c7-e798025a07fc/?from=mp4&to=srt"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("H1_S1E4_IG.srt", "wb") as f:
        f.write(response.content)
    print("Файл скачан!")
else:
    print("Ошибка:", response.status_code)