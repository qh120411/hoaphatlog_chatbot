logistics-chatbot/
```
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