import requests
import time
from datetime import datetime, timedelta
import urllib.parse

# Baca data dari file
with open('data.txt', 'r') as file:
    data = file.read().split("\n\n")

# Pisahkan data Initdata dan Authorization
initdata_list = [block.split('\n')[1].split(": ")[1] for block in data if 'Initdata:' in block]
authorization_list = [block.split('\n')[1].split(": ")[1] for block in data if 'Authorization: Bearer ' in block]

# Fungsi untuk mengekstrak nama pengguna dari Initdata
def ambil_nama_pengguna(initdata):
    params = urllib.parse.parse_qs(initdata)
    user_info = params.get('user', [''])[0]
    username_start = user_info.find('username%22%3A%22') + len('username%22%3A%22')
    username_end = user_info.find('%22', username_start)
    if username_start > len('username%22%3A%22') - 1 and username_end > username_start:
        username = urllib.parse.unquote(user_info[username_start:username_end])
        return username
    return "Unknown"

# Fungsi untuk tugas login
def tugas_login(initdata):
    url = "https://tapadventure.pixelheroes.io/api/init"
    headers = {
        "authority": "tapadventure.pixelheroes.io",
        "method": "GET",
        "path": "/api/init",
        "scheme": "https",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0",
        "Initdata": initdata
    }
    response = requests.get(url, headers=headers)
    return response.status_code

# Fungsi untuk tugas kehadiran harian
def tugas_kehadiran_harian(initdata, auth):
    url = "https://tapadventure.pixelheroes.io/api/receiveAttendanceReward"
    headers = {
        "authority": "tapadventure.pixelheroes.io",
        "method": "POST",
        "path": "/api/receiveAttendanceReward",
        "scheme": "https",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Authorization": f"Bearer {auth}",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Initdata": initdata
    }
    response = requests.post(url, headers=headers, json={})
    return response.status_code

# Fungsi utama untuk menjalankan tugas
def jalankan_tugas():
    akun_total = len(initdata_list)
    for idx, (initdata, auth) in enumerate(zip(initdata_list, authorization_list)):
        username = ambil_nama_pengguna(initdata)
        print(f"Memproses akun {idx+1} dari {akun_total} - Username: {username}")
        login_status = tugas_login(initdata)
        if login_status == 200:
            print(f"Login sukses untuk {username}")
        else:
            print(f"Login gagal untuk {username}")

        attendance_status = tugas_kehadiran_harian(initdata, auth)
        if attendance_status == 200:
            print(f"Kehadiran harian sukses untuk {username}")
        else:
            print(f"Kehadiran harian gagal untuk {username}")

        time.sleep(5)  # Jeda 5 detik antar akun
    
    # Hitung mundur 6 jam
    next_run_time = datetime.now() + timedelta(hours=6)
    print(f"Tugas harian selesai. Akan dimulai lagi pada {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
    while datetime.now() < next_run_time:
        remaining_time = next_run_time - datetime.now()
        print(f"Hitung mundur: {remaining_time}", end='\r')
        time.sleep(1)

while True:
    jalankan_tugas()
