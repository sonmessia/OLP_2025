from fastapi import APIRouter, Request, HTTPException
import json

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.post("/high-co")
async def handle_high_co_alert(request: Request):
    """
    Endpoint này sẽ nhận thông báo từ Orion-LD khi có mức CO cao.
    """
    try:
        notification_payload = await request.json()

        print("=" * 50)
        print("🚨 HIGH CO ALERT RECEIVED! 🚨")
        print(json.dumps(notification_payload, indent=2))
        print("=" * 50)

        # --- Nơi để xử lý logic nghiệp vụ ---
        # Ví dụ: Gửi email, gửi tin nhắn Telegram, lưu vào một DB khác, v.v.
        # for entity in notification_payload.get('data', []):
        #     device_id = entity.get('refDevice')
        #     co_value = entity.get('CO')
        #     print(f"-> Alert from Device: {device_id}, CO Value: {co_value}")

        return {"status": "notification_received"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
