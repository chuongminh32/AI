import matplotlib.pyplot as plt

# Dữ liệu
sectors = ["Công nghiệp", "Xây dựng", "Thương mại, dịch vụ", "Vận tải", "Các ngành khác"]
percentages = [46.1, 15.0, 25.9, 4.7, 8.3]

# Tạo biểu đồ tròn
fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(
    percentages,
    labels=sectors,
    autopct='%1.1f%%',
    startangle=140,
    textprops={'fontsize': 12}
)

# Tiêu đề biểu đồ
plt.title("Tỷ lệ phân bố lao động theo ngành kinh tế tại Việt Nam", fontsize=16, fontweight='bold', pad=30)

# Ghi chú nguồn bên dưới
fig.text(0.5, 0.02, "Nguồn: Tổng cục Thống kê Việt Nam, năm 2023", ha='center', fontsize=10)

# Đảm bảo hình tròn
ax.axis('equal')

# Tăng khoảng cách giữa biểu đồ và mép hình
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.show()
