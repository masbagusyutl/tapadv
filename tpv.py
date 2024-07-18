import time
import requests
import json
from datetime import datetime, timedelta

# Fungsi untuk membaca data dari file data.txt
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read().splitlines()
    return data

# Fungsi untuk mengambil nama pengguna dari init_data
def extract_username(init_data):
    import urllib.parse
    start = init_data.find("username%22%3A%22") + len("username%22%3A%22")
    end = init_data.find("%22", start)
    username = init_data[start:end]
    return urllib.parse.unquote(username)

# Fungsi untuk melakukan login
def login(init_data, user_agent):
    url = "https://tapadventure.pixelheroes.io/api/init"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Initdata": init_data,
        "Origin": "https://d2y873tmoumjr5.cloudfront.net",
        "Pragma": "no-cache",
        "Referer": "https://d2y873tmoumjr5.cloudfront.net/",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": user_agent
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Login successful")
        return True
    else:
        print(f"Login failed with status code: {response.status_code}")
        return False

# Fungsi untuk menjalankan hitung mundur
def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        hours, rem = divmod(remaining, 3600)
        minutes, seconds = divmod(rem, 60)
        timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        print(timeformat, end='\r')
        time.sleep(1)
    print("Countdown finished.")

# Fungsi utama untuk mengelola semua proses
def main():
    data = read_data('data.txt')
    num_accounts = len(data) // 2
    print(f"Total accounts: {num_accounts}")

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"

    for i in range(num_accounts):
        auth_header = data[i * 2]
        init_data = data[i * 2 + 1]
        username = extract_username(init_data)
        print(f"Processing account {i + 1} of {num_accounts}: {username}")

        # Melakukan login
        login_successful = login(init_data, user_agent)
        if login_successful:
            print(f"Login successful for account: {username}")

        # Tunggu selama 10 detik sebelum berpindah ke akun berikutnya
        countdown_timer(10)

    # Hitung mundur selama 6 jam 5 menit sebelum restart
    print("Starting 6-hour 5-minute countdown before restart...")
    countdown_timer(6 * 3600 + 5 * 60)

    # Tanyakan apakah pengguna ingin menjalankan kode lagi atau tidak
    run_again = input("Do you want to run the code again? (y/n): ")
    if run_again.lower() == 'y':
        main()
    else:
        print("Process completed.")

# Menjalankan kode utama
if __name__ == "__main__":
    main()
