import subprocess
import time
import os
import multiprocessing

def start_appium_server():
    print("Khởi động Appium server...")
    subprocess.run(["appium"], shell=True)

def start_emulator():
    print("Khởi động thiết bị ảo (ví dụ: Android Emulator)...")
    subprocess.run(["emulator", "-avd", "Pixel_5_API_30"])
    # emulator -avd Pixel_5_API_30

def run_test():
    print("Run TestScript...")
    os.system("pytest -m MobileChat")

def close_appium_server():
    print("Tắt Appium server...")
    subprocess.run(["TASKKILL", "/F", "/IM", "node.exe"], shell=True)

def close_emulator():
    print("Tắt thiết bị ảo (ví dụ: Android Emulator)...")
    subprocess.run(["adb", "-e", "emu", "kill"], shell=True)


if __name__ == "__main__":
    # Tạo các tiến trình riêng biệt cho mỗi công việc
    appium_process = multiprocessing.Process(target=start_appium_server)
    emulator_process = multiprocessing.Process(target=start_emulator)
    close_appium_process = multiprocessing.Process(target=close_appium_server)
    close_emulator_process = multiprocessing.Process(target=close_emulator)

    # Khởi tạo môi trường test
    emulator_process.start()
    time.sleep(5)
    appium_process.start()
    # Chờ 5 giây sau khi khởi động Appium và Emulator
    time.sleep(5)
    # Run Test
    run_test()
    # Dọn dẹp môi trường
    close_appium_process.start()
    close_emulator_process.start()
