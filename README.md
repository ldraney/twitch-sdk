# twitch-sdk

[![PyPI](https://img.shields.io/pypi/v/twitch-sdk)](https://pypi.org/project/twitch-sdk/)

Complete Twitch Helix API SDK with Pydantic validation for 170+ endpoints.

## Installation

```bash
pip install twitch-sdk
```

## Credentials Setup

Create `~/.twitch-secrets/.env` with your Twitch credentials:

```bash
TWITCH_CLIENT_ID=your_client_id
TWITCH_CLIENT_SECRET=your_client_secret
TWITCH_ACCESS_TOKEN=your_access_token
TWITCH_REFRESH_TOKEN=your_refresh_token
```

See [twitch-client](https://github.com/ldraney/twitch-client) for detailed setup instructions.

## Usage

### Basic Usage

```python
import asyncio
from twitch_sdk import TwitchSDK
from twitch_sdk.schemas.streams import GetStreamsRequest

async def main():
    async with TwitchSDK() as sdk:
        # Get live streams
        params = GetStreamsRequest(game_id=["509658"])  # Just Chatting
        streams = await sdk.streams.get_streams(sdk.http, params)
        for stream in streams.data:
            print(f"{stream.user_name}: {stream.title}")

asyncio.run(main())
```

### Send Chat Message

```python
from twitch_sdk import TwitchSDK
from twitch_sdk.schemas.chat import SendMessageRequest

async def main():
    async with TwitchSDK() as sdk:
        params = SendMessageRequest(
            broadcaster_id="123456",
            sender_id="123456",
            message="Hello from the SDK!"
        )
        result = await sdk.chat.send_chat_message(sdk.http, params)
        print(f"Message sent: {result.data[0].is_sent}")
```

### Create a Poll

```python
from twitch_sdk import TwitchSDK
from twitch_sdk.schemas.polls import CreatePollRequest, PollChoiceInput

async def main():
    async with TwitchSDK() as sdk:
        params = CreatePollRequest(
            broadcaster_id="123456",
            title="Favorite game?",
            choices=[
                PollChoiceInput(title="Option A"),
                PollChoiceInput(title="Option B"),
            ],
            duration=60,
        )
        poll = await sdk.polls.create_poll(sdk.http, params)
        print(f"Poll created: {poll.data[0].id}")
```

### EventSub WebSocket

```python
from twitch_sdk import TwitchSDK

async def main():
    async with TwitchSDK() as sdk:
        async with sdk.create_eventsub_websocket() as ws:
            # Subscribe to chat messages
            await ws.subscribe(
                event_type="channel.chat.message",
                version="1",
                condition={
                    "broadcaster_user_id": "123456",
                    "user_id": "123456"
                }
            )

            # Process events
            async for event in ws.events():
                print(f"Event: {event}")
```

## Endpoints

The SDK covers all Twitch Helix API endpoints:

- **Ads**: start_commercial, get_ad_schedule, snooze_next_ad
- **Analytics**: get_extension_analytics, get_game_analytics
- **Bits**: get_bits_leaderboard, get_cheermotes
- **Channel Points**: custom rewards, redemptions
- **Channels**: get/modify channel info, followers, VIPs
- **Charity**: campaigns, donations
- **Chat**: messages, emotes, badges, settings, shoutouts
- **Clips**: create_clip, get_clips
- **EventSub**: subscriptions, WebSocket, conduits
- **Games**: get_games, get_top_games
- **Goals**: creator goals
- **Guest Star**: sessions, invites, slots
- **Hype Train**: events
- **Moderation**: bans, blocked terms, AutoMod, moderators
- **Polls**: create, get, end
- **Predictions**: create, get, end
- **Raids**: start, cancel
- **Schedule**: segments, iCalendar
- **Search**: categories, channels
- **Streams**: get_streams, markers, stream key
- **Subscriptions**: broadcaster subscriptions
- **Teams**: get teams
- **Users**: get/update users, blocks, extensions
- **Videos**: get, delete
- **Whispers**: send whisper

## Pydantic Validation

All requests and responses use Pydantic models for validation:

```python
from twitch_sdk.schemas.chat import SendMessageRequest

# Validation happens automatically
params = SendMessageRequest(
    broadcaster_id="123",
    sender_id="456",
    message="Hello!"
)

# Access validated fields
print(params.broadcaster_id)
```

## Dependencies

- twitch-client (auth layer)
- pydantic
- websockets (for EventSub)
