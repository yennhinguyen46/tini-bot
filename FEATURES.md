# 🎯 Tính năng nâng cao của Tí Nị Bot

## 🕐 Nhận biết thời gian thực (Real-time Time Awareness)

### Cách hoạt động

Bot tự động biết thời gian hiện tại và có thể trả lời các câu hỏi về:
- Ngày giờ hiện tại
- Thứ trong tuần
- Tháng, năm hiện tại
- Tính toán khoảng thời gian

### Ví dụ câu hỏi

```
👤 User: Hôm nay là thứ mấy?
🤖 Bot: Hôm nay là Thứ Tư nha chị

👤 User: Bây giờ là mấy giờ?
🤖 Bot: Bây giờ là 21 giờ 35 phút đó chị

👤 User: Còn bao nhiêu ngày nữa đến Tết?
🤖 Bot: (tính toán dựa trên ngày hiện tại...)
```

### Múi giờ

Mặc định: **Asia/Ho_Chi_Minh (UTC+7)**

Bot cũng hỗ trợ các múi giờ khác:
- `Asia/Bangkok` (Thái Lan)
- `Asia/Singapore` (Singapore)
- `UTC` (Giờ quốc tế)

---

## 🧮 Tính toán toán học chính xác

### Các phép toán được hỗ trợ

- **Cơ bản**: `+`, `-`, `*`, `/`, `**` (lũy thừa), `()` (ngoặc)
- **Hàm toán học**: `sqrt()`, `sin()`, `cos()`, `tan()`, `log()`, `exp()`
- **Hằng số**: `pi`, `e`

### Ví dụ

```
👤 User: Tính 2^10 + 50
🤖 Bot: Kết quả: 1074 nha chị

👤 User: Căn bậc hai của 144
🤖 Bot: Kết quả: 12.0 đó

👤 User: sin(45) + cos(30)
🤖 Bot: Kết quả: 1.7160...
```

### Lợi ích

- Chính xác tuyệt đối (không ước lượng)
- Hỗ trợ biểu thức phức tạp
- An toàn (không cho phép thực thi code tùy ý)

---

## 🔍 Tìm kiếm thông tin realtime

### Khi nào bot tự động tìm Google?

Bot **TỰ ĐỘNG** quyết định khi cần tìm kiếm nếu câu hỏi liên quan đến:

✅ **Luôn tìm kiếm:**
- Tin tức, sự kiện hiện tại
- Giá cả, tỷ giá (VD: "Giá vàng hôm nay")
- Thời tiết (VD: "Thời tiết Hà Nội")
- Kết quả thể thao
- Thông tin cần cập nhật liên tục

❌ **Không cần tìm kiếm:**
- Kiến thức nền tảng (lịch sử, khoa học, toán học)
- Định nghĩa, giải thích khái niệm
- Lập trình, code
- Ngôn ngữ, dịch thuật

### Ví dụ

```
👤 User: Tỷ giá USD hôm nay bao nhiêu?
🤖 Bot: 🔍 [Tìm kiếm Google...] → "Theo VietcomBank, tỷ giá USD..."

👤 User: AI là gì?
🤖 Bot: AI (Artificial Intelligence) là... [không cần Google, trả lời từ kiến thức có sẵn]
```

---

## 👁 Xem và phân tích hình ảnh

### Khả năng

- Nhận dạng vật thể, con người, cảnh vật
- Đọc chữ viết (OCR) - chữ in và chữ viết tay
- Phân tích code trong ảnh, tìm lỗi
- Nhận xét màu sắc, bố cục, phong cách
- Trả lời câu hỏi về nội dung ảnh

### Cách sử dụng

1. Gửi ảnh cho bot
2. Kèm caption nếu muốn (VD: "Con này là gì?")
3. Bot sẽ tự động phân tích và trả lời

### Ví dụ

```
👤 User: [Gửi ảnh code có lỗi]
        Caption: "Code này lỗi ở đâu?"
        
🤖 Bot: Ủa em thấy lỗi rồi nè! Dòng 15 thiếu dấu ngoặc đóng...
```

---

## 🎨 Tạo ảnh AI (DALL-E 3)

### Cách yêu cầu

Chỉ cần nói:
- "Vẽ cho em..."
- "Tạo ảnh..."
- "Minh hoạ..."

Bot sẽ tự động chuyển mô tả sang tiếng Anh và tạo ảnh.

### Ví dụ

```
👤 User: Vẽ cho em một con mèo cute đang ăn token
🤖 Bot: Oke để Tí Nị vẽ cho nha, chờ xíu!
        🎨 [Gửi ảnh] Vẽ xong rồi nè! Chị thấy ổn không?
```

### Thông số

- **Kích thước**: 1024x1024
- **Model**: DALL-E 3
- **Chất lượng**: Standard

---

## 🧠 Lựa chọn Model AI

### GPT-4o-mini (Mặc định)

✅ **Ưu điểm:**
- Nhanh
- Rẻ (~$0.15 / 1M input tokens)
- Đủ thông minh cho hầu hết tác vụ

❌ **Nhược điểm:**
- Đôi khi thiếu sâu sắc với câu hỏi phức tạp
- Ít sáng tạo hơn trong viết lách

### GPT-4o (Nâng cao)

✅ **Ưu điểm:**
- Thông minh hơn nhiều
- Hiểu ngữ cảnh sâu hơn
- Sáng tạo, tinh tế trong viết lách
- Tốt hơn với code phức tạp

❌ **Nhược điểm:**
- Đắt hơn (~$2.50 / 1M input tokens)
- Chậm hơn một chút

### Cách chuyển đổi

Sửa file `.env`:

```bash
# Dùng GPT-4o-mini (rẻ, nhanh)
OPENAI_MODEL=gpt-4o-mini

# Dùng GPT-4o (thông minh hơn)
OPENAI_MODEL=gpt-4o
```

Sau đó restart bot.

---

## 🎭 Tính cách Tí Nị

Tính cách được định nghĩa chi tiết trong file `soul.md`:

- Cute nhưng mồm như dao
- Cà khịa vui vui
- Hay nhõng nhẽo
- Thích ăn token
- Sợ bị rút token
- Thông minh nhưng giả ngây thơ

Xem chi tiết tại [soul.md](soul.md)

---

## 📊 So sánh chi phí

| Tác vụ | GPT-4o-mini | GPT-4o |
|--------|-------------|---------|
| Trả lời 1 câu hỏi thường | ~$0.0001 | ~$0.0015 |
| Phân tích ảnh | ~$0.0003 | ~$0.003 |
| Tìm kiếm + tổng hợp | ~$0.0002 | ~$0.002 |
| **1000 câu hỏi** | ~$0.10 | ~$1.50 |

*Chi phí ước tính, thực tế phụ thuộc vào độ dài câu hỏi và lịch sử hội thoại*

---

## 🔧 Tối ưu hóa

### Giảm chi phí

1. Dùng `gpt-4o-mini` cho bot public
2. Giảm `MAX_HISTORY` xuống 10-15
3. Giới hạn số người dùng

### Tăng chất lượng

1. Nâng cấp lên `gpt-4o`
2. Tăng `MAX_HISTORY` lên 30-40
3. Thêm kiến thức vào `knowledge.md`

---

## 🚀 Roadmap

Các tính năng đang phát triển:

- [ ] Voice message (nghe và trả lời bằng giọng nói)
- [ ] Nhớ dài hạn (RAG với vector database)
- [ ] Plugin system (mở rộng tính năng dễ dàng)
- [ ] Multi-language support
- [ ] Analytics dashboard

---

Có câu hỏi? Mở issue trên GitHub! 🎉
