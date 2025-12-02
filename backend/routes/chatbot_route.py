import os
import uuid

import boto3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class ChatPayload(BaseModel):
    text: str | None = None
    question: str | None = None
    locale: str = "en_US"


router = APIRouter(prefix="/support/chat", tags=["Chatbot"])


def _lex_client():
    region = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client(
        "lexv2-runtime",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


@router.post("")
async def chat_with_bot(payload: ChatPayload):
    """Send a chat message to Amazon Lex V2 and return the bot reply."""
    try:
        bot_id = os.getenv("LEX_BOT_ID")
        alias_id = os.getenv("LEX_BOT_ALIAS_ID")
        if not bot_id or not alias_id:
            raise HTTPException(status_code=500, detail="Lex bot configuration missing.")

        client = _lex_client()
        message = payload.text or payload.question
        if not message:
            raise HTTPException(status_code=400, detail="Provide 'text' or 'question'.")

        response = client.recognize_text(
            botId=bot_id,
            botAliasId=alias_id,
            localeId=payload.locale,
            sessionId=str(uuid.uuid4()),
            text=message,
        )
        messages = response.get("messages", [])
        reply = messages[0]["content"] if messages else "🤖 No response from bot."
        return {"user": message, "bot": reply}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

