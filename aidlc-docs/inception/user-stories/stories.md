# User Stories - CENTLI Hackathon

## Organización por Stack Técnico

Las stories están organizadas para facilitar trabajo paralelo de 3 desarrolladores:
- **Dev 1**: Frontend/UI Stories
- **Dev 2**: Backend/Mocks Stories  
- **Dev 3**: AgentCore/AI Stories

Cada story incluye:
- Formato estándar: "As a [persona], I want [goal], so that [benefit]"
- Acceptance Criteria en formato Given-When-Then
- Detalles técnicos (AWS services, APIs)
- Estimación en horas
- Demo Validation
- Prioridad (Must Have / Should Have / Could Have)

---

# DEV 3: AGENTCORE/AI STORIES

## Epic 1: Bedrock AgentCore Foundation

### Story 3.1: Setup AWS Bedrock AgentCore
**Priority**: Must Have  
**Estimation**: 2 hours

**As a** sistema CENTLI  
**I want** tener AWS Bedrock AgentCore configurado y funcional  
**So that** pueda orquestar todas las capacidades agentic del sistema

**Technical Details**:
- AWS Bedrock AgentCore setup
- Agent configuration with foundation model (Claude 3.7 Sonnet)
- Managed Memory configuration (DynamoDB backend)
- IAM roles and policies for Bedrock access
- Lambda integration for orchestration

**Acceptance Criteria**:

**Given** una cuenta AWS configurada  
**When** se despliega la infraestructura de AgentCore  
**Then** el agente está activo y responde a invocaciones básicas

**Given** un mensaje de prueba  
**When** se envía al AgentCore  
**Then** el agente procesa el mensaje y retorna respuesta

**Given** múltiples invocaciones  
**When** se envían en secuencia  
**Then** Managed Memory mantiene contexto entre invocaciones

**Error Scenarios**:
- **Given** configuración inválida **When** se intenta desplegar **Then** error claro de configuración
- **Given** permisos IAM insuficientes **When** se invoca agente **Then** error de autorización

**Demo Validation**:
- [ ] AgentCore responde a mensaje "Hola CENTLI"
- [ ] Managed Memory recuerda nombre del usuario entre mensajes
- [ ] Logs de CloudWatch muestran invocaciones exitosas

**Dependencies**: None (base infrastructure)

---

### Story 3.2: Configure Action Groups
**Priority**: Must Have  
**Estimation**: 2 hours

**As a** AgentCore  
**I want** tener Action Groups configurados para Core Bancario, Marketplace y CRM  
**So that** pueda ejecutar acciones transaccionales en los mocks

**Technical Details**:
- 3 Action Groups: CoreBanking, Marketplace, CRM
- OpenAPI schemas para cada Action Group
- Lambda functions como backends de Action Groups
- Bedrock Agent permissions para invocar Lambdas
- Action Group routing configuration

**Acceptance Criteria**:

**Given** AgentCore configurado  
**When** se registran los 3 Action Groups  
**Then** AgentCore puede invocar acciones de cada grupo

**Given** un intent de transferencia  
**When** AgentCore procesa el intent  
**Then** invoca Action Group CoreBanking correctamente

**Given** un intent de compra  
**When** AgentCore procesa el intent  
**Then** invoca Action Group Marketplace correctamente

**Given** un intent de buscar beneficiario  
**When** AgentCore procesa el intent  
**Then** invoca Action Group CRM correctamente

**Error Scenarios**:
- **Given** Action Group no disponible **When** se intenta invocar **Then** error manejado gracefully
- **Given** schema inválido **When** se registra Action Group **Then** error de validación

**Demo Validation**:
- [ ] AgentCore invoca CoreBanking Action Group para consultar saldo
- [ ] AgentCore invoca Marketplace Action Group para listar productos
- [ ] AgentCore invoca CRM Action Group para buscar beneficiario
- [ ] Logs muestran invocaciones exitosas de cada Action Group

**Dependencies**: Story 3.1 (AgentCore setup)

---


### Story 3.3: Integrate Nova Sonic for Voice
**Priority**: Must Have  
**Estimation**: 2 hours

**As a** Usuario Bancario (Carlos)  
**I want** interactuar con CENTLI usando mi voz  
**So that** puedo hacer transacciones manos libres mientras hago otras actividades

**Technical Details**:
- AWS Bedrock Nova Sonic integration
- Speech-to-text (audio input → text)
- Text-to-speech (text output → audio)
- Audio streaming via WebSocket
- Spanish (Mexico) language configuration
- Real-time audio processing

**Acceptance Criteria**:

**Given** un usuario habla "Hola CENTLI"  
**When** el audio se envía al sistema  
**Then** Nova Sonic transcribe correctamente a texto

**Given** AgentCore genera respuesta en texto  
**When** se procesa para salida  
**Then** Nova Sonic convierte a audio natural en español mexicano

**Given** un comando de transferencia por voz  
**When** usuario dice "Envíale 50 lucas a mi hermano"  
**Then** sistema transcribe y extrae: monto=50000, destinatario="mi hermano"

**Given** respuesta de confirmación  
**When** sistema genera "Operación firme. 50,000 pesos enviados"  
**Then** Nova Sonic produce audio natural y expresivo

**Error Scenarios**:
- **Given** audio con ruido **When** se transcribe **Then** solicita repetir comando
- **Given** comando ambiguo **When** se procesa **Then** solicita clarificación por voz

**Demo Validation**:
- [ ] Usuario habla comando y sistema transcribe correctamente
- [ ] Sistema responde con voz natural en español mexicano
- [ ] Latencia total < 3 segundos (audio → respuesta audio)
- [ ] Voz es clara y profesional (personalidad CENTLI)

**Dependencies**: Story 3.1 (AgentCore setup)

---

### Story 3.4: Integrate Nova Canvas for Images
**Priority**: Could Have  
**Estimation**: 1.5 hours

**As a** Usuario Bancario (Carlos)  
**I want** enviar imágenes (recibos, productos) a CENTLI  
**So that** el sistema puede analizar y extraer información relevante

**Technical Details**:
- AWS Bedrock Nova Canvas integration
- Image upload via WebSocket/REST
- Image analysis and text extraction
- Object detection in images
- S3 storage for images
- Integration with AgentCore for context

**Acceptance Criteria**:

**Given** un usuario envía foto de recibo  
**When** Nova Canvas analiza la imagen  
**Then** extrae: monto, comercio, fecha, concepto

**Given** un usuario envía foto de producto  
**When** Nova Canvas analiza la imagen  
**Then** identifica producto y sugiere búsqueda en marketplace

**Given** imagen con texto  
**When** se procesa  
**Then** OCR extrae texto correctamente

**Error Scenarios**:
- **Given** imagen borrosa **When** se analiza **Then** solicita imagen más clara
- **Given** imagen sin contenido relevante **When** se procesa **Then** informa que no puede extraer información

**Demo Validation**:
- [ ] Usuario envía foto de recibo y sistema extrae datos
- [ ] Sistema usa información extraída para contexto de conversación
- [ ] Imágenes se almacenan en S3 correctamente

**Dependencies**: Story 3.1 (AgentCore setup)

---

## Epic 2: Intelligent Processing

### Story 3.5: Implement Intent Recognition
**Priority**: Must Have  
**Estimation**: 1.5 hours

**As a** AgentCore  
**I want** identificar correctamente la intención del usuario  
**So that** puedo invocar el Action Group apropiado

**Technical Details**:
- Natural Language Understanding (NLU) via Claude
- Intent classification (transfer, purchase, query, help)
- Entity extraction (amounts, beneficiaries, products)
- Context-aware intent resolution
- Ambiguity handling

**Acceptance Criteria**:

**Given** usuario dice "Envíale 50 lucas a mi hermano"  
**When** AgentCore procesa  
**Then** identifica intent=TRANSFER, monto=50000, destinatario="mi hermano"

**Given** usuario dice "Quiero comprar una laptop"  
**When** AgentCore procesa  
**Then** identifica intent=PURCHASE, producto="laptop"

**Given** usuario dice "¿Cuánto tengo?"  
**When** AgentCore procesa  
**Then** identifica intent=QUERY_BALANCE

**Given** comando ambiguo  
**When** AgentCore procesa  
**Then** solicita clarificación con opciones específicas

**Error Scenarios**:
- **Given** comando incomprensible **When** se procesa **Then** solicita reformular
- **Given** múltiples intents en un mensaje **When** se procesa **Then** maneja secuencialmente

**Demo Validation**:
- [ ] Sistema identifica correctamente intent de transferencia
- [ ] Sistema identifica correctamente intent de compra
- [ ] Sistema maneja ambigüedades pidiendo clarificación

**Dependencies**: Story 3.1 (AgentCore setup), Story 3.2 (Action Groups)

---

### Story 3.6: Implement Managed Memory
**Priority**: Should Have  
**Estimation**: 1.5 hours

**As a** Usuario Bancario (Carlos)  
**I want** que CENTLI recuerde mis beneficiarios frecuentes y preferencias  
**So that** no tengo que repetir información en cada interacción

**Technical Details**:
- Bedrock Managed Memory (DynamoDB backend)
- Session management
- User context persistence
- Frequent beneficiaries tracking
- Preference storage
- Conversation history

**Acceptance Criteria**:

**Given** usuario ha transferido a "mi hermano" antes  
**When** dice "Envíale 50 lucas a mi hermano"  
**Then** sistema resuelve automáticamente a Juan López

**Given** usuario tiene beneficiarios frecuentes  
**When** inicia transferencia  
**Then** sistema sugiere beneficiarios más usados

**Given** múltiples sesiones del mismo usuario  
**When** inicia nueva sesión  
**Then** sistema recuerda contexto de sesiones anteriores

**Given** usuario establece preferencia (ej. siempre confirmar)  
**When** hace transacciones  
**Then** sistema respeta preferencia

**Error Scenarios**:
- **Given** memoria corrupta **When** se accede **Then** inicia sesión limpia
- **Given** múltiples usuarios en mismo dispositivo **When** se accede **Then** mantiene contextos separados

**Demo Validation**:
- [ ] Sistema recuerda beneficiario "mi hermano" entre sesiones
- [ ] Sistema sugiere beneficiarios frecuentes
- [ ] Managed Memory persiste en DynamoDB

**Dependencies**: Story 3.1 (AgentCore setup)

---


# DEV 2: BACKEND/MOCKS STORIES

## Epic 3: Core Bancario Mock

### Story 2.1: Implement Core Banking Mock - Accounts
**Priority**: Must Have  
**Estimation**: 1.5 hours

**As a** sistema CENTLI  
**I want** un Core Bancario mock que gestione cuentas y saldos  
**So that** puedo simular operaciones bancarias reales

**Technical Details**:
- Lambda function: CoreBankingMock
- DynamoDB table: Accounts
- APIs: getAccount, getBalance, updateBalance
- Account schema: userId, accountNumber, balance, creditLine
- Mock data initialization
- Action Group backend implementation

**Acceptance Criteria**:

**Given** un userId válido  
**When** se consulta getAccount  
**Then** retorna datos completos de cuenta

**Given** un accountNumber  
**When** se consulta getBalance  
**Then** retorna saldo actual

**Given** una transacción exitosa  
**When** se llama updateBalance  
**Then** saldo se actualiza correctamente en DynamoDB

**Given** múltiples consultas concurrentes  
**When** se ejecutan  
**Then** datos son consistentes

**Error Scenarios**:
- **Given** userId inexistente **When** se consulta **Then** retorna error 404
- **Given** saldo insuficiente **When** se intenta debitar **Then** retorna error de fondos

**Demo Validation**:
- [ ] Consulta de saldo retorna datos correctos
- [ ] Actualización de saldo persiste en DynamoDB
- [ ] Action Group invoca Lambda correctamente

**Dependencies**: Story 3.2 (Action Groups configured)

---

### Story 2.2: Implement P2P Transfers
**Priority**: Must Have  
**Estimation**: 2 hours

**As a** Usuario Bancario (Carlos)  
**I want** ejecutar transferencias P2P a mis beneficiarios  
**So that** puedo enviar dinero de forma rápida y segura

**Technical Details**:
- Lambda function: CoreBankingMock (extend)
- API: executeTransfer
- Transaction schema: transactionId, fromAccount, toAccount, amount, concept, timestamp
- DynamoDB table: Transactions
- Atomic balance updates (debit + credit)
- Transaction validation logic

**Acceptance Criteria**:

**Given** usuario con saldo suficiente  
**When** ejecuta transferencia de 50,000 a beneficiario  
**Then** saldo origen se reduce en 50,000 y destino aumenta en 50,000

**Given** transferencia exitosa  
**When** se completa  
**Then** registro se guarda en tabla Transactions

**Given** transferencia con concepto  
**When** se ejecuta  
**Then** concepto se almacena en transacción

**Given** saldo insuficiente  
**When** se intenta transferencia  
**Then** retorna error y no modifica saldos

**Error Scenarios**:
- **Given** cuenta destino inexistente **When** se transfiere **Then** error de cuenta no encontrada
- **Given** monto negativo **When** se valida **Then** error de monto inválido
- **Given** falla en medio de transacción **When** ocurre error **Then** rollback automático

**Demo Validation**:
- [ ] Transferencia P2P actualiza ambos saldos correctamente
- [ ] Transacción se registra en DynamoDB
- [ ] Validaciones de saldo funcionan correctamente
- [ ] Errores se manejan gracefully

**Dependencies**: Story 2.1 (Core Banking Mock - Accounts)

---

### Story 2.3: Implement CRM Mock - Beneficiaries
**Priority**: Should Have  
**Estimation**: 1.5 hours

**As a** Usuario Bancario (Carlos)  
**I want** que el sistema gestione mis beneficiarios frecuentes  
**So that** puedo usar alias como "mi hermano" en lugar de datos completos

**Technical Details**:
- Lambda function: CRMMock
- DynamoDB table: Beneficiaries
- APIs: getBeneficiary, searchByAlias, addBeneficiary
- Beneficiary schema: beneficiaryId, userId, name, alias, accountNumber, frequency
- Fuzzy matching for alias resolution
- Action Group backend implementation

**Acceptance Criteria**:

**Given** usuario tiene beneficiario con alias "mi hermano"  
**When** busca por alias  
**Then** retorna datos de Juan López

**Given** alias ambiguo (múltiples matches)  
**When** se busca  
**Then** retorna lista de opciones para clarificar

**Given** beneficiario usado frecuentemente  
**When** se consulta lista  
**Then** aparece ordenado por frecuencia

**Given** nuevo beneficiario  
**When** se agrega  
**Then** se almacena en DynamoDB con userId asociado

**Error Scenarios**:
- **Given** alias no encontrado **When** se busca **Then** retorna lista vacía
- **Given** datos incompletos **When** se agrega beneficiario **Then** error de validación

**Demo Validation**:
- [ ] Búsqueda por alias "mi hermano" retorna Juan López
- [ ] Sistema maneja alias ambiguos pidiendo clarificación
- [ ] Beneficiarios frecuentes se ordenan correctamente

**Dependencies**: Story 3.2 (Action Groups configured)

---

## Epic 4: Marketplace Mock

### Story 2.4: Implement Marketplace Mock - Products
**Priority**: Must Have  
**Estimation**: 1.5 hours

**As a** Comprador (Ana)  
**I want** ver catálogo de productos disponibles en el marketplace  
**So that** puedo seleccionar qué comprar

**Technical Details**:
- Lambda function: MarketplaceMock
- DynamoDB table: Products
- APIs: listProducts, getProduct, searchProducts
- Product schema: productId, name, description, price, category, imageUrl, benefits[]
- Mock product data (laptops, phones, etc.)
- Action Group backend implementation

**Acceptance Criteria**:

**Given** solicitud de listar productos  
**When** se invoca API  
**Then** retorna catálogo completo de productos

**Given** búsqueda por categoría "laptops"  
**When** se filtra  
**Then** retorna solo productos de categoría laptops

**Given** productId específico  
**When** se consulta getProduct  
**Then** retorna detalles completos incluyendo beneficios

**Given** búsqueda por texto "HP"  
**When** se ejecuta  
**Then** retorna productos que contienen "HP" en nombre o descripción

**Error Scenarios**:
- **Given** productId inexistente **When** se consulta **Then** error 404
- **Given** categoría inválida **When** se filtra **Then** retorna lista vacía

**Demo Validation**:
- [ ] Listado de productos retorna catálogo completo
- [ ] Búsqueda por categoría funciona correctamente
- [ ] Detalles de producto incluyen beneficios

**Dependencies**: Story 3.2 (Action Groups configured)

---

### Story 2.5: Implement Benefits Engine
**Priority**: Must Have  
**Estimation**: 2 hours

**As a** Comprador (Ana)  
**I want** ver qué beneficios tengo disponibles para cada producto  
**So that** puedo tomar la mejor decisión de compra

**Technical Details**:
- Lambda function: MarketplaceMock (extend)
- API: calculateBenefits
- Benefit types: CASHBACK, MSI, DISCOUNT, POINTS
- Benefit calculation logic
- User eligibility validation
- Benefit comparison engine

**Acceptance Criteria**:

**Given** producto con múltiples beneficios  
**When** se consultan beneficios para usuario  
**Then** retorna lista de beneficios aplicables con cálculos

**Given** producto con cashback 5%  
**When** se calcula para compra de 10,000  
**Then** retorna cashback de 500 pesos

**Given** producto con MSI disponible  
**When** usuario tiene crédito suficiente  
**Then** retorna opciones de 3, 6, 12 MSI

**Given** múltiples beneficios  
**When** se comparan  
**Then** sistema sugiere mejor opción según perfil usuario

**Error Scenarios**:
- **Given** usuario sin crédito **When** solicita MSI **Then** indica crédito insuficiente
- **Given** beneficio expirado **When** se calcula **Then** no se incluye en opciones

**Demo Validation**:
- [ ] Cálculo de cashback es correcto
- [ ] Opciones de MSI se presentan cuando aplican
- [ ] Sistema sugiere mejor beneficio para usuario

**Dependencies**: Story 2.4 (Marketplace Mock - Products), Story 2.1 (Core Banking - credit line)

---

### Story 2.6: Implement Purchase Execution
**Priority**: Must Have  
**Estimation**: 1.5 hours

**As a** Comprador (Ana)  
**I want** ejecutar compra de producto con beneficios aplicados  
**So that** puedo adquirir productos y recibir beneficios automáticamente

**Technical Details**:
- Lambda function: MarketplaceMock (extend)
- API: executePurchase
- Purchase schema: purchaseId, userId, productId, amount, benefits[], timestamp
- DynamoDB table: Purchases
- Integration with Core Banking for payment
- Automatic benefit application

**Acceptance Criteria**:

**Given** usuario selecciona producto y beneficio  
**When** ejecuta compra  
**Then** saldo/crédito se debita y compra se registra

**Given** compra con cashback  
**When** se completa  
**Then** cashback se acredita automáticamente

**Given** compra con MSI  
**When** se ejecuta  
**Then** crédito se reduce y se configura plan de pagos

**Given** compra exitosa  
**When** se completa  
**Then** registro se guarda en tabla Purchases

**Error Scenarios**:
- **Given** saldo/crédito insuficiente **When** se intenta compra **Then** error de fondos
- **Given** producto agotado **When** se compra **Then** error de disponibilidad
- **Given** falla en aplicación de beneficio **When** ocurre **Then** compra se completa sin beneficio y se notifica

**Demo Validation**:
- [ ] Compra actualiza saldo correctamente
- [ ] Beneficios se aplican automáticamente
- [ ] Registro de compra persiste en DynamoDB
- [ ] Integración con Core Banking funciona

**Dependencies**: Story 2.5 (Benefits Engine), Story 2.1 (Core Banking Mock)

---


# DEV 1: FRONTEND/UI STORIES

## Epic 5: User Interface

### Story 1.1: Implement WebSocket Connection
**Priority**: Must Have  
**Estimation**: 1 hour

**As a** Usuario Bancario (Carlos)  
**I want** una conexión en tiempo real con CENTLI  
**So that** puedo tener conversaciones fluidas sin recargar la página

**Technical Details**:
- WebSocket client implementation
- Connection to API Gateway WebSocket
- Message sending/receiving
- Connection state management
- Reconnection logic
- Error handling

**Acceptance Criteria**:

**Given** usuario abre la aplicación  
**When** se inicializa  
**Then** WebSocket se conecta automáticamente

**Given** conexión establecida  
**When** usuario envía mensaje  
**Then** mensaje se transmite vía WebSocket

**Given** sistema envía respuesta  
**When** llega vía WebSocket  
**Then** se muestra en UI inmediatamente

**Given** conexión se pierde  
**When** se detecta desconexión  
**Then** intenta reconectar automáticamente

**Error Scenarios**:
- **Given** falla de red **When** se intenta conectar **Then** muestra error y reintenta
- **Given** WebSocket cerrado **When** se envía mensaje **Then** encola mensaje y reconecta

**Demo Validation**:
- [ ] Conexión WebSocket se establece al cargar app
- [ ] Mensajes se envían y reciben en tiempo real
- [ ] Reconexión automática funciona

**Dependencies**: None (base infrastructure)

---

### Story 1.2: Implement Voice Input UI
**Priority**: Must Have  
**Estimation**: 1.5 hours

**As a** Usuario Bancario (Carlos)  
**I want** un botón para activar entrada de voz  
**So that** puedo hablar con CENTLI en lugar de escribir

**Technical Details**:
- Voice input button/widget
- Browser MediaRecorder API
- Audio capture and streaming
- Visual feedback (recording indicator)
- Audio format conversion (if needed)
- Integration with WebSocket for audio transmission

**Acceptance Criteria**:

**Given** usuario presiona botón de voz  
**When** se activa  
**Then** comienza grabación de audio

**Given** usuario está hablando  
**When** audio se captura  
**Then** indicador visual muestra que está grabando

**Given** usuario termina de hablar  
**When** suelta botón o presiona stop  
**Then** audio se envía vía WebSocket a Nova Sonic

**Given** audio se está procesando  
**When** espera respuesta  
**Then** muestra indicador de "procesando"

**Error Scenarios**:
- **Given** permisos de micrófono denegados **When** se intenta grabar **Then** solicita permisos
- **Given** micrófono no disponible **When** se activa voz **Then** muestra error y sugiere texto

**Demo Validation**:
- [ ] Botón de voz captura audio correctamente
- [ ] Indicador visual muestra estado de grabación
- [ ] Audio se transmite a backend vía WebSocket

**Dependencies**: Story 1.1 (WebSocket Connection)

---

### Story 1.3: Implement Voice Output UI
**Priority**: Must Have  
**Estimation**: 1 hour

**As a** Usuario Bancario (Carlos)  
**I want** escuchar las respuestas de CENTLI en voz  
**So that** puedo recibir información sin mirar la pantalla

**Technical Details**:
- Audio playback component
- Browser Audio API
- Audio streaming from WebSocket
- Playback controls (pause, stop)
- Volume control
- Visual feedback (speaking indicator)

**Acceptance Criteria**:

**Given** sistema genera respuesta de voz  
**When** audio llega vía WebSocket  
**Then** se reproduce automáticamente

**Given** audio se está reproduciendo  
**When** usuario escucha  
**Then** indicador visual muestra que CENTLI está hablando

**Given** usuario quiere pausar  
**When** presiona control de pausa  
**Then** audio se pausa y puede reanudar

**Given** múltiples respuestas en cola  
**When** se reproducen  
**Then** se reproducen secuencialmente sin solaparse

**Error Scenarios**:
- **Given** audio corrupto **When** se intenta reproducir **Then** muestra error y ofrece texto
- **Given** volumen del dispositivo en 0 **When** reproduce **Then** muestra alerta de volumen

**Demo Validation**:
- [ ] Audio de respuesta se reproduce correctamente
- [ ] Indicador visual muestra cuando CENTLI habla
- [ ] Controles de playback funcionan

**Dependencies**: Story 1.1 (WebSocket Connection)

---

### Story 1.4: Implement Chat Interface
**Priority**: Must Have  
**Estimation**: 1.5 hours

**As a** Usuario Bancario (Carlos)  
**I want** una interfaz de chat clara y moderna  
**So that** puedo ver el historial de mi conversación con CENTLI

**Technical Details**:
- Chat UI component (messages list)
- Message bubbles (user vs assistant)
- Timestamp display
- Auto-scroll to latest message
- Message status indicators (sending, sent, error)
- Responsive design (mobile-first)

**Acceptance Criteria**:

**Given** usuario envía mensaje  
**When** se transmite  
**Then** aparece en chat con indicador "enviando"

**Given** mensaje enviado exitosamente  
**When** se confirma  
**Then** indicador cambia a "enviado"

**Given** CENTLI responde  
**When** respuesta llega  
**Then** aparece en chat con estilo diferenciado

**Given** múltiples mensajes  
**When** se acumulan  
**Then** chat hace scroll automático al último mensaje

**Error Scenarios**:
- **Given** mensaje falla al enviar **When** ocurre error **Then** muestra indicador de error y opción de reintentar
- **Given** respuesta muy larga **When** se muestra **Then** se formatea correctamente sin romper UI

**Demo Validation**:
- [ ] Mensajes de usuario y CENTLI se distinguen visualmente
- [ ] Auto-scroll funciona correctamente
- [ ] Timestamps se muestran en formato legible
- [ ] UI es responsive en móvil

**Dependencies**: Story 1.1 (WebSocket Connection)

---

### Story 1.5: Implement Transaction Confirmation UI
**Priority**: Must Have  
**Estimation**: 1 hour

**As a** Usuario Bancario (Carlos)  
**I want** ver confirmación clara de mis transacciones  
**So that** puedo verificar detalles antes de ejecutar

**Technical Details**:
- Confirmation modal/card component
- Transaction details display (monto, destinatario, concepto)
- Confirm/Cancel buttons
- Success/Error feedback
- Transaction receipt display

**Acceptance Criteria**:

**Given** usuario inicia transferencia  
**When** sistema valida datos  
**Then** muestra modal de confirmación con detalles

**Given** modal de confirmación  
**When** usuario revisa detalles  
**Then** puede ver: monto, destinatario, concepto, saldo resultante

**Given** usuario confirma  
**When** presiona botón confirmar  
**Then** ejecuta transacción y muestra feedback de éxito

**Given** transacción exitosa  
**When** se completa  
**Then** muestra recibo con detalles y opción de compartir

**Error Scenarios**:
- **Given** usuario cancela **When** presiona cancelar **Then** cierra modal sin ejecutar
- **Given** transacción falla **When** se ejecuta **Then** muestra error claro y opciones

**Demo Validation**:
- [ ] Modal de confirmación muestra todos los detalles
- [ ] Botones de confirmar/cancelar funcionan
- [ ] Feedback de éxito/error es claro
- [ ] Recibo se genera correctamente

**Dependencies**: Story 1.4 (Chat Interface)

---

### Story 1.6: Implement Product Catalog UI
**Priority**: Must Have  
**Estimation**: 1.5 hours

**As a** Comprador (Ana)  
**I want** ver catálogo de productos con imágenes y precios  
**So that** puedo explorar y seleccionar qué comprar

**Technical Details**:
- Product grid/list component
- Product card (image, name, price, benefits badge)
- Category filters
- Search functionality
- Product detail view
- Benefits comparison display

**Acceptance Criteria**:

**Given** usuario solicita ver productos  
**When** catálogo se carga  
**Then** muestra grid de productos con imágenes y precios

**Given** producto con beneficios  
**When** se muestra en catálogo  
**Then** badge indica tipo de beneficio (cashback, MSI, descuento)

**Given** usuario selecciona producto  
**When** hace click  
**Then** muestra vista detallada con todos los beneficios

**Given** múltiples beneficios disponibles  
**When** se muestran  
**Then** presenta comparación clara de opciones

**Error Scenarios**:
- **Given** imagen de producto no carga **When** se muestra **Then** usa placeholder
- **Given** catálogo vacío **When** se carga **Then** muestra mensaje apropiado

**Demo Validation**:
- [ ] Grid de productos se muestra correctamente
- [ ] Imágenes cargan y se ven bien
- [ ] Badges de beneficios son claros
- [ ] Vista detallada muestra toda la información
- [ ] Comparación de beneficios es fácil de entender

**Dependencies**: Story 1.4 (Chat Interface)

---

### Story 1.7: Implement Image Upload UI
**Priority**: Could Have  
**Estimation**: 1 hour

**As a** Usuario Bancario (Carlos)  
**I want** enviar imágenes a CENTLI  
**So that** puedo compartir recibos o fotos de productos

**Technical Details**:
- Image upload button/widget
- File picker integration
- Image preview before sending
- Image compression (if needed)
- Progress indicator for upload
- Integration with WebSocket/REST for transmission

**Acceptance Criteria**:

**Given** usuario presiona botón de imagen  
**When** se activa  
**Then** abre file picker del dispositivo

**Given** usuario selecciona imagen  
**When** se carga  
**Then** muestra preview antes de enviar

**Given** usuario confirma envío  
**When** presiona enviar  
**Then** imagen se transmite a backend

**Given** imagen se está subiendo  
**When** en progreso  
**Then** muestra indicador de progreso

**Error Scenarios**:
- **Given** archivo muy grande **When** se selecciona **Then** comprime o rechaza con mensaje
- **Given** formato no soportado **When** se selecciona **Then** muestra error de formato

**Demo Validation**:
- [ ] File picker abre correctamente
- [ ] Preview de imagen funciona
- [ ] Upload progresa y completa
- [ ] Imagen llega a backend

**Dependencies**: Story 1.1 (WebSocket Connection)

---


---

# SUMMARY

## Total Stories: 19 stories

### By Developer:
- **Dev 1 (Frontend/UI)**: 7 stories (8.5 hours estimated)
- **Dev 2 (Backend/Mocks)**: 6 stories (10 hours estimated)
- **Dev 3 (AgentCore/AI)**: 6 stories (10.5 hours estimated)

### By Priority:
- **Must Have**: 15 stories (critical for 8-hour demo)
- **Should Have**: 2 stories (important but not critical)
- **Could Have**: 2 stories (nice to have if time permits)

### By Epic:
- **Epic 1: Bedrock AgentCore Foundation** (Dev 3): 4 stories
- **Epic 2: Intelligent Processing** (Dev 3): 2 stories
- **Epic 3: Core Bancario Mock** (Dev 2): 3 stories
- **Epic 4: Marketplace Mock** (Dev 2): 3 stories
- **Epic 5: User Interface** (Dev 1): 7 stories

## Timeline Allocation (8 hours)

### Hours 1-2: Foundation
- **Dev 1**: Story 1.1 (WebSocket), Story 1.4 (Chat Interface)
- **Dev 2**: Story 2.1 (Core Banking Mock)
- **Dev 3**: Story 3.1 (AgentCore Setup)

### Hours 3-4: Core Features
- **Dev 1**: Story 1.2 (Voice Input), Story 1.3 (Voice Output)
- **Dev 2**: Story 2.2 (P2P Transfers), Story 2.4 (Marketplace Products)
- **Dev 3**: Story 3.2 (Action Groups), Story 3.3 (Nova Sonic)

### Hours 5-6: Integration & Polish
- **Dev 1**: Story 1.5 (Transaction Confirmation), Story 1.6 (Product Catalog)
- **Dev 2**: Story 2.5 (Benefits Engine), Story 2.6 (Purchase Execution)
- **Dev 3**: Story 3.5 (Intent Recognition), Story 3.6 (Managed Memory)

### Hours 7-8: Testing & Demo Prep
- **All Devs**: Integration testing, bug fixes, demo rehearsal
- **Optional**: Story 2.3 (CRM Mock), Story 3.4 (Nova Canvas), Story 1.7 (Image Upload)

## Critical Path

### Must Complete (Priority 1):
1. Story 3.1 → Story 3.2 → Story 3.3 (AgentCore foundation)
2. Story 2.1 → Story 2.2 (P2P capability)
3. Story 2.4 → Story 2.5 → Story 2.6 (Purchase capability)
4. Story 1.1 → Story 1.2 → Story 1.3 → Story 1.4 (UI foundation)

### Should Complete (Priority 2):
5. Story 3.5 (Intent Recognition)
6. Story 1.5 (Transaction Confirmation)
7. Story 1.6 (Product Catalog)

### Nice to Have (Priority 3):
8. Story 3.6 (Managed Memory)
9. Story 2.3 (CRM Mock)
10. Story 3.4 (Nova Canvas)
11. Story 1.7 (Image Upload)

## Dependencies Map

```
Story 3.1 (AgentCore Setup)
  ├── Story 3.2 (Action Groups)
  │     ├── Story 2.1 (Core Banking Mock)
  │     │     └── Story 2.2 (P2P Transfers)
  │     ├── Story 2.3 (CRM Mock)
  │     └── Story 2.4 (Marketplace Mock)
  │           ├── Story 2.5 (Benefits Engine)
  │           └── Story 2.6 (Purchase Execution)
  ├── Story 3.3 (Nova Sonic)
  ├── Story 3.4 (Nova Canvas)
  ├── Story 3.5 (Intent Recognition)
  └── Story 3.6 (Managed Memory)

Story 1.1 (WebSocket)
  ├── Story 1.2 (Voice Input)
  ├── Story 1.3 (Voice Output)
  ├── Story 1.4 (Chat Interface)
  │     ├── Story 1.5 (Transaction Confirmation)
  │     └── Story 1.6 (Product Catalog)
  └── Story 1.7 (Image Upload)
```

## Risk Mitigation

### High Risk Stories (Complex/Critical):
- **Story 3.1** (AgentCore Setup): 2 hours - Foundation for everything
- **Story 3.2** (Action Groups): 2 hours - Critical integration point
- **Story 3.3** (Nova Sonic): 2 hours - Voice is demo centerpiece
- **Story 2.2** (P2P Transfers): 2 hours - Core business logic

**Mitigation**: Start these first, allocate best developers, have fallback plans

### Medium Risk Stories:
- **Story 2.5** (Benefits Engine): 2 hours - Complex calculation logic
- **Story 2.6** (Purchase Execution): 1.5 hours - Multiple integrations
- **Story 3.5** (Intent Recognition): 1.5 hours - NLU complexity

**Mitigation**: Start early in timeline, test thoroughly

### Low Risk Stories:
- **Story 1.1-1.7** (Frontend): Standard web development
- **Story 2.1** (Core Banking Mock): Simple CRUD operations

**Mitigation**: Can be done in parallel, less critical path

## Demo Scenarios Coverage

### Scenario 1: Transferencia P2P por Voz
**Stories Required**:
- Story 3.1, 3.2, 3.3, 3.5 (AgentCore + Voice + Intent)
- Story 2.1, 2.2 (Core Banking + P2P)
- Story 1.1, 1.2, 1.3, 1.4, 1.5 (UI + Voice + Confirmation)
- **Optional**: Story 2.3 (CRM for alias resolution)

### Scenario 2: Compra de Producto con Beneficios
**Stories Required**:
- Story 3.1, 3.2, 3.5 (AgentCore + Intent)
- Story 2.4, 2.5, 2.6 (Marketplace + Benefits + Purchase)
- Story 1.1, 1.4, 1.6 (UI + Product Catalog)
- **Optional**: Story 3.3 (Voice for purchase)

## INVEST Criteria Compliance

All stories have been validated against INVEST criteria:
- **Independent**: Stories can be developed in parallel by different devs
- **Negotiable**: Scope can be adjusted (Must/Should/Could Have)
- **Valuable**: Each story delivers user value
- **Estimable**: All stories have hour estimates
- **Small**: Stories range from 1-2 hours (appropriate for 8-hour hackathon)
- **Testable**: All stories have clear acceptance criteria and demo validation

## Notes for Implementation

### Parallel Work Strategy:
- **Dev 1** focuses on UI/UX - minimal backend dependencies initially
- **Dev 2** focuses on mocks - can work independently with mock data
- **Dev 3** focuses on AgentCore - critical path, needs to complete first

### Integration Points:
- **Hour 4**: First integration (AgentCore + Mocks)
- **Hour 6**: Second integration (AgentCore + Mocks + Frontend)
- **Hour 7-8**: Full integration testing

### Communication:
- Sync every 2 hours
- Use GitHub issues for stories
- Slack/Discord for real-time coordination
- Shared Postman collection for API testing

### Quality Gates:
- Each story must pass Demo Validation checklist
- Integration tests at hours 4, 6
- Full demo rehearsal at hour 7.5
