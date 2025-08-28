# Channel Message Recorder

A flexible Python script to record messages from various chat platforms (Discord, Slack, IRC) and save them to files in multiple formats.

## Features

- **Multi-platform support**: Discord, Slack, IRC, and demo mode
- **Multiple output formats**: JSON, CSV, Markdown, Plain Text
- **Real-time recording**: Live message capture with timestamps
- **Flexible configuration**: Command-line arguments and config files
- **Message metadata**: Captures user info, timestamps, and platform-specific data

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up platform-specific tokens/credentials (see Configuration section)

## Quick Start

### Demo Mode (No setup required)
```bash
# Generate sample messages in JSON format
python3 channel_recorder.py --platform demo --format json

# Generate sample messages in Markdown format
python3 channel_recorder.py --platform demo --format markdown --output my_chat.md
```

### Discord Recording
```bash
# Record last 100 messages from a Discord channel
python3 channel_recorder.py --platform discord --token YOUR_BOT_TOKEN --channel CHANNEL_ID --limit 100 --format json
```

### Slack Recording
```bash
# Record messages from a Slack channel
python3 channel_recorder.py --platform slack --token YOUR_BOT_TOKEN --channel CHANNEL_ID --format markdown
```

### IRC Recording
```bash
# Record IRC messages for 30 minutes
python3 channel_recorder.py --platform irc --server irc.libera.chat --channel "#python" --duration 30 --format txt
```

## Configuration

### Discord Setup
1. Create a Discord bot at https://discord.com/developers/applications
2. Get the bot token
3. Invite the bot to your server with message reading permissions

### Slack Setup
1. Create a Slack app at https://api.slack.com/apps
2. Add bot token scopes: `channels:history`, `users:read`
3. Install the app to your workspace
4. Use the Bot User OAuth Token

### IRC Setup
- No special setup required
- The script connects as a regular IRC client

## Command Line Options

- `--platform`: Choose recording platform (discord, slack, irc, demo)
- `--token`: Bot token for Discord/Slack
- `--channel`: Channel ID or name to record from
- `--server`: IRC server address
- `--port`: IRC server port (default: 6667)
- `--duration`: Recording duration in minutes (for IRC)
- `--limit`: Maximum number of messages to fetch (for Discord/Slack)
- `--format`: Output format (json, csv, markdown, txt)
- `--output`: Custom output filename

## Output Formats

### JSON
Structured data with full message metadata:
```json
[
  {
    "timestamp": "2025-08-28T09:40:36.958315",
    "channel": "general",
    "user": "alice",
    "content": "Hello everyone!",
    "message_id": "123456789",
    "metadata": {...}
  }
]
```

### Markdown
Human-readable format organized by channel:
```markdown
## Channel: #general
**2025-08-28T09:40:36** - **alice**: Hello everyone!
```

### Plain Text
Simple log format:
```
[2025-08-28T09:40:36] #general <alice>: Hello everyone!
```

### CSV
Spreadsheet-compatible format with columns: timestamp, channel, user, content, message_id

## File Structure

```
workspace/
├── channel_recorder.py     # Main script
├── requirements.txt        # Python dependencies
├── config_example.json     # Configuration template
├── README.md              # This file
└── recorded_messages/     # Default output directory
    ├── messages_*.json    # JSON output files
    ├── messages_*.md      # Markdown output files
    └── messages_*.txt     # Text output files
```

## Usage Examples

### Record Discord channel to markdown
```bash
python3 channel_recorder.py \
  --platform discord \
  --token "YOUR_DISCORD_BOT_TOKEN" \
  --channel "123456789012345678" \
  --format markdown \
  --limit 50 \
  --output "discord_general.md"
```

### Record Slack channel to CSV
```bash
python3 channel_recorder.py \
  --platform slack \
  --token "xoxb-your-slack-bot-token" \
  --channel "C1234567890" \
  --format csv \
  --output "slack_team.csv"
```

### Record IRC channel for 2 hours
```bash
python3 channel_recorder.py \
  --platform irc \
  --server "irc.libera.chat" \
  --channel "#python" \
  --duration 120 \
  --format txt \
  --output "irc_python.txt"
```

## Security Notes

- Keep bot tokens secure and never commit them to version control
- Use environment variables or config files for sensitive data
- Respect platform rate limits and terms of service
- Only record channels you have permission to access

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Run `pip install -r requirements.txt`
2. **Discord permission errors**: Ensure bot has "Read Message History" permission
3. **Slack token errors**: Verify token scopes include `channels:history` and `users:read`
4. **IRC connection issues**: Check server address and port, some servers require SSL

### Error Messages
- "Channel not found": Verify channel ID/name is correct
- "Unauthorized": Check bot permissions and token validity
- "Rate limited": Wait and retry, or reduce message limit

## Contributing

Feel free to extend this script with additional platforms or output formats. The modular design makes it easy to add new recorders by inheriting from the `MessageRecorder` base class.