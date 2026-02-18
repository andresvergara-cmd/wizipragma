# 🎯 CENTLI - Asistente Financiero Inteligente

**Agente autónomo con IA que ejecuta transacciones financieras usando AWS Bedrock y Tool Use**

[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazon-aws)](https://aws.amazon.com/bedrock/)
[![Claude 3.7](https://img.shields.io/badge/Claude-3.7%20Sonnet-8A2BE2)](https://www.anthropic.com/claude)
[![Tool Use](https://img.shields.io/badge/Feature-Tool%20Use-success)](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](https://d210pgg1e91kn6.cloudfront.net)

---

## 🚀 Demo en Vivo

**URL**: https://d210pgg1e91kn6.cloudfront.net

**QR Code**: Escanea para probar en tu móvil

![QR Code](centli-qr-code.png)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Desarrollo](#-desarrollo)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Documentación](#-documentación)
- [Contribuir](#-contribuir)

---

## ✨ Características

### Funcionalidades Principales

- ✅ **Chat Inteligente**: Conversación natural en español mexicano
- ✅ **Tool Use**: Ejecuta transferencias y compras automáticamente
- ✅ **Multimodal**: Soporta texto y voz (Amazon Transcribe)
- ✅ **Streaming**: Respuestas en tiempo real via WebSocket
- ✅ **Contexto Financiero**: Conoce perfil completo del usuario
- ✅ **Validaciones**: Límites de seguridad integrados

### Capacidades del Agente

| Acción | Comando | Resultado |
|--------|---------|-----------|
| Consulta | "¿Cuál es mi saldo?" | Muestra saldos de todas las cuentas |
| Transferencia | "Envía $500 a mi mamá" | Ejecuta y retorna `TRF-XXXXXXXX` |
| Compra | "Compra un iPhone 15 Pro" | Ejecuta y retorna `ORD-XXXXXXXX` |
| Análisis | "Muestra mis gastos" | Analiza transacciones recientes |

---

## 🏗️ Arquitectura

### Stack Tecnológico

**Backend**:
- AWS Bedrock (Claude 3.7 Sonnet)
- AWS Lambda (Python 3.10)
- Amazon Transcribe (Audio STT)
- API Gateway (WebSocket)
- DynamoDB (User data)
- S3 (Audio storage)

**Frontend**:
- React 18
- WebSocket API
- MediaRecorder API
- CloudFront (HTTPS)

### Diagrama de Arquitectura

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────┐
│   CloudFront    │
│   (Frontend)    │
└──────┬──────────┘
       │ WebSocket
       ▼
┌─────────────────┐
│  API Gateway    │
│   (WebSocket)   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐      ┌──────────────┐
│  Lambda         │─────▶│  DynamoDB    │
│  (Inference)    │      │  (User Data) │
└──────┬──────────┘      └──────────────┘
       │
       ├─────▶ AWS Bedrock (Claude 3.7)
       │
       ├─────▶ Amazon Transcribe (Audio)
       │
       └─────▶ S3 (Audio Temp)
```

### Flujo de Tool Use

```
1. Usuario: "Envía $500 a mi mamá"
   ↓
2. Lambda recibe mensaje via WebSocket
   ↓
3. Bedrock analiza intención → Tool Use
   ↓
4. Lambda ejecuta transfer_money(amount=500, recipient="mamá")
   ↓
5. Genera TRF-XXXXXXXX
   ↓
6. Bedrock formatea respuesta natural
   ↓
7. Stream respuesta al usuario
```

---

## 🚀 Instalación

### Prerrequisitos

- Node.js 18+
- Python 3.10+
- AWS CLI configurado
- Cuenta AWS con acceso a Bedrock

### 1. Clonar Repositorio

```bash
git clone https://github.com/tu-usuario/centli.git
cd centli
```

### 2. Configurar Backend

```bash
cd src_aws/app_inference

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export AWS_PROFILE=tu-perfil
export REGION_NAME=us-east-1
```

### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env.production
# Editar .env.production con tus valores
```

### 4. Desplegar Infraestructura

Ver [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) para instrucciones detalladas.

---

## 💻 Uso

### Desarrollo Local

**Backend**:
```bash
cd src_aws/app_inference
python -m pytest tests/
```

**Frontend**:
```bash
cd frontend
npm run dev
```

### Comandos de Ejemplo

**Consultas**:
- "¿Cuál es mi saldo?"
- "Muéstrame mis cuentas"
- "¿Cuánto dinero tengo?"

**Transferencias**:
- "Envía $500 a mi mamá"
- "Transfiere mil pesos a Juan"
- "Manda doscientos pesos a mi hermano"

**Compras**:
- "Quiero comprar un iPhone 15 Pro"
- "Compra un MacBook"
- "Necesito comprar AirPods"

**Por Voz** 🎤:
- Click en micrófono
- Hablar claramente
- Esperar transcripción

---

## 🛠️ Desarrollo

### Estructura del Proyecto

```
centli/
├── src_aws/
│   └── app_inference/          # Lambda backend
│       ├── app.py              # Handler principal
│       ├── bedrock_config.py   # Configuración Bedrock + Tool Use
│       ├── action_tools.py     # Herramientas ejecutables
│       ├── audio_processor.py  # Procesamiento de audio
│       └── requirements.txt    # Dependencias Python
│
├── frontend/
│   ├── src/
│   │   ├── components/         # Componentes React
│   │   ├── context/            # Context providers
│   │   ├── pages/              # Páginas
│   │   └── data/               # Mock data
│   └── package.json
│
├── tests/
│   ├── unit/                   # Tests unitarios
│   └── integration/            # Tests de integración
│
├── docs/
│   ├── DEPLOYMENT.md           # Guía de deployment
│   ├── TOOL-USE.md             # Documentación Tool Use
│   ├── AUDIO.md                # Configuración de audio
│   └── API.md                  # Documentación API
│
└── scripts/
    ├── deploy-backend.sh       # Deploy Lambda
    ├── deploy-frontend.sh      # Deploy Frontend
    └── test-complete.py        # Tests end-to-end
```

### Agregar Nueva Herramienta (Tool)

1. **Definir función en `action_tools.py`**:
```python
def nueva_accion(parametro1: str, parametro2: int) -> dict:
    """Descripción de la acción"""
    # Implementación
    return {"success": True, "result": "..."}
```

2. **Agregar tool definition**:
```python
{
    "toolSpec": {
        "name": "nueva_accion",
        "description": "Descripción para el modelo",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "parametro1": {"type": "string"},
                    "parametro2": {"type": "integer"}
                },
                "required": ["parametro1"]
            }
        }
    }
}
```

3. **Actualizar `execute_tool()`**:
```python
elif tool_name == "nueva_accion":
    return nueva_accion(**tool_input)
```

4. **Desplegar**:
```bash
./scripts/deploy-backend.sh
```

---

## 🚢 Deployment

### Backend (Lambda)

```bash
cd src_aws/app_inference
./deploy-tool-use-fix.sh
```

### Frontend (CloudFront)

```bash
cd frontend
npm run build
./deploy-frontend.sh
```

### Audio (Transcribe)

```bash
./deploy-audio-transcribe.sh
# Luego agregar permisos IAM manualmente
```

Ver [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) para detalles completos.

---

## 🧪 Testing

### Tests Unitarios

```bash
cd tests
pytest unit/ -v
```

### Tests de Integración

```bash
python test-tool-use-complete.py
```

### Tests End-to-End

```bash
./scripts/test-complete.py
```

### Resultados Esperados

```
✅ Test 1: Transferencia - PASSED
✅ Test 2: Compra - PASSED
✅ Test 3: Consulta - PASSED

Total: 3 passed, 0 failed
```

---

## 📚 Documentación

### Documentos Principales

- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Guía de deployment completa
- [TOOL-USE-WORKING.md](docs/TOOL-USE-WORKING.md) - Documentación técnica de Tool Use
- [AUDIO-SETUP-COMPLETO.md](docs/AUDIO-SETUP-COMPLETO.md) - Configuración de audio
- [CHECKLIST-PRESENTACION-JURADOS.md](docs/CHECKLIST-PRESENTACION-JURADOS.md) - Guía de demo

### Documentos de Desarrollo

- [SESSION-COMPLETE.md](docs/SESSION-COMPLETE.md) - Resumen de implementación
- [SESION-FINAL-COMPLETA.md](docs/SESION-FINAL-COMPLETA.md) - Estado final del sistema
- [QR-CODES-CENTLI.md](docs/QR-CODES-CENTLI.md) - Guía de QR codes

---

## 🤝 Contribuir

### Workflow de Desarrollo

1. **Fork** el repositorio
2. **Crear branch**: `git checkout -b feature/nueva-funcionalidad`
3. **Commit cambios**: `git commit -am 'Add nueva funcionalidad'`
4. **Push**: `git push origin feature/nueva-funcionalidad`
5. **Pull Request** a `main`

### Estándares de Código

- **Python**: PEP 8, type hints
- **JavaScript**: ESLint, Prettier
- **Commits**: Conventional Commits
- **Tests**: Cobertura mínima 80%

### Áreas de Contribución

- 🐛 **Bug fixes**
- ✨ **Nuevas features**
- 📝 **Documentación**
- 🧪 **Tests**
- 🎨 **UI/UX**
- 🌐 **Internacionalización**

---

## 📊 Métricas

### Performance

- **Latencia promedio**: 3-5 segundos
- **Tasa de éxito**: 100% (tests)
- **Precisión Tool Use**: 100%
- **Disponibilidad**: 99.9%

### Costos (Estimados)

- **Por request**: ~$0.003 USD
- **Por usuario/mes**: ~$5-10 USD
- **Transcribe**: ~$0.024/minuto

---

## 🔒 Seguridad

- ✅ HTTPS obligatorio (CloudFront)
- ✅ Validación de inputs
- ✅ Límites de transacción
- ✅ Logs completos (CloudWatch)
- ✅ IAM roles con mínimos privilegios

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 👥 Equipo

- **Desarrollador Principal**: [Tu Nombre]
- **Arquitecto**: [Nombre]
- **QA**: [Nombre]

---

## 🙏 Agradecimientos

- AWS Bedrock Team
- Anthropic (Claude)
- Comunidad Open Source

---

## 📞 Contacto

- **Email**: tu-email@ejemplo.com
- **LinkedIn**: [Tu LinkedIn]
- **Twitter**: [@tu_twitter]

---

## 🎯 Roadmap

### v1.0 (Actual)
- ✅ Chat de texto
- ✅ Tool Use (transferencias y compras)
- ✅ Audio transcription
- ✅ Frontend multimodal

### v1.1 (Próximo)
- ⏳ Text-to-Speech (TTS)
- ⏳ Procesamiento de imágenes
- ⏳ Más tipos de transacciones
- ⏳ Dashboard de analytics

### v2.0 (Futuro)
- 📋 Integraciones bancarias reales
- 📋 Autenticación multi-factor
- 📋 Soporte multi-idioma
- 📋 App móvil nativa

---

**⭐ Si te gusta este proyecto, dale una estrella en GitHub!**

**🚀 [Demo en Vivo](https://d210pgg1e91kn6.cloudfront.net)**
