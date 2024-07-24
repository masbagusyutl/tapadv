import time
from datetime import datetime, timedelta
import urllib.parse
import requests

# Baca data dari file
with open('data.txt', 'r') as file:
    lines = file.read().strip().split('\n')

# Pisahkan data Initdata dan Authorization
initdata_list = []
authorization_list = []

# Mengasumsikan data setiap akun dimulai dengan baris query_id, diikuti oleh baris auth
for i in range(0, len(lines), 2):
    initdata_list.append(lines[i])
    authorization_list.append(lines[i + 1])

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
        # Tugas login
        print(f"Akun {idx+1} - Memulai tugas login")
        login_status = tugas_login(initdata)
        if login_status == 200:
            print(f"Akun {idx+1} berhasil login")
        else:
            print(f"Akun {idx+1} gagal login")
            continue  # Lewati tugas kehadiran harian jika login gagal

        # Tugas kehadiran harian
        print(f"Akun {idx+1} - Memulai tugas kehadiran harian")
        attendance_status = tugas_kehadiran_harian(initdata, auth)
        if attendance_status == 200:
            print(f"Akun {idx+1} berhasil menyelesaikan tugas harian")
        else:
            print(f"Akun {idx+1} gagal menyelesaikan tugas harian")

        time.sleep(5)  # Jeda 5 detik antar akun

    # Hitung mundur 6 jam
    next_run_time = datetime.now() + timedelta(hours=6)
    print(f"\nSemua akun telah diproses. Hitung mundur 6 jam hingga {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
    while datetime.now() < next_run_time:
        remaining_time = next_run_time - datetime.now()
        print(f"Hitung mundur: {remaining_time}", end='\r')
        time.sleep(1)

while True:
    jalankan_tugas()
