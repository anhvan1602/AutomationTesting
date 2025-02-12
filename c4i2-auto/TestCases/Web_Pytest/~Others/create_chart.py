import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Đọc dữ liệu JSON từ file
with open('allure-report/data/timeline.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# Hàm đệ quy để trích xuất thời gian và tên test case
def extract_test_case_data(children, results=None):
    if results is None:
        results = []

    for child in children:
        if 'children' in child:
            # Nếu có các test case con, gọi đệ quy
            extract_test_case_data(child['children'], results)
        elif 'time' in child:
            # Trích xuất thông tin thời gian và tên test case
            test_case_name = child.get('name', 'Unknown')
            start_time = pd.to_datetime(child['time']['start'], unit='ms')
            duration = child['time']['duration'] / 1000  # duration in seconds
            results.append((test_case_name, start_time, duration))

    return results


# Trích xuất dữ liệu từ JSON
test_case_data = extract_test_case_data(data['children'])

# Chuyển dữ liệu thành DataFrame
df = pd.DataFrame(test_case_data, columns=['Test Case', 'Start Time', 'Duration'])

# Tạo biểu đồ
fig, ax = plt.subplots(figsize=(16, 10))

# Vẽ biểu đồ đường (line chart) thể hiện thời gian thực thi của từng test case
lines = {}
for test_case in df['Test Case'].unique():
    # Lọc các dòng dữ liệu cho từng test case
    case_data = df[df['Test Case'] == test_case]
    line, = ax.plot(case_data['Start Time'], case_data['Duration'], marker='o', label=test_case)
    lines[line] = test_case  # Lưu trữ thông tin line và tên test case

# Cấu hình cho biểu đồ
ax.set_title('Test Case Execution Time')
ax.set_xlabel('Start Time')
ax.set_ylabel('Duration (seconds)')
plt.xticks(rotation=45)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

# Đặt chú thích ở bên phải biểu đồ
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Test Cases")

# Tạo chú thích động cho tên test case khi di chuột
tooltip = ax.annotate("", xy=(0, 0), xytext=(20, 20),
                      textcoords="offset points", ha="center", fontsize=9,
                      bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.5),
                      arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"))
tooltip.set_visible(False)


# Hàm cập nhật tooltip khi di chuột
def on_hover(event):
    # Kiểm tra xem chuột có nằm trong vùng biểu đồ không
    if event.inaxes == ax:
        for line in lines:
            # Lấy thông tin dữ liệu của line
            cont, ind = line.contains(event)
            if cont:
                # Nếu di chuột vào điểm dữ liệu, hiển thị tooltip
                test_case_name = lines[line]
                x, y = line.get_data()
                tooltip.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
                tooltip.set_text(f"{test_case_name}\nDuration: {y[ind['ind'][0]]} s")
                tooltip.set_visible(True)
                fig.canvas.draw_idle()
                return
    tooltip.set_visible(False)
    fig.canvas.draw_idle()


# Kết nối sự kiện di chuột với hàm cập nhật tooltip
fig.canvas.mpl_connect("motion_notify_event", on_hover)

# Hiển thị biểu đồ
plt.tight_layout()
plt.show()
