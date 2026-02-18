# Permisos IAM Necesarios para Audio Transcription

## Problema
El Lambda necesita permisos adicionales para:
1. Amazon Transcribe (transcribir audio)
2. S3 (almacenar audio temporalmente)

## Solución Manual

### Opción 1: Agregar Política Inline al Role del Lambda

1. **Ir a IAM Console**: https://console.aws.amazon.com/iam/
2. **Buscar el role**: `poc-wizi-mex-stack-InferenceAPIFnRole-gNaIeNvDMIxD`
3. **Agregar política inline** con este JSON:

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

4. **Nombre de la política**: `AudioTranscriptionPolicy`
5. **Guardar**

### Opción 2: Usar AWS CLI con Credenciales de Admin

```bash
# Configurar perfil de admin temporalmente
aws configure --profile admin

# Agregar política
aws iam put-role-policy \
    --role-name poc-wizi-mex-stack-InferenceAPIFnRole-gNaIeNvDMIxD \
    --policy-name AudioTranscriptionPolicy \
    --policy-document file://audio-iam-policy.json \
    --profile admin
```

Donde `audio-iam-policy.json` contiene el JSON de arriba.

### Opción 3: Modificar CloudFormation Stack

Si el Lambda fue creado con CloudFormation, agregar estos permisos al template:

```yaml
InferenceAPIFnRole:
  Type: AWS::IAM::Role
  Properties:
    Policies:
      - PolicyName: AudioTranscriptionPolicy
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - transcribe:StartTranscriptionJob
                - transcribe:GetTranscriptionJob
                - transcribe:DeleteTranscriptionJob
              Resource: '*'
            - Effect: Allow
              Action:
                - s3:PutObject
                - s3:GetObject
                - s3:DeleteObject
              Resource: arn:aws:s3:::poc-wizi-mex-audio-temp/*
            - Effect: Allow
              Action:
                - s3:ListBucket
              Resource: arn:aws:s3:::poc-wizi-mex-audio-temp
```

## Verificación

Después de agregar los permisos, verifica que funcionen:

```bash
# Verificar permisos del role
aws iam get-role-policy \
    --role-name poc-wizi-mex-stack-InferenceAPIFnRole-gNaIeNvDMIxD \
    --policy-name AudioTranscriptionPolicy \
    --profile pragma-power-user
```

## Recursos Creados

- ✅ **S3 Bucket**: `poc-wizi-mex-audio-temp`
  - Lifecycle: Archivos se borran después de 1 día
  - Ubicación: us-east-1

- ✅ **Lambda**: Código actualizado con Amazon Transcribe
  - Función: `poc-wizi-mex-lambda-inference-model-dev`
  - Última actualización: 2026-02-17T22:07:59.000+0000

## Próximos Pasos

1. **Agregar permisos IAM** (una de las 3 opciones arriba)
2. **Probar audio** en https://d210pgg1e91kn6.cloudfront.net
3. **Verificar logs** si hay errores

## Comandos Útiles

```bash
# Ver logs en tiempo real
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev --follow --profile pragma-power-user

# Listar archivos en S3
aws s3 ls s3://poc-wizi-mex-audio-temp/audio-input/ --profile pragma-power-user

# Ver trabajos de transcripción
aws transcribe list-transcription-jobs --profile pragma-power-user
```
