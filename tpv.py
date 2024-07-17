import time
import requests
import random
import json

# Fungsi untuk membaca data dari file data.txt
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read().splitlines()
    return data

# Fungsi untuk melakukan request tap tap
def tap_tap(auth_header, init_data):
    url = "https://tapadventure.pixelheroes.io/api/tapTouch"
    headers = {
        "Authorization": auth_header,
        "Initdata": init_data,
        "Content-Type": "application/json"
    }

    for _ in range(10):
        touch_count = random.randint(170, 180)
        payload = {
            "touchCount": touch_count,
            "autoCount": 12,
            "autoDamage": 12
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Tap tap request successful:", response.json())
        else:
            print("Tap tap request failed:", response.status_code)
        time.sleep(3)

# Fungsi untuk melakukan request gatcha
def gatcha(auth_header, init_data):
    url = "https://tapadventure.pixelheroes.io/api/gatCha"
    headers = {
        "Authorization": auth_header,
        "Initdata": init_data,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Gatcha request successful:", response.json())
    else:
        print("Gatcha request failed:", response.status_code)

# Fungsi untuk menjalankan hitung mundur
def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
    print("Countdown finished.")

# Fungsi utama untuk mengelola semua proses
def main():
    data = read_data('data.txt')
    num_accounts = len(data) // 2
    print(f"Total accounts: {num_accounts}")

    for i in range(num_accounts):
        auth_header = data[i * 2]
        init_data = data[i * 2 + 1]
        print(f"Processing account {i + 1} of {num_accounts}")
        
        # Menjalankan tugas tap tap
        tap_tap(auth_header, init_data)
        # Menjalankan tugas gatcha
        gatcha(auth_header, init_data)
        
        # Jeda 5 detik sebelum akun berikutnya
        time.sleep(5)
    
    print("All accounts processed. Starting 1 hour countdown.")
    countdown_timer(3600)
    print("Restarting process.")
    main()

if __name__ == "__main__":
    main()
