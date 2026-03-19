#!/usr/bin/env python3
"""Check latest Lambda logs for voice pipeline timing."""
import boto3

logs = boto3.client('logs', region_name='us-east-1')
streams = logs.describe_log_streams(
    logGroupName='/aws/lambda/centli-app-message',
    orderBy='LastEventTime', descending=True, limit=1
)
stream = streams['logStreams'][0]['logStreamName']
print(f"Stream: {stream}")

events = logs.get_log_events(
    logGroupName='/aws/lambda/centli-app-message',
    logStreamName=stream, limit=80
)
keywords = ['STEP','STT','Streaming','Transcri','Bedrock','Polly',
            'REPORT','Duration','VOICE','time','COMPLETED','ERROR',
            'ffmpeg','WAV','PCM','Converting','Converted','Started']
for e in events['events']:
    msg = e['message'].strip()
    if any(k in msg for k in keywords):
        print(msg[:250])
