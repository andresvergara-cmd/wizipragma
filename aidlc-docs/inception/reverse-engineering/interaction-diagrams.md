# Interaction Diagrams

## Business Transaction: Consulta Financiera Completa

Este diagrama muestra cómo se implementa la transacción de negocio principal: un usuario hace una consulta financiera y recibe una respuesta personalizada.

```
Usuario          API Gateway      Lambda          Lambda         DynamoDB      DynamoDB       DynamoDB      DynamoDB      AWS
                 WebSocket        Connect         Inference      ChatHistory   Users          Transactions  Retailers     Bedrock
  |                  |               |                |              |             |              |             |           |
  |--wss connect---->|               |                |              |             |              |             |           |
  |                  |--$connect---->|                |              |             |              |             |           |
  |                  |               |--return 200--->|              |             |              |             |           |
  |<--connected------|<--------------|                |              |             |              |             |           |
  |                  |               |                |              |             |              |             |           |
  |--sendMessage---->|               |                |              |             |              |             |           |
  | {user_id,        |               |                |              |             |              |             |           |
  |  message,        |               |                |              |             |              |             |           |
  |  session_id}     |               |                |              |             |              |             |           |
  |                  |--sendMessage----------------->|              |             |              |             |           |
  |                  |               |                |              |             |              |             |           |
  |                  |               |                |--Query------>|             |              |             |           |
  |                  |               |                |  session_id  |             |              |             |           |
  |                  |               |                |<--history----|             |              |             |           |
  |                  |               |                |              |             |              |             |           |
  |                  |               |                |--Delete----->|             |              |             |           |
  |                  |               |                |  session     |             |              |             |           |
  |                  |               |                |<--deleted----|             |              |             |           |
  |                  |               |                |              |             |              |             |           |
  |                  |               |                |--Query user_id------------>|              |             |           |
  |                  |               |                |<--user profile-------------|              |             |           |
  |                  |               |                |              |             |              |             |           |
  |                  |               |                |--Scan all transactions-------------------->|             |           |
  |                  |               |                |<--transactions list------------------------|             |           |
  |                  |               |                |              |             |              |             |           |
  |                  |               |                |--Scan all retailers----------------------------------->|           |
  |                  |               |                |<--retailers list---------------------------------------|           |
  |                  |               |                |              |             |              |             |           |
  |                  |               |                |--[Format complete user context]           |             |           |
  |                  |               |                |              |             |              |             |           |
  |                  |               |                |--converse_stream(context, message, history)----------->|           |
  |                  |               |                |              |             |              |             |           |
  |                  |               |                |<--stream chunk 1----------------------------------------|           |
  |                  |<--post_to_connection-----------|              |             |              |             |           |
  |<--token 1--------|               |                |              |             |              |             |           |
  |                  |               |                |<--stream chunk 2----------------------------------------|           |
  |                  |<--post_to_connection-----------|              |             |              |             |           |
  |<--token 2--------|               |                |              |             |              |             |           |
  |                  |               |                |<--stream chunk N----------------------------------------|           |
  |                  |<--post_to_connection-----------|              |             |              |             |           |
  |<--token N--------|               |                |              |             |              |             |           |
  |                  |               |                |              |             |              |             |           |
  |                  |               |                |--PutItem---->|             |              |             |           |
  |                  |               |                |  updated     |             |              |             |           |
  |                  |               |                |  history     |             |              |             |           |
  |                  |               |                |<--saved------|             |              |             |           |
  |                  |               |                |              |             |              |             |           |
  |                  |               |                |--return 200->|             |              |             |           |
  |                  |               |                |              |             |              |             |           |
```

## Business Transaction: Establecer Sesión

```
Usuario          API Gateway      Lambda
                 WebSocket        Connect
  |                  |               |
  |--wss://url------>|               |
  |  (handshake)     |               |
  |                  |--$connect---->|
  |                  |               |
  |                  |               |--[Generate connection_id]
  |                  |               |
  |                  |               |--return 200
  |                  |               |  {statusCode: 200,
  |                  |               |   body: "Connection Established: {id}"}
  |                  |<--------------|
  |<--connected------|               |
  |  (connection_id) |               |
  |                  |               |
```

## Business Transaction: Cerrar Sesión

```
Usuario          API Gateway      Lambda
                 WebSocket        Disconnect
  |                  |               |
  |--close---------->|               |
  |                  |--$disconnect->|
  |                  |               |
  |                  |               |--[Cleanup resources]
  |                  |               |
  |                  |               |--return 200
  |                  |               |  {statusCode: 200,
  |                  |               |   body: "Connection closed"}
  |                  |<--------------|
  |<--closed---------|               |
  |                  |               |
```

## Component Interaction: Data Context Building

```
Lambda           data_config.py                DynamoDB      DynamoDB       DynamoDB
Inference                                      Users         Transactions   Retailers
  |                  |                            |             |              |
  |--get_user_context(table_names, user_id)---->|             |              |
  |                  |                            |             |              |
  |                  |--get_user_data(user_id)-->|             |              |
  |                  |<--user profile------------|             |              |
  |                  |                            |             |              |
  |                  |--format_user_context()                  |              |
  |                  |  [Format profile sections]              |              |
  |                  |                            |             |              |
  |                  |--scan_table(transactions)-------------->|              |
  |                  |<--all transactions----------------------|              |
  |                  |                            |             |              |
  |                  |--summarize_transactions()               |              |
  |                  |  [Filter by user_id]                    |              |
  |                  |  [Group by month/category]              |              |
  |                  |  [Get recent N transactions]            |              |
  |                  |  [Extract unique categories]            |              |
  |                  |                            |             |              |
  |                  |--scan_table(retailers)------------------------------>|
  |                  |<--all retailers------------------------------------|
  |                  |                            |             |              |
  |                  |--format_retailer_context_pairs()        |              |
  |                  |  [Filter by user categories]            |              |
  |                  |  [Group by industry]                    |              |
  |                  |  [Format in pairs]                      |              |
  |                  |                            |             |              |
  |                  |--[Combine all sections]                 |              |
  |                  |                            |             |              |
  |<--complete context string--------------------|             |              |
  |                  |                            |             |              |
```

## Component Interaction: Chat History Management

```
Lambda           config.py                      bedrock_config.py    DynamoDB      AWS
Inference        ConfigChat                                          ChatHistory   Bedrock
  |                  |                                |                  |           |
  |--chat_with_bedrock(query, context, conn_id, session_id)-->         |           |
  |                  |                                |                  |           |
  |                  |--retrieve_chat_history(session_id)-------------->|           |
  |                  |                                |                  |           |
  |                  |--get_session_data(session_id)------------------->|           |
  |                  |<--session data-----------------------------------|           |
  |                  |                                |                  |           |
  |                  |--delete_session(session_id)---------------------->|           |
  |                  |<--deleted----------------------------------------|           |
  |                  |                                |                  |           |
  |                  |<--{session_id, conversation[]}|                  |           |
  |                  |                                |                  |           |
  |                  |--parse_conversation_history()  |                  |           |
  |                  |  [Convert to Bedrock format]   |                  |           |
  |                  |  [Limit to max_turns if needed]|                  |           |
  |                  |                                |                  |           |
  |                  |--stream_chat(model, context, query, history, conn_id)-------->|
  |                  |                                |                  |           |
  |                  |                                |--converse_stream------------>|
  |                  |                                |<--chunk 1--------------------|
  |                  |                                |--transmit_response(chunk 1)  |
  |                  |                                |  [post_to_connection]        |
  |                  |                                |<--chunk 2--------------------|
  |                  |                                |--transmit_response(chunk 2)  |
  |                  |                                |<--chunk N--------------------|
  |                  |                                |--transmit_response(chunk N)  |
  |                  |                                |                  |           |
  |                  |<--complete response------------|                  |           |
  |                  |                                |                  |           |
  |                  |--update_chat_history(history, query, response)-->|           |
  |                  |  [Append new interaction]      |                  |           |
  |                  |                                |                  |           |
  |                  |--put_item(updated history)----------------------->|           |
  |                  |<--saved------------------------------------------|           |
  |                  |                                |                  |           |
  |<--response-------|                                |                  |           |
  |                  |                                |                  |           |
```

## Error Flow: Connection Lost During Streaming

```
Lambda           bedrock_config.py    API Gateway      Usuario
Inference                             Management
  |                  |                    |              |
  |--stream_chat---->|                    |              |
  |                  |--converse_stream-->|              |
  |                  |<--chunk 1----------|              |
  |                  |--post_to_connection-------------->|
  |                  |                    |<--ACK--------|
  |                  |<--chunk 2----------|              |
  |                  |--post_to_connection-------------->|
  |                  |                    |   X (disconnected)
  |                  |<--GoneException----|              |
  |                  |                    |              |
  |                  |--[Log warning]     |              |
  |                  |--[Continue streaming but don't transmit]
  |                  |<--chunk 3----------|              |
  |                  |  (skip transmission)              |
  |                  |<--chunk N----------|              |
  |                  |  (skip transmission)              |
  |                  |                    |              |
  |<--complete response (for history)----|              |
  |                  |                    |              |
  |--[Save to history anyway]            |              |
  |                  |                    |              |
```

## Data Flow: User Context Assembly

```
                    +------------------+
                    | get_user_context |
                    +------------------+
                            |
            +---------------+---------------+
            |               |               |
            v               v               v
    +-------------+  +-------------+  +-------------+
    | Get User    |  | Get Trans-  |  | Get         |
    | Profile     |  | actions     |  | Retailers   |
    +-------------+  +-------------+  +-------------+
            |               |               |
            v               v               v
    +-------------+  +-------------+  +-------------+
    | Format      |  | Summarize   |  | Filter &    |
    | Profile     |  | by Month    |  | Format      |
    | Sections    |  | & Category  |  | by Industry |
    +-------------+  +-------------+  +-------------+
            |               |               |
            +---------------+---------------+
                            |
                            v
                    +------------------+
                    | Combine Sections |
                    | with Separators  |
                    +------------------+
                            |
                            v
                    +------------------+
                    | Complete Context |
                    | String (~5-10KB) |
                    +------------------+
```

## Streaming Flow: Token-by-Token Transmission

```
Bedrock                Lambda              API Gateway         Usuario
  |                      |                     |                 |
  |--start stream------->|                     |                 |
  |                      |                     |                 |
  |--token: "Hola"------>|                     |                 |
  |                      |--post: "Hola"------>|                 |
  |                      |                     |--ws: "Hola"---->|
  |                      |                     |                 | [Display: "Hola"]
  |                      |                     |                 |
  |--token: " Juan"----->|                     |                 |
  |                      |--post: "Hola Juan"->|                 |
  |                      |                     |--ws: "Hola Juan"->|
  |                      |                     |                 | [Display: "Hola Juan"]
  |                      |                     |                 |
  |--token: ","--------->|                     |                 |
  |                      |--post: "Hola Juan,"->|                |
  |                      |                     |--ws: "Hola Juan,"->|
  |                      |                     |                 | [Display: "Hola Juan,"]
  |                      |                     |                 |
  |--token: " veo"------>|                     |                 |
  |                      |--post: "Hola Juan, veo"->|            |
  |                      |                     |--ws: "Hola Juan, veo"->|
  |                      |                     |                 | [Display: "Hola Juan, veo"]
  |                      |                     |                 |
  |--[continue...]------>|                     |                 |
  |                      |                     |                 |
  |--end stream--------->|                     |                 |
  |                      |--[Save complete response to history]  |
  |                      |                     |                 |
```

## Notes on Interaction Patterns

### Synchronous Operations
- WebSocket connection establishment
- Lambda handler invocations
- DynamoDB queries and scans
- Bedrock API calls

### Asynchronous Operations
- Streaming response transmission (appears synchronous but uses async iteration)
- WebSocket message delivery (fire-and-forget after post_to_connection)

### Error Handling Patterns
- Try-catch with logging in most operations
- Return default values on error ([], empty string)
- Continue processing even if transmission fails
- No retry logic implemented

### Performance Considerations
- Full table scans on transactions and retailers (expensive)
- No caching of user data or retailers
- Context built fresh on every request
- History limited to N turns to control token usage
