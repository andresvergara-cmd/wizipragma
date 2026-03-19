# Organización del Repositorio - Comfi

## Estructura

```
comfi/
├── src_aws/                        # Backend (Lambdas)
│   ├── app_message/                # Lambda principal (producción)
│   │   ├── app_message.py          # Handler: TEXT, AUDIO
│   │   ├── transcribe_stt.py       # Transcribe Streaming STT
│   │   ├── polly_tts.py            # Polly Neural TTS
│   │   └── amazon_transcribe/      # SDK Transcribe Streaming
│   ├── app_connect/                # Lambda $connect
│   ├── app_disconnect/             # Lambda $disconnect
│   ├── app_inference/              # ⚠️ LEGACY - No usar en producción
│   ├── core_banking_*/             # Action Groups mock (banking)
│   ├── crm_*/                      # Action Groups mock (CRM)
│   ├── marketplace_*/              # Action Groups mock (marketplace)
│   └── utils/                      # Utilidades compartidas
│
├── frontend/                       # React 18 + Vite
│   ├── src/
│   │   ├── components/             # Chat, FAQ, Layout, Logo, Product
│   │   ├── context/                # WebSocket, Chat providers
│   │   ├── pages/                  # Home, Marketplace, ProductDetail, Transactions
│   │   └── data/                   # FAQ data, mock products
│   └── .env.production
│
├── tests/                          # Tests unitarios
│   └── unit/                       # test_app_connect, test_app_message, etc.
│
├── docs/                           # Documentación técnica
│   ├── ARQUITECTURA-COMFI.md       # Arquitectura detallada
│   ├── DEPLOYMENT.md               # Guía de despliegue
│   └── QUICK-START.md              # Guía rápida
│
├── scripts/                        # Scripts de deploy y testing
│   ├── deploy_message_lambda.sh    # Deploy Lambda app_message
│   ├── generate_faq_docx.py        # Generar FAQ para Knowledge Base
│   ├── test_voice_complete.py      # Test E2E de voz
│   └── ...
│
├── knowledge-base-docs/            # Documentos fuente para KB
├── aidlc-docs/                     # Documentación de diseño (AI-DLC)
├── infrastructure/                 # Templates CloudFormation/SAM
│
├── README.md                       # Documentación principal
├── CONTRIBUTING.md                 # Guía de contribución
├── .gitignore                      # Archivos ignorados
└── pyproject.toml                  # Configuración Python
```

## Convenciones

- **Documentación**: `UPPERCASE-WITH-DASHES.md`
- **Scripts**: `lowercase_with_underscores.py` o `lowercase-with-dashes.sh`
- **Código Python**: `snake_case.py`
- **Código React**: `PascalCase.jsx`
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`)
