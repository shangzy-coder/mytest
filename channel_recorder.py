#!/usr/bin/env python3
"""
Channel Message Recorder

A flexible script to record messages from various channel types (Discord, Slack, IRC, etc.)
and save them to files with different output formats.
"""

import asyncio
import json
import csv
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ChannelMessage:
    """Represents a channel message with metadata"""
    timestamp: str
    channel: str
    user: str
    content: str
    message_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MessageRecorder:
    """Records channel messages to various file formats"""
    
    def __init__(self, output_dir: str = "recorded_messages"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.messages: List[ChannelMessage] = []
    
    def add_message(self, message: ChannelMessage):
        """Add a message to the recording buffer"""
        self.messages.append(message)
        print(f"[{message.timestamp}] #{message.channel} <{message.user}>: {message.content}")
    
    def save_to_json(self, filename: Optional[str] = None) -> str:
        """Save messages to JSON format"""
        if not filename:
            filename = f"messages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump([asdict(msg) for msg in self.messages], f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.messages)} messages to {filepath}")
        return str(filepath)
    
    def save_to_csv(self, filename: Optional[str] = None) -> str:
        """Save messages to CSV format"""
        if not filename:
            filename = f"messages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if self.messages:
                writer = csv.DictWriter(f, fieldnames=['timestamp', 'channel', 'user', 'content', 'message_id'])
                writer.writeheader()
                for msg in self.messages:
                    row = asdict(msg)
                    # Convert metadata to string for CSV
                    if row.get('metadata'):
                        row['metadata'] = json.dumps(row['metadata'])
                    writer.writerow({k: v for k, v in row.items() if k != 'metadata'})
        
        print(f"Saved {len(self.messages)} messages to {filepath}")
        return str(filepath)
    
    def save_to_markdown(self, filename: Optional[str] = None) -> str:
        """Save messages to Markdown format"""
        if not filename:
            filename = f"messages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Channel Messages Record\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Messages**: {len(self.messages)}\n\n")
            f.write("---\n\n")
            
            current_channel = None
            for msg in self.messages:
                if msg.channel != current_channel:
                    current_channel = msg.channel
                    f.write(f"## Channel: #{msg.channel}\n\n")
                
                f.write(f"**{msg.timestamp}** - **{msg.user}**: {msg.content}\n\n")
        
        print(f"Saved {len(self.messages)} messages to {filepath}")
        return str(filepath)
    
    def save_to_txt(self, filename: Optional[str] = None) -> str:
        """Save messages to plain text format"""
        if not filename:
            filename = f"messages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Channel Messages Record - Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            
            for msg in self.messages:
                f.write(f"[{msg.timestamp}] #{msg.channel} <{msg.user}>: {msg.content}\n")
        
        print(f"Saved {len(self.messages)} messages to {filepath}")
        return str(filepath)
    
    def clear_messages(self):
        """Clear the message buffer"""
        self.messages.clear()
        print("Message buffer cleared")

# Example implementations for different platforms

class DiscordRecorder(MessageRecorder):
    """Discord-specific message recorder"""
    
    def __init__(self, token: str, output_dir: str = "discord_messages"):
        super().__init__(output_dir)
        self.token = token
    
    async def record_channel(self, channel_id: str, limit: Optional[int] = None):
        """Record messages from a Discord channel (requires discord.py)"""
        try:
            import discord
        except ImportError:
            print("Error: discord.py not installed. Run: pip install discord.py")
            return
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(f"Connected as {client.user}")
            channel = client.get_channel(int(channel_id))
            if not channel:
                print(f"Channel {channel_id} not found")
                await client.close()
                return
            
            print(f"Recording messages from #{channel.name}...")
            
            async for message in channel.history(limit=limit):
                msg = ChannelMessage(
                    timestamp=message.created_at.isoformat(),
                    channel=channel.name,
                    user=str(message.author),
                    content=message.content,
                    message_id=str(message.id),
                    metadata={
                        "attachments": [att.url for att in message.attachments],
                        "reactions": [str(reaction.emoji) for reaction in message.reactions]
                    }
                )
                self.add_message(msg)
            
            await client.close()
        
        await client.start(self.token)

class SlackRecorder(MessageRecorder):
    """Slack-specific message recorder"""
    
    def __init__(self, token: str, output_dir: str = "slack_messages"):
        super().__init__(output_dir)
        self.token = token
    
    async def record_channel(self, channel_id: str, limit: Optional[int] = None):
        """Record messages from a Slack channel (requires slack-sdk)"""
        try:
            from slack_sdk.web.async_client import AsyncWebClient
        except ImportError:
            print("Error: slack-sdk not installed. Run: pip install slack-sdk")
            return
        
        client = AsyncWebClient(token=self.token)
        
        try:
            # Get channel info
            channel_info = await client.conversations_info(channel=channel_id)
            channel_name = channel_info["channel"]["name"]
            
            print(f"Recording messages from #{channel_name}...")
            
            # Get messages
            response = await client.conversations_history(
                channel=channel_id,
                limit=limit or 100
            )
            
            for message in reversed(response["messages"]):
                if message.get("type") == "message" and not message.get("subtype"):
                    # Get user info
                    user_info = await client.users_info(user=message["user"])
                    username = user_info["user"]["real_name"] or user_info["user"]["name"]
                    
                    msg = ChannelMessage(
                        timestamp=datetime.fromtimestamp(float(message["ts"])).isoformat(),
                        channel=channel_name,
                        user=username,
                        content=message["text"],
                        message_id=message["ts"],
                        metadata={
                            "user_id": message["user"],
                            "thread_ts": message.get("thread_ts")
                        }
                    )
                    self.add_message(msg)
        
        except Exception as e:
            print(f"Error recording Slack messages: {e}")

class IRCRecorder(MessageRecorder):
    """IRC-specific message recorder"""
    
    def __init__(self, server: str, port: int = 6667, output_dir: str = "irc_messages"):
        super().__init__(output_dir)
        self.server = server
        self.port = port
        self.nickname = "recorder_bot"
        self.channels_to_record: List[str] = []
    
    async def record_channel(self, channel: str, duration_minutes: int = 60):
        """Record messages from an IRC channel for a specified duration"""
        try:
            import asyncio
            import socket
        except ImportError:
            print("Error: Required modules not available")
            return
        
        print(f"Connecting to {self.server}:{self.port}...")
        
        reader, writer = await asyncio.open_connection(self.server, self.port)
        
        # IRC handshake
        writer.write(f"NICK {self.nickname}\r\n".encode())
        writer.write(f"USER {self.nickname} 0 * :{self.nickname}\r\n".encode())
        await writer.drain()
        
        # Join channel
        writer.write(f"JOIN {channel}\r\n".encode())
        await writer.drain()
        
        print(f"Joined {channel}, recording for {duration_minutes} minutes...")
        
        end_time = datetime.now().timestamp() + (duration_minutes * 60)
        
        try:
            while datetime.now().timestamp() < end_time:
                data = await asyncio.wait_for(reader.readline(), timeout=1.0)
                line = data.decode('utf-8', errors='ignore').strip()
                
                if line.startswith('PING'):
                    writer.write(f"PONG {line.split()[1]}\r\n".encode())
                    await writer.drain()
                    continue
                
                # Parse PRIVMSG
                if 'PRIVMSG' in line and channel in line:
                    parts = line.split(' ', 3)
                    if len(parts) >= 4:
                        user = parts[0].split('!')[0][1:]  # Remove : prefix
                        content = parts[3][1:]  # Remove : prefix
                        
                        msg = ChannelMessage(
                            timestamp=datetime.now().isoformat(),
                            channel=channel[1:],  # Remove # prefix
                            user=user,
                            content=content
                        )
                        self.add_message(msg)
        
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print(f"Error during IRC recording: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

def main():
    """Main function with command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Record channel messages to file")
    parser.add_argument("--platform", choices=["discord", "slack", "irc", "demo"], 
                       default="demo", help="Platform to record from")
    parser.add_argument("--token", help="Bot token (for Discord/Slack)")
    parser.add_argument("--channel", help="Channel ID or name to record")
    parser.add_argument("--server", help="Server address (for IRC)")
    parser.add_argument("--port", type=int, default=6667, help="Server port (for IRC)")
    parser.add_argument("--duration", type=int, default=60, help="Recording duration in minutes")
    parser.add_argument("--limit", type=int, help="Message limit to fetch")
    parser.add_argument("--format", choices=["json", "csv", "markdown", "txt"], 
                       default="json", help="Output format")
    parser.add_argument("--output", help="Output filename")
    
    args = parser.parse_args()
    
    async def run_recorder():
        if args.platform == "discord":
            if not args.token or not args.channel:
                print("Error: Discord recording requires --token and --channel")
                return
            
            recorder = DiscordRecorder(args.token)
            await recorder.record_channel(args.channel, args.limit)
        
        elif args.platform == "slack":
            if not args.token or not args.channel:
                print("Error: Slack recording requires --token and --channel")
                return
            
            recorder = SlackRecorder(args.token)
            await recorder.record_channel(args.channel, args.limit)
        
        elif args.platform == "irc":
            if not args.server or not args.channel:
                print("Error: IRC recording requires --server and --channel")
                return
            
            recorder = IRCRecorder(args.server, args.port)
            await recorder.record_channel(args.channel, args.duration)
        
        else:  # demo mode
            print("Running in demo mode - generating sample messages...")
            recorder = MessageRecorder("demo_messages")
            
            # Generate some demo messages
            demo_messages = [
                ChannelMessage(
                    timestamp=datetime.now().isoformat(),
                    channel="general",
                    user="alice",
                    content="Hello everyone! How's the project going?"
                ),
                ChannelMessage(
                    timestamp=datetime.now().isoformat(),
                    channel="general", 
                    user="bob",
                    content="Great! Just finished the API integration."
                ),
                ChannelMessage(
                    timestamp=datetime.now().isoformat(),
                    channel="dev-team",
                    user="charlie",
                    content="Found a bug in the payment module, working on a fix."
                ),
                ChannelMessage(
                    timestamp=datetime.now().isoformat(),
                    channel="dev-team",
                    user="alice",
                    content="Thanks! Let me know if you need help testing it."
                )
            ]
            
            for msg in demo_messages:
                recorder.add_message(msg)
        
        # Save in requested format
        if args.format == "json":
            filepath = recorder.save_to_json(args.output)
        elif args.format == "csv":
            filepath = recorder.save_to_csv(args.output)
        elif args.format == "markdown":
            filepath = recorder.save_to_markdown(args.output)
        elif args.format == "txt":
            filepath = recorder.save_to_txt(args.output)
        
        print(f"\nRecording completed! Output saved to: {filepath}")
        print(f"Total messages recorded: {len(recorder.messages)}")
    
    # Run the async recorder
    asyncio.run(run_recorder())

if __name__ == "__main__":
    main()