# Knowledge Base Setup - Comfi

## ✅ COMPLETADO

La Knowledge Base ha sido creada y configurada exitosamente para el agente Comfi.

## Recursos Creados

### 1. S3 Bucket
- **Nombre**: `comfi-knowledge-base-pragma`
- **Región**: us-east-1
- **Contenido**: FAQ_Comfama_Centro_Conocimiento.docx (37.8 KB)

### 2. IAM Role
- **Nombre**: `ComfiKnowledgeBaseRole`
- **ARN**: `arn:aws:iam::777937796305:role/ComfiKnowledgeBaseRole`
- **Permisos**: 
  - Acceso a S3 (comfi-knowledge-base-pragma)
  - Invocación de modelos Bedrock
  - Acceso a OpenSearch Serverless

### 3. OpenSearch Serverless Collection
- **Nombre**: `comfi-kb-collection`
- **ID**: `a1qucftvd7w7udgkzpji`
- **ARN**: `arn:aws:aoss:us-east-1:777937796305:collection/a1qucftvd7w7udgkzpji`
- **Endpoint**: `https://a1qucftvd7w7udgkzpji.us-east-1.aoss.amazonaws.com`
- **Tipo**: VECTORSEARCH
- **Estado**: ACTIVE

### 4. OpenSearch Index
- **Nombre**: `bedrock-knowledge-base-default-index`
- **Dimensión de vectores**: 1024
- **Método**: HNSW (Faiss)

### 5. Knowledge Base
- **ID**: `PDNW6DDDGZ`
- **Nombre**: `comfi-knowledge-base`
- **ARN**: `arn:aws:bedrock:us-east-1:777937796305:knowledge-base/PDNW6DDDGZ`
- **Modelo de embeddings**: Amazon Titan Embed Text v2
- **Estado**: ACTIVE

### 6. Data Source
- **ID**: `ELUSMDMG9H`
- **Nombre**: `comfi-faq-documents`
- **Tipo**: S3
- **Estado**: AVAILABLE

### 7. Ingestion Job
- **ID**: `8ALBVW6I0V`
- **Estado**: COMPLETE
- **Documentos indexados**: 1
- **Documentos fallidos**: 0

### 8. Agent Association
- **Agent ID**: `Z6PCEKYNPS` (centli-agentcore)
- **Knowledge Base ID**: `PDNW6DDDGZ`
- **Estado**: ENABLED
- **Agent Status**: PREPARED

## Documento Indexado

- **Archivo**: FAQ_Comfama_Centro_Conocimiento.docx
- **Tamaño**: 37.8 KB
- **Estado**: Indexado exitosamente

## Cómo Funciona

1. **Usuario hace pregunta** → Frontend envía mensaje vía WebSocket
2. **Lambda recibe mensaje** → Invoca Bedrock Agent (Z6PCEKYNPS)
3. **Bedrock Agent consulta Knowledge Base** → Busca información relevante en los FAQs
4. **Knowledge Base busca en vectores** → OpenSearch Serverless encuentra documentos similares
5. **Agent genera respuesta** → Combina información de la KB con su system prompt
6. **Lambda envía respuesta** → Streaming al frontend
7. **Frontend muestra respuesta** → Tarjeta FAQ formateada o texto

## Comandos Útiles

### Ver estado de la Knowledge Base
```bash
aws bedrock-agent get-knowledge-base --knowledge-base-id PDNW6DDDGZ --region us-east-1
```

### Ver documentos en S3
```bash
aws s3 ls s3://comfi-knowledge-base-pragma/
```

### Iniciar nueva sincronización
```bash
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id PDNW6DDDGZ \
  --data-source-id ELUSMDMG9H \
  --region us-east-1
```

### Ver estado de sincronización
```bash
aws bedrock-agent list-ingestion-jobs \
  --knowledge-base-id PDNW6DDDGZ \
  --data-source-id ELUSMDMG9H \
  --region us-east-1
```

### Agregar más documentos
```bash
# 1. Subir documento a S3
aws s3 cp nuevo-documento.pdf s3://comfi-knowledge-base-pragma/

# 2. Iniciar sincronización
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id PDNW6DDDGZ \
  --data-source-id ELUSMDMG9H \
  --region us-east-1
```

## Próximos Pasos

El agente Comfi ahora tiene acceso a la base de conocimiento con los FAQs de Comfama. Puedes:

1. ✅ Probar el agente haciendo preguntas sobre Comfama
2. ✅ Agregar más documentos al bucket S3
3. ✅ Sincronizar la Knowledge Base después de agregar documentos
4. ✅ Monitorear el uso y rendimiento

## Notas Importantes

- Los documentos deben estar en formatos soportados: PDF, TXT, MD, HTML, DOC, DOCX
- Después de agregar nuevos documentos, debes ejecutar una sincronización
- El modelo de embeddings (Titan Embed Text v2) tiene un límite de 8192 tokens por chunk
- La Knowledge Base usa chunking automático para dividir documentos grandes

## Fecha de Creación

13 de marzo de 2026
