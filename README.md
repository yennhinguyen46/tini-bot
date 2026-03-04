# 🌸 Tí Nị Bot – Telegram AI Bot

Một con bot AI thân thiện trên Telegram, sử dụng GPT của OpenAI để trò chuyện bằng tiếng Việt.

---

## ✨ Tính năng

- 💬 Trò chuyện thông minh với GPT-4o-mini hoặc GPT-4o
- 🕐 **Biết thời gian thực** - Tự động cập nhật ngày giờ hiện tại
- 🧮 **Tính toán chính xác** - Giải các bài toán phức tạp
- 🔍 **Tìm kiếm Google** - Tự động tìm thông tin mới nhất khi cần
- 👁 **Xem và phân tích ảnh** - Hiểu nội dung hình ảnh
- 🎨 **Tạo ảnh AI** - Vẽ ảnh theo yêu cầu bằng DALL-E 3
- 🧠 Nhớ lịch sử hội thoại theo từng người dùng
- 🇻🇳 Phản hồi bằng tiếng Việt tự nhiên
- 🔄 Bắt đầu cuộc hội thoại mới với `/new`
- ⌨️ Hiển thị trạng thái "đang gõ..." khi xử lý

---

## 🚀 Cài đặt

### Bước 1 – Tạo Telegram Bot

1. Mở Telegram, tìm **@BotFather**
2. Gõ `/newbot` và làm theo hướng dẫn
3. Sao chép **Token** được cấp

### Bước 2 – Lấy OpenAI API Key

1. Truy cập [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Tạo API key mới và sao chép lại

### Bước 3 – Cấu hình môi trường

```bash
# Sao chép file .env mẫu
cp .env.example .env
```

Mở file `.env` và điền thông tin:

```
TELEGRAM_BOT_TOKEN=token_của_bạn
OPENAI_API_KEY=api_key_của_bạn
OPENAI_MODEL=gpt-4o-mini
```

### Bước 4 – Cài thư viện

```bash
pip install -r requirements.txt
```

### Bước 5 – Chạy bot

```bash
python bot.py
```

---

## 📋 Các lệnh

| Lệnh | Mô tả |
|------|-------|
| `/start` | Chào mừng & reset hội thoại |
| `/new` | Bắt đầu cuộc trò chuyện mới |
| `/help` | Xem hướng dẫn |
| `/about` | Thông tin về bot |

---

## ⚙️ Tuỳ chỉnh

Chỉnh sửa trong file `.env`:

| Biến | Mô tả | Mặc định |
|------|-------|---------|
| `BOT_NAME` | Tên của bot | `Tí Nị` |
| `BOT_PERSONALITY` | Tính cách/system prompt | Thân thiện, vui vẻ |
| `OPENAI_MODEL` | Model AI sử dụng | `gpt-4o-mini` |
| `MAX_HISTORY` | Số tin nhắn lịch sử lưu giữ | `20` |

### Lựa chọn Model

- **`gpt-4o-mini`** (mặc định): Nhanh, rẻ, phù hợp sử dụng thường ngày
- **`gpt-4o`**: Thông minh hơn, phức tạp hơn, nhưng đắt hơn (~15-20x)

---

## 🧠 Khả năng đặc biệt

### 🕐 Nhận biết thời gian thực

Bot tự động biết ngày giờ hiện tại và có thể trả lời các câu hỏi như:
- "Hôm nay là thứ mấy?"
- "Bây giờ là mấy giờ?"
- "Hôm nay ngày bao nhiêu?"

### 🧮 Tính toán toán học

Bot có thể tính toán chính xác các phép toán phức tạp:
- "Tính 2^10 + 50"
- "Căn bậc hai của 144 là bao nhiêu?"
- "sin(45) + cos(30)"

### 🔍 Tìm kiếm thông tin realtime

Bot tự động tìm Google khi cần thông tin mới nhất về:
- Tin tức, sự kiện hiện tại
- Giá cả, tỷ giá
- Thời tiết
- Thông tin cập nhật

---

## 📁 Cấu trúc dự án

```
Tí Nị bot/
├── bot.py              # File chính của bot
├── soul.md             # Tính cách chi tiết của Tí Nị
├── knowledge.md        # Kiến thức bổ sung
├── requirements.txt    # Các thư viện cần thiết
├── .env                # Cấu hình (không commit lên git!)
├── .env.example        # Mẫu cấu hình
├── README.md           # Hướng dẫn này
├── QUICK_START.md      # Hướng dẫn nhanh
└── DEPLOY_BYTEPLUS.md  # Hướng dẫn deploy lên VM
```

---

## 🚀 Deploy lên Production

Xem hướng dẫn chi tiết tại [DEPLOY_BYTEPLUS.md](DEPLOY_BYTEPLUS.md)

---

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Tạo issue hoặc pull request.

---

## 📄 License

MIT License - Tự do sử dụng và chỉnh sửa
