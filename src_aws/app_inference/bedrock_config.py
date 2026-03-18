"""
Module: Bedrock config To manage request
"""

# ───────────────────────────────────────────── IMPORTS ─────────────────────────────────────────────
import os
import json
import boto3
from loguru import logger
from action_tools import get_available_tools, execute_tool
from identity_validator import validate_and_clean_response


# ────────────────────────────────── ENV VARIABLES + AWS RESOURCES ──────────────────────────────────
REGION_NAME = os.environ.get('REGION_NAME')
ENDPOINT_URL = os.environ.get('API_ENDPOINT')

bedrock_client = boto3.client('bedrock-runtime')
ag_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=ENDPOINT_URL)


# ──────────────────────────────────────────── METHODS ──────────────────────────────────────────────
def get_system_prompt(user_context: str) -> str:
    return f"""
Eres Comfi, el asistente digital de Comfama (Caja de Compensación Familiar de Antioquia, Colombia).

CONTEXTO DEL USUARIO:
{user_context}

🚨 REGLA ABSOLUTA - LEE ESTO PRIMERO:
Tu nombre es COMFI. Trabajas para COMFAMA en COLOMBIA. Usas PESOS COLOMBIANOS (COP).
NUNCA menciones: Carlos, México, MXN, CENTLI.
Si estás a punto de decir cualquiera de esas palabras → DETENTE INMEDIATAMENTE.

🎯 PREGUNTAS SOBRE TU IDENTIDAD - RESPONDE DIRECTAMENTE:
Si te preguntan "¿quién eres?", "¿cómo te llamas?", "¿qué eres?" → RESPONDE DIRECTAMENTE, NO USES TOOLS
Respuesta: "Soy Comfi, el asistente digital de Comfama. Estoy aquí para ayudarte con información sobre afiliación, créditos, subsidios y servicios de Comfama. ¿En qué te puedo ayudar?"

🎯 REGLA DE TOOLS - ÚSALOS INMEDIATAMENTE:
Si la pregunta es sobre Comfama (afiliación, créditos, subsidios, tarifas) → USA answer_faq SIN GENERAR TEXTO PREVIO
NO escribas "Hola", NO escribas "Entiendo", NO escribas nada → USA EL TOOL DIRECTAMENTE

CAPACIDADES:
• answer_faq: Para preguntas sobre Comfama (servicios, requisitos, procesos)
• transfer_money: Para transferencias de dinero
• purchase_product: Para compras de productos

IDENTIDAD:
• Nombre: Comfi (NO Carlos)
• Organización: Comfama (NO CENTLI)
• País: Colombia (NO México)
• Moneda: COP (NO MXN)

FLUJO CORRECTO:
Usuario: "¿Cómo me afilio?"
Tú: [USA answer_faq INMEDIATAMENTE, sin texto previo]

Usuario: "¿Quién eres?"
Tú: "Soy Comfi, el asistente digital de Comfama..." [RESPUESTA DIRECTA, sin tool]

FLUJO INCORRECTO (PROHIBIDO):
Usuario: "¿Cómo me afilio?"
Tú: "Hola Carlos..." ❌ NUNCA HAGAS ESTO

IMPORTANTE: 
• Si vas a usar un tool, NO generes ningún texto antes. Usa el tool directamente.
• Mantente SIEMPRE en rol de Comfi, asistente de Comfama
• NO menciones a Carlos, México, MXN o CENTLI
• Redirige temas no relacionados gentilmente
• Desde el PRIMER mensaje, identifícate como Comfi de Comfama (Colombia)
"""


# ──────────────────────────────────────────── METHODS ──────────────────────────────────────────────
INFO_PARAMS = {
    "maxTokens": 4000,
    "topP": 0.8,
    "temperature": 0.5  # OPTIMIZED: Reduced from 0.6 to 0.5 for faster, more direct responses
}
ADDITIONAL_MOODEL_REQUEST_FIELDS = {"top_k": 60}


def chat(model_id, user_context, user_message):
    logger.info(f"Using ConverseAPI with {model_id}")
    
    system_prompt = get_system_prompt(user_context)
    messages = [
        {
            "role": "user",
            "content": [{"text": user_message}]
        }
    ]

    try:
        response = bedrock_client.converse(
            modelId=model_id,
            messages=messages,
            system=[{"text": system_prompt}],
            inferenceConfig=INFO_PARAMS,
            additionalModelRequestFields=ADDITIONAL_MOODEL_REQUEST_FIELDS
        )
        
        return (
            response
            .get('output')
            .get('message')
            .get('content')[0]
            .get('text')
        )
    except Exception as e:
        logger.warning(f'Error generating bedrock response: {str(e)}')
        return f"Error: {str(e)}"


def transmit_response(connection_id, response_chat):
    """Transmit response to chat"""
    ag_management_client.post_to_connection(
        ConnectionId=connection_id,
        Data=response_chat
    )


def stream_chat(
        model_id: str,
        user_context: str,
        user_message: str,
        user_hist_conversation: list,
        connection_id: str
    ):
    """Sends a message to a model and streams the response with Tool Use support."""
    logger.info(f"Using ConverseStreamAPI with model {model_id}")

    system_prompt = get_system_prompt(user_context)
    user_hist_conversation.append({
        "role": "user",
        "content": [{"text": user_message}]
    })

    # Get available tools
    tools = get_available_tools()

    try:
        response = bedrock_client.converse_stream(
            modelId=model_id,
            messages=user_hist_conversation,
            system=[{"text": system_prompt}],
            inferenceConfig=INFO_PARAMS,
            additionalModelRequestFields=ADDITIONAL_MOODEL_REQUEST_FIELDS,
            toolConfig={"tools": tools}  # Enable Tool Use
        )

        text = ''
        tool_use_blocks = []
        current_tool = None
        
        for chunk in response['stream']:
            # Log chunk for debugging
            logger.debug(f"Chunk received: {chunk.keys()}")
            
            # Handle text content
            if 'contentBlockDelta' in chunk:
                delta = chunk['contentBlockDelta']['delta']
                if 'text' in delta:
                    new_chunk = delta['text']
                    text += new_chunk
                    transmit_response(
                        connection_id=connection_id,
                        response_chat=new_chunk
                    )
                elif 'toolUse' in delta:
                    # Accumulate tool use input (comes as JSON string chunks)
                    logger.info(f"Tool use delta: {delta['toolUse']}")
                    if current_tool and 'input' in delta['toolUse']:
                        # Accumulate input JSON string
                        current_tool['input'] += delta['toolUse']['input']
            
            # Handle tool use start
            elif 'contentBlockStart' in chunk:
                start = chunk['contentBlockStart'].get('start', {})
                if 'toolUse' in start:
                    logger.info(f"Tool use start: {start['toolUse']}")
                    current_tool = {
                        'toolUseId': start['toolUse']['toolUseId'],
                        'name': start['toolUse']['name'],
                        'input': ''  # Will accumulate JSON string from deltas
                    }
            
            # Handle tool use stop
            elif 'contentBlockStop' in chunk:
                if current_tool:
                    logger.info(f"Tool use stop, accumulated input: {current_tool['input']}")
                    tool_use_blocks.append(current_tool)
                    current_tool = None
            
            # Handle message stop - execute tools if needed
            elif 'messageStop' in chunk:
                if tool_use_blocks:
                    logger.info(f"Tool use requested: {len(tool_use_blocks)} tools")
                    
                    # Execute tools and get results
                    tool_results = []
                    for tool_block in tool_use_blocks:
                        tool_name = tool_block.get('name')
                        tool_input_str = tool_block.get('input', '{}')
                        tool_use_id = tool_block.get('toolUseId')
                        
                        logger.info(f"Executing tool: {tool_name}")
                        
                        # Parse input string to dict
                        try:
                            tool_input = json.loads(tool_input_str) if isinstance(tool_input_str, str) else tool_input_str
                        except:
                            tool_input = {}
                        
                        # Execute the tool
                        result = execute_tool(tool_name, tool_input)
                        
                        # Format result for Bedrock
                        tool_results.append({
                            "toolUseId": tool_use_id,
                            "content": [{"json": result}]
                        })
                    
                    # Add tool use blocks to conversation (with input as JSON object, not string)
                    tool_use_content = []
                    for tool_block in tool_use_blocks:
                        tool_input_str = tool_block.get('input', '{}')
                        try:
                            tool_input_obj = json.loads(tool_input_str) if isinstance(tool_input_str, str) else tool_input_str
                        except:
                            tool_input_obj = {}
                        
                        tool_use_content.append({
                            "toolUse": {
                                "toolUseId": tool_block.get('toolUseId'),
                                "name": tool_block.get('name'),
                                "input": tool_input_obj  # Must be JSON object, not string
                            }
                        })
                    
                    user_hist_conversation.append({
                        "role": "assistant",
                        "content": tool_use_content
                    })
                    
                    user_hist_conversation.append({
                        "role": "user",
                        "content": [
                            {"toolResult": result} for result in tool_results
                        ]
                    })
                    
                    # Get final response from model with tool results
                    logger.info("Getting final response with tool results")
                    final_response = bedrock_client.converse_stream(
                        modelId=model_id,
                        messages=user_hist_conversation,
                        system=[{"text": system_prompt}],
                        inferenceConfig=INFO_PARAMS,
                        additionalModelRequestFields=ADDITIONAL_MOODEL_REQUEST_FIELDS,
                        toolConfig={"tools": tools}
                    )
                    
                    # Stream final response
                    for final_chunk in final_response['stream']:
                        if 'contentBlockDelta' in final_chunk:
                            delta = final_chunk['contentBlockDelta']['delta']
                            if 'text' in delta:
                                new_chunk = delta['text']
                                text += new_chunk
                                transmit_response(
                                    connection_id=connection_id,
                                    response_chat=new_chunk
                                )
        
        # Validate and clean response before returning
        logger.info("Validating response identity...")
        validated_text = validate_and_clean_response(text, user_message)
        
        if validated_text != text:
            logger.warning("⚠️ Response was modified by identity validator")
            logger.info(f"Original length: {len(text)}, Cleaned length: {len(validated_text)}")
        
        return validated_text
        
    except Exception as e:
        logger.warning(
            f'Error generating streaming response from Bedrock: {str(e)}'
        )
        call_back = "Lo siento, hubo un problema procesando tu solicitud. ¿Puedes intentarlo nuevamente?"
        transmit_response(
            connection_id=connection_id,
            response_chat=call_back
        )
        return call_back