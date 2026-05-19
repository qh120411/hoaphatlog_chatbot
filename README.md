# Logistics AI Chatbot

Hệ thống chatbot nội bộ hỗ trợ quản lý xe logistics thông qua Zalo Webhook, AI và Google Sheets.

Dự án được xây dựng nhằm hỗ trợ các phòng ban tra cứu nhanh thông tin xe, hạn đăng kiểm, lịch bảo dưỡng và các dữ liệu vận hành liên quan.

---

## 1. Mục tiêu dự án

Dự án hướng tới việc xây dựng một chatbot có khả năng:

- Nhận câu hỏi từ người dùng qua Zalo
- Xác minh người dùng dựa trên Zalo User ID
- Phân quyền theo phòng ban
- Phân loại ý định câu hỏi bằng AI
- Truy xuất dữ liệu từ Google Sheets
- Sinh câu trả lời tự nhiên bằng AI
- Gửi phản hồi lại cho người dùng qua Zalo
- Lưu lịch sử tương tác vào MySQL nếu cần

---

## 2. Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Backend | Python Flask |
| AI Model | Gemini 2.5 Flash |
| AI Gateway | 9Router |
| Database | MySQL |
| Business Data | Google Sheets |
| Messaging Platform | Zalo |
| Local Testing | ngrok |
| Environment | Python virtualenv |

---

## 3. Kiến trúc tổng quan

```txt
Zalo User
    ↓
Zalo Webhook
    ↓
Flask Backend
    ↓
User Authentication & Permission Check
    ↓
AI Intent Classification
    ↓
Business Handler
    ↓
Google Sheets / MySQL
    ↓
AI Response Generator
    ↓
Zalo Sender
```

## 4. Cấu trúc thư mục

```
logistics-chatbot/
│
├── app.py
├── config.py
├── .env
├── requirements.txt
│
├── ai/
│   ├── router_client.py
│   ├── intent_classifier.py
│   ├── response_generator.py
│   └── training_data/
│       └── intent_examples.json
│
├── zalo/
│   ├── webhook.py
│   └── sender.py
│
├── handlers/
│   ├── inspection_handler.py
│   ├── maintenance_handler.py
│   └── fallback_handler.py
│
├── services/
│   ├── sheet_service.py
│   ├── auth_service.py
│   └── chat_history_service.py
│
├── database/
│   ├── mysql_client.py
│   └── models/
│       └── chat_history.sql
│
└── utils/
    └── date_utils.py
```
