#!/usr/bin/env python3
"""Check CloudWatch logs for recent voice processing"""
import boto3
import time
import sys

logs = boto3.client('logs', region_name='us-east-1')

minutes = int(sys.argv[1]) if len(sys.argv) > 1 else 10
start_time = int((time.time() - minutes * 60) * 1000)
search = sys.argv[2] if len(sys.argv) > 2 else None

print(f"=== Lambda logs (last {minutes} min) ===\n")

streams_resp = logs.describe_log_streams(
    logGroupName='/aws/lambda/centli-app-message',
    orderBy='LastEventTime',
    descending=True,
    limit=10
)

for stream in streams_resp.get('logStreams', []):
    stream_name = stream['logStreamName']
    last_event = stream.get('lastEventTimestamp', 0)
    
    if last_event < start_time:
        continue
    
    events_resp = logs.get_log_events(
        logGroupName='/aws/lambda/centli-app-message',
        logStreamName=stream_name,
        startTime=start_time,
        startFromHead=True
    )
    
    for event in events_resp.get('events', []):
        msg = event['message'].strip()
        if not msg or msg.startswith('INIT_START') or msg.startswith('END ') or msg.startswith('REPORT '):
            continue
        if search:
            if search.lower() in msg.lower():
                print(msg[:500])
        else:
            # Show AUDIO/VOICE related
            if any(k in msg for k in ['AUDIO', 'VOICE', 'audio', 'voice', 'TRANSCRI', 'Transcri', 
                                       'ffmpeg', 'WAV', 'STT', 'entender', 'PROCESS_VOICE',
                                       'Message type', 'Content length', 'blob']):
                print(msg[:500])
                print()
