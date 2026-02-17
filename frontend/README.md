# CENTLI Frontend - Multimodal Banking UI

Asistente bancario multimodal con soporte para voz, texto e imágenes.

## Tech Stack

- Vanilla JavaScript ES6+
- Bootstrap 5 (via CDN)
- HTML5 APIs (WebSocket, MediaRecorder, Canvas, Audio)
- S3 Static Website Hosting

## Local Development

### Option 1: File Protocol
```bash
# Open directly in browser
open frontend/index.html
```

### Option 2: Local Server
```bash
# Python 3
cd frontend
python3 -m http.server 8000

# Then open: http://localhost:8000
```

## Configuration

Edit `config.js` to change:
- WebSocket URL
- S3 bucket name
- Timeouts and limits

## Deployment

### Prerequisites
- AWS CLI configured
- S3 bucket created (centli-frontend-bucket)
- Bucket policy, CORS, and lifecycle configured

### Deploy
```bash
./commands/deploy-frontend.sh
```

### Manual S3 Configuration
```bash
# Enable static website hosting
aws s3 website s3://centli-frontend-bucket/ \
  --index-document index.html \
  --error-document index.html \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Set bucket policy
aws s3api put-bucket-policy \
  --bucket centli-frontend-bucket \
  --policy file://infrastructure/s3-bucket-policy.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Set CORS
aws s3api put-bucket-cors \
  --bucket centli-frontend-bucket \
  --cors-configuration file://infrastructure/s3-cors-config.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Set lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket centli-frontend-bucket \
  --lifecycle-configuration file://infrastructure/s3-lifecycle-policy.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

## Testing

### Manual Testing Checklist
- [ ] Page loads successfully
- [ ] Login with user ID
- [ ] WebSocket connects
- [ ] Send text message
- [ ] Receive response
- [ ] Voice recording (if supported)
- [ ] Image upload
- [ ] Transaction confirmation modal
- [ ] Product catalog display
- [ ] Logout

### Browser Testing
- Chrome/Edge (latest 2 versions) - PRIMARY
- Firefox, Safari - Best effort
- Mobile: iOS Safari 14+, Chrome Mobile

## Features

- **WebSocket Communication**: Real-time bidirectional communication
- **Voice Input**: Push-to-talk recording (30s max)
- **Voice Output**: Audio playback of responses
- **Chat Interface**: Text messaging with history (50 messages)
- **Image Upload**: Client-side compression, direct S3 upload
- **Transaction Confirmation**: Modal dialogs for confirmations
- **Product Catalog**: Display products with benefits
- **Auto-Reconnect**: 5 attempts with exponential backoff
- **Responsive Design**: Mobile-first, works on all devices

## Architecture

```
frontend/
├── index.html              # Main HTML
├── config.js               # Configuration
├── css/
│   └── custom.css          # Custom styles
└── js/
    ├── app.js              # Main application
    ├── websocket-manager.js
    ├── voice-manager.js
    ├── chat-manager.js
    ├── image-manager.js
    ├── transaction-manager.js
    ├── product-catalog-manager.js
    ├── app-state.js
    └── logger.js
```

## Troubleshooting

### WebSocket won't connect
- Check WebSocket URL in config.js
- Verify backend is running
- Check browser console for errors

### Voice not working
- Check browser supports MediaRecorder API
- Grant microphone permission
- Try Chrome/Edge (best support)

### Images won't upload
- Check file size (max 5MB)
- Check file type (JPEG, PNG only)
- Verify S3 bucket permissions

## URLs

- **Frontend**: http://centli-frontend-bucket.s3-website-us-east-1.amazonaws.com
- **WebSocket**: wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod

## License

Hackathon Demo - Internal Use Only
