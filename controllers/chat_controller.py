@app.post("/llm-cv-chat-bot")
async def llm_cv_chat_bot(request: Request):
    data = await request.json()

    print('show me the data:', data)
    print("Hello There")