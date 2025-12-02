## Session Notes – BiteWise Project (AWS Lex + Bedrock Coach)

Last updated: 2025‑11‑26  
Environment: `bitewise` repo on Windows + WSL  

### Context
- BiteWise FastAPI + frontend project implementing requirements from *Project Description (3).pdf*.
- Support workspace must use Amazon Lex/Bedrock as an in-app coach.
- AWS resources in play: S3 bucket (`bitewise-ai-uploads`), Rekognition, Lex bot (`bitewise-ai-bot`), Bedrock via Lambda (`bitewise-bedrock-coach`).

### Key Changes Discussed
1. **Support notifications** – Fixed SQLAlchemy session issue, improved serialization.
2. **Chatbot route** – `/support/chat` now proxies directly to Lex (and respects either `text` or `question` payloads).
3. **Frontend UX** – All feature panels render human-readable cards for results (no `[object Object]`).
4. **Bedrock Coach**  
   - Lambda `bitewise-bedrock-coach` calls Bedrock (`anthropic.claude-3-haiku...`) and returns Lex-style messages.  
   - IAM role `bitewise-bedrock-coach-role-*` has `AmazonBedrockFullAccess` + Lambda logging perms.
   - Lex intent `CoachIntent` added with representative utterances and fulfillment wired to the Lambda.

### Notes on Lex / Bedrock Wiring
1. **Lambda code skeleton** (in AWS console):
   ```python
   import json, os, boto3
   bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

   def lambda_handler(event, context):
       user_text = event.get("inputTranscript", "") or "Hello"
       prompt = (
           "You are BiteWise Coach. Give concise nutrition guidance.\n"
           f"User: {user_text}\nCoach:"
       )
       response = bedrock.invoke_model(
           modelId="anthropic.claude-3-haiku-20240307-v1:0",
           body=json.dumps({"prompt": prompt, "max_tokens": 400, "temperature": 0.7})
       )
       body = json.loads(response["body"].read().decode("utf-8"))
       reply = body.get("completion", "").strip() or "Ask me about meals, allergies, or swaps!"
       return {"sessionState": event.get("sessionState", {}), "messages": [{"contentType": "PlainText", "content": reply}]}
   ```
2. **Lex steps (CoachIntent)**  
   - Add intent → sample utterances (allergy questions, swaps, etc.).  
   - Fulfillment → use Lambda (`bitewise-bedrock-coach`).  
   - Build draft, create a new bot version, then associate alias `ChatAlias` with that version.
3. **Testing tip** – The default `TestBotAlias` cannot be removed and lacks the Lambda. Always use the alias page (`Deployment → Aliases → ChatAlias → Test`) to verify responses.

### Open Tasks / Reminders
- Recreate `ChatAlias` (or repoint it) whenever you add intents: **Build** ➜ **Create version** ➜ **Associate version with alias**.
- The support UI will reflect Lex responses once the alias is updated; no frontend changes needed.
- If Lex returns “No response from bot,” confirm the alias points to the latest version and the Lambda role still has Bedrock permissions.

### Project Description Excerpt (for context)
BiteWise is a mobile/ops console hybrid that:
- Rates meals (Good/Mid/Bad) via photos or ingredients, stores data in PostgreSQL, and keeps images in S3.
- Generates budget-aware meal plans, searchable recommendations, reminders, FAQs, and chatbot support.
- Uses S3 for photos, PostgreSQL/SQLite for structured data, Redis (planned) for cache, AWS Rekognition for labels, and now Bedrock via Lex for conversational guidance.

This file is a lightweight replacement for the chat transcript so you can resume work after restarting Cursor/WSL. Update it as you iterate.

