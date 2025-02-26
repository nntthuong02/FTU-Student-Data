import aiohttp
import asyncio
import re
import time
from bs4 import BeautifulSoup

# URL cho tra cứu sinh viên
URL = "https://tracuuthongtin.ftu.edu.vn/03_select_tracuuemail_k59.php"
SEMAPHORE = asyncio.Semaphore(1) 

TEST_MSV = "2015810341"

patterns = {
    "Mã sinh viên": r"Mã sinh viên:\s*(\d+)",
    "Họ và Tên": r"Họ và Tên:\s*([\w\sÀ-Ỹà-ỹ]+?)(?=\s*Khóa:)",
    "Khóa": r"Khóa:\s*(K\d+)",
    "Truy cập địa chỉ": r"Truy cập địa chỉ:\s*(http[^\s]+)",
    "Tài khoản truy cập": r"Tài khoản truy cập:\s*([\w.@]+)",
    "Mật khẩu": r"Mật khẩu:\s*([\S]+)"
}

async def fetch_data(session, msv):
    """ Gửi request và lấy thông tin sinh viên """
    async with SEMAPHORE:
        try:
            async with session.post(URL, data={"msv": msv}, timeout=5) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, "html.parser")
                    if "KHÔNG TÌM THẤY THÔNG TIN TRA CỨU" in soup.get_text():
                        return f"❌ Không tìm thấy thông tin cho {msv}"
                    
                    return extract_info(msv, soup)
                else:
                    return f"⚠️ Lỗi HTTP {response.status} khi tra cứu {msv}"
        except Exception as e:
            return f"⚠️ Lỗi khi tra cứu {msv}: {e}"

def extract_info(msv, soup):
    """ Trích xuất thông tin từ trang """
    text = soup.get_text(" ", strip=True)
    data = {"Mã sinh viên tra cứu": msv}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        data[key] = match.group(1) if match else "Không có dữ liệu"

    return data

async def main():
    async with aiohttp.ClientSession() as session:
        result = await fetch_data(session, TEST_MSV)
        print("🔍 Kết quả tra cứu:")
        print(result)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print(f"⏱️ Hoàn thành trong {time.time() - start_time:.2f}s")
