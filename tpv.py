import time
import requests
import random
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
        "Initdata": init_data,
        "User-Agent": user_agent,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Login successful")
        data = response.json()
        auto_count = data.get('autoCount', 0)
        auto_damage = data.get('autoDamage', 0)
        return True, auto_count, auto_damage
    else:
        print(f"Login failed with status code: {response.status_code}")
        return False, None, None

# Fungsi untuk menghitung akumulasi autoDamage
def calculate_accumulated_damage(last_login_time, current_time, base_auto_damage):
    elapsed_time = current_time - last_login_time
    elapsed_seconds = elapsed_time.total_seconds()
    accumulated_damage = base_auto_damage + int(elapsed_seconds)
    return accumulated_damage

# Fungsi untuk melakukan request tap tap
def tap_tap(auth_header, init_data, user_agent, last_login_time, base_auto_count, base_auto_damage):
    url = "https://tapadventure.pixelheroes.io/api/tapTouch"
    headers = {
        "Authorization": auth_header,
        "Initdata": init_data,
        "User-Agent": user_agent,
        "Content-Type": "application/json"
    }

    total_touch_count = 0
    current_time = datetime.now()

    accumulated_damage = calculate_accumulated_damage(last_login_time, current_time, base_auto_damage)

    for _ in range(10):
        touch_count = random.randint(170, 180)
        total_touch_count += touch_count
        payload = {
            "touchCount": touch_count,
            "autoCount": base_auto_count,
            "autoDamage": accumulated_damage
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Tap tap request successful: status 200")
        elif response.status_code == 202:
            print("Tap tap request accepted: status 202")
        elif response.status_code == 203:
            print("Tap tap request failed: REDUNDANT_CONNECTION")
            break
        else:
            print(f"Tap tap request failed with status code: {response.status_code}")
        base_auto_count += 1
        accumulated_damage += 1
        time.sleep(3)
    
    print(f"Total touch count for this account: {total_touch_count}")

# Fungsi untuk melakukan request gatcha
def gatcha(auth_header, init_data, user_agent):
    url = "https://tapadventure.pixelheroes.io/api/gatCha"
    headers = {
        "Authorization": auth_header,
        "Initdata": init_data,
        "User-Agent": user_agent,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Gatcha request successful")
    elif response.status_code == 201:
        print("Gatcha request failed: COIN_IS_NOT_ENOUGH")
    else:
        print(f"Gatcha request failed with status code: {response.status_code}")

# Fungsi untuk menjalankan hitung mundur
def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
    print("Countdown finished.")

# Fungsi utama untuk mengelola semua proses
def main(gatcha_enabled, login_only):
    data = read_data('data.txt')
    num_accounts = len(data) // 2
    print(f"Total accounts: {num_accounts}")

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"

    last_login_time = datetime.now() - timedelta(hours=6)

    for i in range(num_accounts):
        auth_header = data[i * 2]
        init_data = data[i * 2 + 1]
        username = extract_username(init_data)
        print(f"Processing account {i + 1} of {num_accounts}: {username}")

        # Melakukan login sebelum menjalankan tugas
        login_successful, base_auto_count, base_auto_damage = login(init_data, user_agent)
        if login_successful:
            if not login_only:
                # Menjalankan tugas tap tap
                tap_tap(auth_header, init_data, user_agent, last_login_time, base_auto_count, base_auto_damage)

            if gatcha_enabled:
                # Menampilkan waktu untuk tugas gatcha berikutnya
                next_gatcha_time = datetime.now() + timedelta(seconds=5600)
                print(f"Next gatcha task for account {i + 1} ({username}) will be at {next_gatcha_time.strftime('%Y-%m-%d %H:%M:%S')}")

                # Menjalankan tugas gatcha
                gatcha(auth_header, init_data, user_agent)
        
        # Jeda 5 detik sebelum akun berikutnya
        time.sleep(5)
    
    if login_only:
        print("All accounts logged in. Starting 6 hours and 5 minutes countdown.")
        countdown_timer(6 * 3600 + 5 * 60)
        print("Restarting login process.")
        main(gatcha_enabled, login_only)
    else:
        print("All accounts processed. Starting 1 hour countdown.")
        countdown_timer(3600)
        print("Restarting process.")
        main(gatcha_enabled, login_only)

if __name__ == "__main__":
    gatcha_enabled = input("Do you want to enable the gatcha task? (yes/no): ").strip().lower() == "yes"
    login_only = input("Do you want to only login and calculate accumulated damage? (yes/no): ").strip().lower() == "yes"
    main(gatcha_enabled, login_only)
