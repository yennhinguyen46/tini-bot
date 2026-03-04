# 🌸 Tí Nị Bot – Telegram AI Bot

Một con bot AI thân thiện trên Telegram, sử dụng GPT của OpenAI để trò chuyện bằng tiếng Việt.

---

## ✨ Tính năng

- 💬 Trò chuyện thông minh với GPT-4o-mini
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
| `MAX_HISTORY` | Số tin nhắn lịch sử lưu giữ | `20` |

---

## 📁 Cấu trúc dự án

```
Tí Nị bot/
├── bot.py           # File chính của bot
├── requirements.txt # Các thư viện cần thiết
├── .env             # Cấu hình (không commit lên git!)
├── .env.example     # Mẫu cấu hình
└── README.md        # Hướng dẫn này
```
