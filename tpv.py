import time
from datetime import datetime, timedelta
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

# Fungsi untuk menjalankan semua tugas login dan kehadiran harian
def jalankan_semua_tugas():
    akun_total = len(initdata_list)
    for idx, (initdata, auth) in enumerate(zip(initdata_list, authorization_list)):
        print(f"Memproses akun {idx+1} dari {akun_total}")

        # Tugas login
        print(f"Memulai tugas login untuk akun {idx+1}")
        login_status = tugas_login(initdata)
        if login_status == 200:
            print(f"Akun {idx+1} berhasil login")
        else:
            print(f"Akun {idx+1} gagal login")
            continue  # Lewati tugas kehadiran harian jika login gagal

        # Tugas kehadiran harian
        print(f"Memulai tugas kehadiran harian untuk akun {idx+1}")
        attendance_status = tugas_kehadiran_harian(initdata, auth)
        if attendance_status == 200:
            print(f"Akun {idx+1} berhasil menyelesaikan tugas harian")
        else:
            print(f"Akun {idx+1} gagal menyelesaikan tugas harian")

        time.sleep(5)  # Jeda 5 detik antar akun

def jadwalkan_tugas():
    next_login_time = datetime.now() + timedelta(hours=6)
    next_attendance_time = datetime.now() + timedelta(hours=24)

    while True:
        now = datetime.now()

        # Jalankan tugas login jika waktu sudah tiba
        if now >= next_login_time:
            print("Waktu untuk menjalankan tugas login telah tiba.")
            jalankan_semua_tugas()  # Jalankan semua tugas login dan kehadiran harian
            next_login_time = now + timedelta(hours=6)  # Atur waktu berikutnya
            print(f"Tugas login berikutnya dijadwalkan pada {next_login_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Jalankan tugas kehadiran harian jika waktu sudah tiba
        if now >= next_attendance_time:
            print("Waktu untuk menjalankan tugas kehadiran harian telah tiba.")
            jalankan_semua_tugas()  # Jalankan semua tugas login dan kehadiran harian
            next_attendance_time = now + timedelta(hours=24)  # Atur waktu berikutnya
            print(f"Tugas kehadiran harian berikutnya dijadwalkan pada {next_attendance_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Hitung mundur dan periksa setiap menit
        remaining_time_login = next_login_time - now
        remaining_time_attendance = next_attendance_time - now
        print(f"Hitung mundur login berikutnya: {remaining_time_login}", end='\r')
        print(f"Hitung mundur kehadiran berikutnya: {remaining_time_attendance}", end='\r')

        time.sleep(60)  # Periksa setiap menit

if __name__ == "__main__":
    print("Menjalankan semua tugas untuk pertama kali...")
    jalankan_semua_tugas()  # Jalankan semua tugas login dan kehadiran harian sekali
    print("Menjadwalkan tugas login dan kehadiran harian...")
    jadwalkan_tugas()  # Mulai jadwal tugas
