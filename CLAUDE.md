# CLAUDE.md - twitch-sdk

## Project Overview

Complete Twitch Helix API SDK with Pydantic validation for all 170+ endpoints.

## Architecture

```
twitch-sdk/
├── src/twitch_sdk/
│   ├── __init__.py      # Public exports
│   ├── client.py        # TwitchSDK main class
│   ├── endpoints/       # API endpoint functions
│   │   ├── ads.py
│   │   ├── chat.py
│   │   ├── streams.py
│   │   └── ... (26 modules)
│   └── schemas/         # Pydantic models
│       ├── base.py      # TwitchResponse, Pagination
│       ├── ads.py
│       ├── chat.py
│       └── ... (26 modules)
└── tests/
```

## Pattern

Each endpoint module follows this pattern:

```python
# endpoints/chat.py
async def send_chat_message(client, params: SendMessageRequest) -> TwitchResponse[SendMessageResponse]:
    response = await client.post("/chat/messages", data=params.model_dump())
    return TwitchResponse[SendMessageResponse].model_validate(response)
```

## Common Tasks

```bash
# Install dependencies
cd ~/twitch-sdk && poetry install

# Run tests
poetry run pytest

# Test import
poetry run python -c "from twitch_sdk import TwitchSDK; print('ok')"
```

## Dependencies

- twitch-client (auth layer)
- pydantic
- websockets (EventSub)

## Used By

- twitch-mcp (MCP wrapper)
