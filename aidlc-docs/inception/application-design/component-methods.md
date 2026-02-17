# Component Methods - CENTLI

## Overview

This document defines method signatures for each application component. Detailed business rules and implementation logic will be defined later in Functional Design (CONSTRUCTION phase).

**Note**: Infrastructure Foundation (Component 1) has no methods - it's pure configuration.

---

## Component 2: AgentCore Orchestrator

**Note**: AgentCore is a managed Bedrock service, not a Lambda. Configuration is done via Bedrock Agent setup, not code methods. Listed here are the conceptual capabilities configured in the agent.

### Configured Capabilities

#### process_message
**Purpose**: Main entry point for processing user messages  
**Input**: 
- `message_content`: str - User message (text/transcribed voice)
- `user_id`: str - User identifier
- `session_id`: str - Session identifier
- `modality`: str - Input type ("text", "voice", "image")
- `metadata`: dict - Additional context (auth tokens, biometric data)

**Output**:
- `response`: dict - Generated response with text and optional audio
- `action_events`: list - Events to publish to EventBridge
- `session_state`: dict - Updated session context

**High-level Purpose**: Analyze user intent, determine required actions, orchestrate Action Groups

---

#### recognize_intent
**Purpose**: Identify user intent from natural language input  
**Input**:
- `message`: str - User message
- `context`: dict - Conversation history and user context

**Output**:
- `intent`: str - Identified intent (TRANSFER, PURCHASE, QUERY, HELP)
- `entities`: dict - Extracted entities (amount, beneficiary, product, etc.)
- `confidence`: float - Confidence score (0-1)

**High-level Purpose**: Use Claude 3.7 Sonnet to classify intent and extract entities

---

#### validate_authentication
**Purpose**: Validate user authentication and biometric data  
**Input**:
- `user_id`: str - User identifier
- `auth_token`: str - Authentication token
- `biometric_data`: dict - Voice print or other biometric data (optional)
- `transaction_type`: str - Type of transaction requiring auth

**Output**:
- `is_authenticated`: bool - Authentication status
- `auth_level`: str - Authentication level (BASIC, BIOMETRIC, MFA)
- `error`: str - Error message if authentication fails

**High-level Purpose**: Verify user identity before executing sensitive operations

---

#### manage_session
**Purpose**: Create, update, or retrieve session state  
**Input**:
- `session_id`: str - Session identifier
- `user_id`: str - User identifier
- `operation`: str - Operation type (CREATE, UPDATE, GET, DELETE)
- `session_data`: dict - Session data to store (optional)

**Output**:
- `session`: dict - Session object with state
- `success`: bool - Operation success status

**High-level Purpose**: Coordinate with Managed Memory for session persistence

---

#### process_voice_input
**Purpose**: Process voice input via Nova Sonic  
**Input**:
- `audio_data`: bytes - Audio stream data
- `audio_format`: str - Audio format (wav, mp3, etc.)
- `language`: str - Language code (es-MX)

**Output**:
- `transcription`: str - Transcribed text
- `confidence`: float - Transcription confidence
- `error`: str - Error message if transcription fails

**High-level Purpose**: Convert speech to text using Nova Sonic

---

#### generate_voice_output
**Purpose**: Generate voice response via Nova Sonic  
**Input**:
- `text`: str - Text to synthesize
- `language`: str - Language code (es-MX)
- `voice_style`: str - Voice style/emotion (professional, warm, etc.)

**Output**:
- `audio_data`: bytes - Synthesized audio stream
- `audio_format`: str - Audio format
- `duration`: float - Audio duration in seconds

**High-level Purpose**: Convert text to speech using Nova Sonic

---

#### process_image_input
**Purpose**: Analyze image input via Nova Canvas  
**Input**:
- `image_url`: str - S3 URL of uploaded image
- `analysis_type`: str - Type of analysis (OCR, OBJECT_DETECTION, GENERAL)

**Output**:
- `analysis_result`: dict - Extracted information from image
- `text_content`: str - OCR text if applicable
- `objects`: list - Detected objects if applicable
- `confidence`: float - Analysis confidence

**High-level Purpose**: Extract information from images using Nova Canvas

---

#### publish_action_event
**Purpose**: Publish event to EventBridge for Action Group invocation  
**Input**:
- `action_type`: str - Action type (TRANSFER, PURCHASE, QUERY_BENEFICIARY)
- `action_data`: dict - Action parameters
- `user_id`: str - User identifier
- `session_id`: str - Session identifier

**Output**:
- `event_id`: str - Published event identifier
- `success`: bool - Publish success status

**High-level Purpose**: Send action requests to Action Groups via EventBridge

---

## Component 3: Orchestration Service

### Lambda: app_connect

#### handle_connect
**Purpose**: Handle new WebSocket connection  
**Input**:
- `connection_id`: str - WebSocket connection ID
- `query_params`: dict - Query parameters (auth token, user_id)

**Output**:
- `status_code`: int - HTTP status code (200, 401, 500)
- `body`: str - Response message

**High-level Purpose**: Establish WebSocket connection and initialize session

---

### Lambda: app_disconnect

#### handle_disconnect
**Purpose**: Handle WebSocket disconnection  
**Input**:
- `connection_id`: str - WebSocket connection ID

**Output**:
- `status_code`: int - HTTP status code (200, 500)
- `body`: str - Response message

**High-level Purpose**: Clean up session and connection state

---

### Lambda: app_message (evolved from app_inference)

#### handle_message
**Purpose**: Main message handler for WebSocket messages  
**Input**:
- `connection_id`: str - WebSocket connection ID
- `message`: dict - Message payload
- `message_type`: str - Message type (TEXT, VOICE, IMAGE)

**Output**:
- `status_code`: int - HTTP status code
- `response`: dict - Response to send back to client

**High-level Purpose**: Route messages to AgentCore and return responses

---

#### route_to_agentcore
**Purpose**: Route message to AgentCore for processing  
**Input**:
- `user_id`: str - User identifier
- `session_id`: str - Session identifier
- `message_content`: str - Message content
- `modality`: str - Input modality
- `metadata`: dict - Additional context

**Output**:
- `agentcore_response`: dict - Response from AgentCore
- `success`: bool - Invocation success status

**High-level Purpose**: Invoke AgentCore and handle response

---

#### manage_local_session
**Purpose**: Manage session state in local DynamoDB  
**Input**:
- `session_id`: str - Session identifier
- `operation`: str - Operation (CREATE, UPDATE, GET, DELETE)
- `session_data`: dict - Session data (optional)

**Output**:
- `session`: dict - Session object
- `success`: bool - Operation success

**High-level Purpose**: Maintain local session cache for fast access

---

#### sync_with_managed_memory
**Purpose**: Synchronize local session with Bedrock Managed Memory  
**Input**:
- `session_id`: str - Session identifier
- `local_session`: dict - Local session data
- `sync_direction`: str - Direction (LOCAL_TO_BEDROCK, BEDROCK_TO_LOCAL, BIDIRECTIONAL)

**Output**:
- `synced_session`: dict - Synchronized session data
- `conflicts`: list - Any conflicts detected
- `success`: bool - Sync success status

**High-level Purpose**: Keep local and Bedrock memory in sync

---

#### handle_voice_stream
**Purpose**: Handle streaming voice data  
**Input**:
- `connection_id`: str - WebSocket connection ID
- `audio_chunk`: bytes - Audio data chunk
- `is_final`: bool - Whether this is the final chunk

**Output**:
- `transcription`: str - Partial or final transcription
- `success`: bool - Processing success

**High-level Purpose**: Stream audio to AgentCore for real-time transcription

---

#### handle_image_upload
**Purpose**: Handle image upload to S3  
**Input**:
- `connection_id`: str - WebSocket connection ID
- `image_data`: bytes - Image data
- `image_format`: str - Image format (jpg, png)
- `user_id`: str - User identifier

**Output**:
- `s3_url`: str - S3 URL of uploaded image
- `success`: bool - Upload success

**High-level Purpose**: Upload image to S3 and return URL for processing

---

#### send_response
**Purpose**: Send response back to WebSocket client  
**Input**:
- `connection_id`: str - WebSocket connection ID
- `response_data`: dict - Response payload
- `response_type`: str - Response type (TEXT, VOICE, ERROR)

**Output**:
- `success`: bool - Send success status

**High-level Purpose**: Deliver responses to connected clients

---

## Component 4: Core Banking Mock (Action Group)

### Action Group Methods

#### get_balance
**Purpose**: Retrieve user account balance  
**Input**:
- `user_id`: str - User identifier

**Output**:
- `balance`: float - Current balance
- `currency`: str - Currency code (MXN)
- `account_number`: str - Account number
- `success`: bool - Operation success
- `error`: str - Error message if failed

**High-level Purpose**: Query account balance from DynamoDB

---

#### get_account
**Purpose**: Retrieve complete account information  
**Input**:
- `user_id`: str - User identifier

**Output**:
- `account`: dict - Account object with all details
- `success`: bool - Operation success
- `error`: str - Error message if failed

**High-level Purpose**: Get full account details including credit line

---

#### validate_funds
**Purpose**: Validate if user has sufficient funds  
**Input**:
- `user_id`: str - User identifier
- `amount`: float - Amount to validate
- `transaction_type`: str - Transaction type (DEBIT, CREDIT_PURCHASE)

**Output**:
- `has_funds`: bool - Whether funds are sufficient
- `available_balance`: float - Available balance
- `shortfall`: float - Amount short if insufficient (0 if sufficient)
- `success`: bool - Validation success

**High-level Purpose**: Check balance before transaction execution

---

#### execute_transfer
**Purpose**: Execute P2P transfer between accounts  
**Input**:
- `from_user_id`: str - Source user ID
- `to_account_number`: str - Destination account number
- `amount`: float - Transfer amount
- `concept`: str - Transfer concept/description

**Output**:
- `transaction_id`: str - Generated transaction ID
- `new_balance`: float - New balance after transfer
- `timestamp`: str - Transaction timestamp (ISO 8601)
- `success`: bool - Transfer success
- `error`: str - Error message if failed

**High-level Purpose**: Execute atomic transfer with balance updates

---

#### get_transactions
**Purpose**: Retrieve transaction history  
**Input**:
- `user_id`: str - User identifier
- `limit`: int - Maximum number of transactions (default: 10)
- `start_date`: str - Start date filter (optional, ISO 8601)
- `end_date`: str - End date filter (optional, ISO 8601)

**Output**:
- `transactions`: list - List of transaction objects
- `count`: int - Number of transactions returned
- `success`: bool - Query success
- `error`: str - Error message if failed

**High-level Purpose**: Query transaction history with filters

---

#### validate_account_exists
**Purpose**: Check if account exists  
**Input**:
- `account_number`: str - Account number to validate

**Output**:
- `exists`: bool - Whether account exists
- `account_holder`: str - Account holder name if exists
- `success`: bool - Validation success

**High-level Purpose**: Validate destination account before transfer

---

### EventBridge Event Handler

#### handle_action_event
**Purpose**: Main event handler for EventBridge events  
**Input**:
- `event`: dict - EventBridge event payload
- `context`: dict - Lambda context

**Output**:
- `response_event`: dict - Response event to publish
- `success`: bool - Handler success

**High-level Purpose**: Route incoming events to appropriate action methods

---

## Component 5: Marketplace Mock (Action Group)

### Action Group Methods

#### list_products
**Purpose**: List products in catalog  
**Input**:
- `category`: str - Product category filter (optional)
- `limit`: int - Maximum products to return (default: 20)
- `offset`: int - Pagination offset (default: 0)

**Output**:
- `products`: list - List of product objects
- `total_count`: int - Total products matching filter
- `success`: bool - Query success
- `error`: str - Error message if failed

**High-level Purpose**: Browse product catalog with filters

---

#### get_product
**Purpose**: Get detailed product information  
**Input**:
- `product_id`: str - Product identifier

**Output**:
- `product`: dict - Complete product object with benefits
- `success`: bool - Query success
- `error`: str - Error message if failed

**High-level Purpose**: Retrieve full product details

---

#### search_products
**Purpose**: Search products by text query  
**Input**:
- `query`: str - Search query
- `limit`: int - Maximum results (default: 20)

**Output**:
- `products`: list - Matching products
- `count`: int - Number of results
- `success`: bool - Search success
- `error`: str - Error message if failed

**High-level Purpose**: Full-text search across product catalog

---

#### calculate_benefits
**Purpose**: Calculate available benefits for product and user  
**Input**:
- `product_id`: str - Product identifier
- `user_id`: str - User identifier
- `purchase_amount`: float - Purchase amount

**Output**:
- `benefits`: list - List of available benefit options
- `recommended_benefit`: dict - Best benefit for user
- `success`: bool - Calculation success
- `error`: str - Error message if failed

**High-level Purpose**: Compute cashback, MSI, discounts, points for product

---

#### execute_purchase
**Purpose**: Execute product purchase with benefits  
**Input**:
- `user_id`: str - User identifier
- `product_id`: str - Product identifier
- `benefit_option`: dict - Selected benefit option
- `payment_method`: str - Payment method (DEBIT, CREDIT)

**Output**:
- `purchase_id`: str - Generated purchase ID
- `applied_benefits`: dict - Benefits applied
- `final_amount`: float - Final amount charged
- `timestamp`: str - Purchase timestamp (ISO 8601)
- `success`: bool - Purchase success
- `error`: str - Error message if failed

**High-level Purpose**: Process purchase and apply benefits

---

#### get_purchase_history
**Purpose**: Retrieve user purchase history  
**Input**:
- `user_id`: str - User identifier
- `limit`: int - Maximum purchases (default: 10)

**Output**:
- `purchases`: list - List of purchase objects
- `count`: int - Number of purchases
- `success`: bool - Query success
- `error`: str - Error message if failed

**High-level Purpose**: Query past purchases

---

### EventBridge Event Handler

#### handle_action_event
**Purpose**: Main event handler for EventBridge events  
**Input**:
- `event`: dict - EventBridge event payload
- `context`: dict - Lambda context

**Output**:
- `response_event`: dict - Response event to publish
- `success`: bool - Handler success

**High-level Purpose**: Route incoming events to appropriate action methods

---

#### publish_payment_event
**Purpose**: Publish payment event to Core Banking  
**Input**:
- `user_id`: str - User identifier
- `amount`: float - Payment amount
- `purchase_id`: str - Purchase identifier
- `payment_method`: str - Payment method

**Output**:
- `event_id`: str - Published event ID
- `success`: bool - Publish success

**High-level Purpose**: Trigger payment processing in Core Banking

---

## Component 6: CRM Mock (Action Group)

### Action Group Methods

#### search_beneficiary
**Purpose**: Search beneficiary by alias or name  
**Input**:
- `user_id`: str - User identifier
- `alias`: str - Alias to search ("mi hermano", "mi mamá")

**Output**:
- `beneficiaries`: list - Matching beneficiaries (may be multiple)
- `is_ambiguous`: bool - Whether multiple matches found
- `count`: int - Number of matches
- `success`: bool - Search success
- `error`: str - Error message if failed

**High-level Purpose**: Resolve natural language alias to beneficiary

---

#### get_beneficiary
**Purpose**: Get beneficiary by ID  
**Input**:
- `beneficiary_id`: str - Beneficiary identifier

**Output**:
- `beneficiary`: dict - Beneficiary object
- `success`: bool - Query success
- `error`: str - Error message if failed

**High-level Purpose**: Retrieve specific beneficiary details

---

#### add_beneficiary
**Purpose**: Add new beneficiary  
**Input**:
- `user_id`: str - User identifier
- `name`: str - Beneficiary name
- `alias`: str - Alias for beneficiary
- `account_number`: str - Beneficiary account number
- `bank`: str - Bank name (optional)

**Output**:
- `beneficiary_id`: str - Generated beneficiary ID
- `success`: bool - Creation success
- `error`: str - Error message if failed

**High-level Purpose**: Create new beneficiary relationship

---

#### update_beneficiary
**Purpose**: Update beneficiary information  
**Input**:
- `beneficiary_id`: str - Beneficiary identifier
- `updates`: dict - Fields to update

**Output**:
- `beneficiary`: dict - Updated beneficiary object
- `success`: bool - Update success
- `error`: str - Error message if failed

**High-level Purpose**: Modify beneficiary details

---

#### delete_beneficiary
**Purpose**: Delete beneficiary  
**Input**:
- `beneficiary_id`: str - Beneficiary identifier

**Output**:
- `success`: bool - Deletion success
- `error`: str - Error message if failed

**High-level Purpose**: Remove beneficiary relationship

---

#### get_frequent_beneficiaries
**Purpose**: Get most frequently used beneficiaries  
**Input**:
- `user_id`: str - User identifier
- `limit`: int - Maximum beneficiaries (default: 5)

**Output**:
- `beneficiaries`: list - Beneficiaries sorted by frequency
- `count`: int - Number of beneficiaries
- `success`: bool - Query success
- `error`: str - Error message if failed

**High-level Purpose**: Suggest frequent beneficiaries for quick access

---

#### increment_usage_frequency
**Purpose**: Increment beneficiary usage counter  
**Input**:
- `beneficiary_id`: str - Beneficiary identifier

**Output**:
- `new_frequency`: int - Updated frequency count
- `success`: bool - Update success

**High-level Purpose**: Track beneficiary usage for suggestions

---

### EventBridge Event Handler

#### handle_action_event
**Purpose**: Main event handler for EventBridge events  
**Input**:
- `event`: dict - EventBridge event payload
- `context`: dict - Lambda context

**Output**:
- `response_event`: dict - Response event to publish
- `success`: bool - Handler success

**High-level Purpose**: Route incoming events to appropriate action methods

---

## Component 7: Frontend Multimodal UI

### JavaScript Module: WebSocketManager

#### connect
**Purpose**: Establish WebSocket connection  
**Input**:
- `auth_token`: str - Authentication token
- `user_id`: str - User identifier

**Output**:
- `connection`: WebSocket - WebSocket connection object
- `success`: bool - Connection success

**High-level Purpose**: Connect to Orchestration Service

---

#### disconnect
**Purpose**: Close WebSocket connection  
**Input**: None

**Output**:
- `success`: bool - Disconnection success

**High-level Purpose**: Clean disconnect from server

---

#### send_message
**Purpose**: Send message via WebSocket  
**Input**:
- `message`: dict - Message payload
- `message_type`: str - Message type (TEXT, VOICE, IMAGE)

**Output**:
- `success`: bool - Send success

**High-level Purpose**: Transmit message to server

---

#### on_message
**Purpose**: Handle incoming WebSocket message  
**Input**:
- `message`: dict - Received message

**Output**: None (triggers UI updates)

**High-level Purpose**: Process server responses

---

### JavaScript Module: VoiceManager

#### start_recording
**Purpose**: Start voice recording  
**Input**: None

**Output**:
- `recorder`: MediaRecorder - Recorder instance
- `success`: bool - Start success

**High-level Purpose**: Capture audio from microphone

---

#### stop_recording
**Purpose**: Stop voice recording and send audio  
**Input**: None

**Output**:
- `audio_data`: Blob - Recorded audio data
- `success`: bool - Stop success

**High-level Purpose**: Finalize recording and transmit

---

#### play_audio
**Purpose**: Play audio response  
**Input**:
- `audio_data`: Blob - Audio data to play

**Output**:
- `success`: bool - Playback success

**High-level Purpose**: Play voice response from server

---

### JavaScript Module: ChatManager

#### add_message
**Purpose**: Add message to chat UI  
**Input**:
- `message`: dict - Message object
- `sender`: str - Sender type (USER, ASSISTANT)

**Output**: None (updates UI)

**High-level Purpose**: Display message in chat interface

---

#### clear_chat
**Purpose**: Clear chat history  
**Input**: None

**Output**: None (updates UI)

**High-level Purpose**: Reset chat display

---

#### auto_scroll
**Purpose**: Scroll to latest message  
**Input**: None

**Output**: None (updates UI)

**High-level Purpose**: Keep latest message visible

---

### JavaScript Module: ImageManager

#### upload_image
**Purpose**: Upload image to server  
**Input**:
- `image_file`: File - Image file from picker

**Output**:
- `s3_url`: str - S3 URL of uploaded image
- `success`: bool - Upload success

**High-level Purpose**: Send image for processing

---

### JavaScript Module: TransactionManager

#### show_confirmation
**Purpose**: Display transaction confirmation modal  
**Input**:
- `transaction_details`: dict - Transaction details

**Output**: Promise - Resolves with user confirmation

**High-level Purpose**: Get user confirmation before transaction

---

#### show_receipt
**Purpose**: Display transaction receipt  
**Input**:
- `transaction`: dict - Completed transaction

**Output**: None (updates UI)

**High-level Purpose**: Show transaction success

---

### JavaScript Module: ProductCatalogManager

#### display_products
**Purpose**: Display product grid  
**Input**:
- `products`: list - Product list

**Output**: None (updates UI)

**High-level Purpose**: Render product catalog

---

#### show_product_details
**Purpose**: Show product detail view  
**Input**:
- `product`: dict - Product object

**Output**: None (updates UI)

**High-level Purpose**: Display full product information

---

#### show_benefits_comparison
**Purpose**: Display benefits comparison  
**Input**:
- `benefits`: list - Available benefits

**Output**: Promise - Resolves with selected benefit

**High-level Purpose**: Help user choose best benefit

---

**Document Status**: Complete  
**Created**: 2026-02-16  
**Total Methods**: 60+ methods across 6 application components  
**Note**: Detailed business rules will be defined in Functional Design (CONSTRUCTION phase)
