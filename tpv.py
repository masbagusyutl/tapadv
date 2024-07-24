import requests
import time
import json
from datetime import datetime, timedelta
import urllib.parse

# Fungsi untuk membaca data akun dari data.txt
def read_accounts(file_path):
    with open(file_path, 'r') as file:
        accounts = file.readlines()
    return [account.strip() for account in accounts]

# Fungsi untuk menulis data authorization ke authorization.txt
def write_authorization(data):
    with open('authorization.txt', 'w') as file:
        json.dump(data, file)

# Fungsi untuk membaca data authorization dari authorization.txt
def read_authorization():
    with open('authorization.txt', 'r') as file:
        return json.load(file)

# Fungsi untuk login dan mendapatkan data authorization
def login_and_get_authorization(account):
    url = "https://tapadventure.pixelheroes.io/api/init"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Referer': 'https://d2y873tmoumjr5.cloudfront.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    response = requests.get(url, headers=headers, params={'Initdata': account})
    if response.status_code == 200:
        data = response.json()
        return data['body']['authorization']
    else:
        print(f"Login failed for account: {account}")
        return None

# Fungsi untuk menjalankan tugas kehadiran harian
def daily_attendance(authorization):
    url = "https://tapadventure.pixelheroes.io/api/receiveAttendanceReward"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'Authorization': f"Bearer {authorization}",
        'Cache-Control': 'no-cache',
        'Content-Length': '2',
        'Content-Type': 'application/json',
        'Pragma': 'no-cache',
        'Referer': 'https://d2y873tmoumjr5.cloudfront.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    response = requests.post(url, headers=headers, json={})
    if response.status_code == 200:
        print("Daily attendance successful")
    else:
        print("Daily attendance failed")

# Fungsi untuk mengekstrak nama pengguna dari data URL-encoded
def extract_username(account):
    parsed_data = urllib.parse.parse_qs(account)
    user_info = parsed_data.get('user', [''])[0]
    user_info_decoded = urllib.parse.unquote(user_info)
    user_json = json.loads(user_info_decoded)
    return user_json.get('username', 'unknown')

# Fungsi utama untuk menjalankan proses
def main():
    accounts = read_accounts('data.txt')
    total_accounts = len(accounts)
    print(f"Total accounts: {total_accounts}")
    
    # Proses login dan tugas kehadiran harian
    for i, account in enumerate(accounts):
        username = extract_username(account)
        print(f"Processing account {i + 1}/{total_accounts} - {username}")
        authorization = login_and_get_authorization(account)
        if authorization:
            daily_attendance(authorization)
            write_authorization({username: authorization})
        time.sleep(5)  # Jeda 5 detik antar akun
    
    # Hitung mundur 6 jam
    next_run_time = datetime.now() + timedelta(hours=6)
    print(f"Next run at {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
    while datetime.now() < next_run_time:
        time_left = next_run_time - datetime.now()
        print(f"Time left: {time_left}", end='\r')
        time.sleep(1)
    
    # Mulai ulang proses
    main()

if __name__ == "__main__":
    main()
