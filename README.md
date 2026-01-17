# Gmail Schedule Watcher

Schedule Gmail messages for specific threads and automatically cancel them if a new email arrives in that thread.

To use:
    1. Create a Google Cloud project and enable Gmail API
    2. Download OAuth credentials as credentials.json to the backend directory
    3. On first run, you'll be prompted to authorize - this generates token.json


API endpoint:

POST /api/schedule-email
{
"thread_id": "unique-id-or-gmail-thread-id",
"to": "recipient@example.com",
"subject": "Email subject",
"message_content": "Email body",
"scheduled_time": "2024-01-20T10:00:00Z",
"message_count_at_schedule": 0
}