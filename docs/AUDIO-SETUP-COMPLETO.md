# 🎤 Setup Completo de Audio - CENTLI

**Fecha**: 2026-02-17
**Status**: ✅ CÓDIGO DESPLEGADO - ⏳ PERMISOS PENDIENTES

## ✅ Lo que YA está hecho

1. **Código actualizado** ✅
   - `audio_processor.py` usa Amazon Transcribe
   - Lambda desplegado con nuevo código
   - S3 bucket creado: `poc-wizi-mex-audio-temp`

2. **Frontend funcionando** ✅
   - Grabación de audio funciona
   - Envío de audio via WebSocket funciona
   - Lambda recibe el audio correctamente

## ⏳ Lo que FALTA (5 minutos)

**Solo falta agregar permisos IAM al Lambda**

### Opción 1: Consola de AWS (MÁS FÁCIL) - 3 minutos

1. **Ir a IAM Console**: https://console.aws.amazon.com/iam/home?region=us-east-1#/roles

2. **Buscar el role**: `poc-wizi-mex-stack-InferenceAPIFnRole-gNaIeNvDMIxD`

3. **Click en el role** → Pestaña "Permissions"

4. **Click "Add permissions"** → "Create inline policy"

5. **Click en "JSON"** y pegar esto:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob",
        "transcribe:DeleteTranscriptionJob"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::poc-wizi-mex-audio-temp/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::poc-wizi-mex-audio-temp"
    }
  ]
}
```

6. **Click "Review policy"**

7. **Nombre**: `AudioTranscriptionPolicy`

8. **Click "Create policy"**

9. **¡Listo!** 🎉

### Opción 2: AWS CLI (si tienes credenciales de admin)

```bash
./add-audio-permissions.sh
```

O manualmente:

```bash
aws iam put-role-policy \
    --role-name poc-wizi-mex-stack-InferenceAPIFnRole-gNaIeNvDMIxD \
    --policy-name AudioTranscriptionPolicy \
    --policy-document file://audio-iam-policy.json \
    --profile [TU-PERFIL-ADMIN]
```

## 🧪 Cómo Probar

### Paso 1: Verificar Permisos Agregados

```bash
aws iam get-role-policy \
    --role-name poc-wizi-mex-stack-InferenceAPIFnRole-gNaIeNvDMIxD \
    --policy-name AudioTranscriptionPolicy \
    --profile pragma-power-user
```

Si devuelve la política, ¡está listo!

### Paso 2: Abrir Frontend

```bash
open https://d210pgg1e91kn6.cloudfront.net
```

### Paso 3: Hard Refresh

- Mac: `Cmd + Shift + R`
- Windows: `Ctrl + Shift + R`

### Paso 4: Grabar Audio

1. Click en el chat widget (esquina inferior derecha)
2. Click en el ícono del micrófono 🎤
3. Permitir acceso al micrófono (si pregunta)
4. Hablar claramente: **"Envía quinientos pesos a mi mamá"**
5. Click en "Enviar"

### Paso 5: Ver Resultado

Deberías ver:
```
✅ Listo Carlos! Transferí $500 MXN a tu mamá.

Detalles de la transacción:
- ID: TRF-XXXXXXXX
- Monto: $500.00 MXN
- Destinatario: mamá

Tu nuevo saldo: $99,500.00 MXN
```

## 📊 Monitoreo

### Ver Logs en Tiempo Real

```bash
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev --follow --profile pragma-power-user
```

Busca estas líneas:
```
Processing AUDIO message
Audio decoded: XXXX bytes
Uploading audio to S3: s3://poc-wizi-mex-audio-temp/audio-input/...
Starting transcription job: audio-transcribe-...
Transcription status: IN_PROGRESS
Transcription status: COMPLETED
Transcribed text: 'envía quinientos pesos a mi mamá'
```

### Ver Trabajos de Transcripción

```bash
aws transcribe list-transcription-jobs --profile pragma-power-user
```

### Ver Archivos en S3

```bash
aws s3 ls s3://poc-wizi-mex-audio-temp/audio-input/ --profile pragma-power-user
```

## 🎯 Mensajes de Voz para Probar

### Transferencia
```
"Envía quinientos pesos a mi mamá"
"Transfiere mil pesos a Juan"
"Manda doscientos pesos a mi hermano"
```

### Compra
```
"Quiero comprar un iPhone quince Pro"
"Compra un MacBook"
"Necesito comprar AirPods"
```

### Consulta
```
"¿Cuál es mi saldo?"
"Muéstrame mis cuentas"
"¿Cuánto dinero tengo?"
```

## ⚠️ Troubleshooting

### Problema: "Lo siento, hubo un error procesando tu mensaje de voz"

**Causa**: Permisos IAM no agregados

**Solución**: Agregar permisos (ver Opción 1 arriba)

### Problema: "Lo siento, no pude entender el audio"

**Causa**: Audio muy corto o sin voz

**Solución**: Hablar más claro y más tiempo (mínimo 2 segundos)

### Problema: Transcripción incorrecta

**Causa**: Audio con ruido o pronunciación poco clara

**Solución**: 
- Hablar más despacio
- Ambiente silencioso
- Micrófono cerca de la boca

### Problema: Timeout

**Causa**: Transcripción toma más de 30 segundos

**Solución**: Audio muy largo, grabar mensajes más cortos (<10 segundos)

## 📈 Latencia Esperada

- **Grabación**: Instantánea
- **Upload a S3**: ~500ms
- **Transcripción**: 2-5 segundos
- **Respuesta del agente**: 3-4 segundos
- **Total**: 6-10 segundos

## 💰 Costos

### Amazon Transcribe
- **Precio**: $0.024 por minuto de audio
- **Ejemplo**: 100 mensajes de 5 segundos = 8.3 minutos = $0.20

### S3
- **Storage**: Gratis (archivos se borran después de 1 día)
- **Requests**: ~$0.0004 por 1000 requests

**Total estimado para demo**: < $1 USD

## 🎬 Para la Demo

### Flujo 1: Transferencia con Voz
```
1. Click en micrófono 🎤
2. Decir: "Envía quinientos pesos a mi mamá"
3. Esperar transcripción (2-3 seg)
4. Ver respuesta con TRF-XXXXXXXX
```

### Flujo 2: Compra con Voz
```
1. Click en micrófono 🎤
2. Decir: "Quiero comprar un iPhone quince Pro"
3. Esperar transcripción (2-3 seg)
4. Ver respuesta con ORD-XXXXXXXX
```

## ✅ Checklist Final

```
[ ] Permisos IAM agregados
[ ] Frontend abierto con hard refresh
[ ] Micrófono funcionando
[ ] Audio grabado y enviado
[ ] Logs muestran transcripción exitosa
[ ] Agente responde correctamente
[ ] Tool Use ejecuta transferencia/compra
[ ] Transaction ID visible en respuesta
```

## 🚀 Próximos Pasos

Una vez que agregues los permisos IAM:

1. **Probar audio** con los mensajes de ejemplo
2. **Verificar logs** para confirmar transcripción
3. **Grabar demo** con voz y texto
4. **Celebrar** 🎉

---

**Resumen**: Solo falta agregar los permisos IAM (3 minutos en consola) y el audio funcionará completamente con Tool Use!
