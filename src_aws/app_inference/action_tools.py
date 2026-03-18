"""
Module: Action Tools for CENTLI Agent
Implements executable actions: transfers, purchases, etc.
"""

import json
import uuid
from datetime import datetime
from loguru import logger


def transfer_money(amount: float, recipient_name: str, concept: str = "") -> dict:
    """
    Execute a money transfer
    
    Args:
        amount: Amount to transfer in COP
        recipient_name: Name of recipient
        concept: Transfer concept/description
        
    Returns:
        dict: Transfer result with transaction ID and status
    """
    try:
        logger.info(f"Executing transfer: ${amount} COP to {recipient_name}")
        
        # Simulate security validation
        if amount <= 0:
            return {
                "success": False,
                "error": "El monto debe ser mayor a cero"
            }
        
        if amount > 50000:
            return {
                "success": False,
                "error": "El monto excede el límite diario de $50,000 COP"
            }
        
        # Generate transaction ID
        transaction_id = f"TRF-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Simulate successful transfer
        result = {
            "success": True,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": "COP",
            "recipient": recipient_name,
            "concept": concept or "Transferencia",
            "timestamp": timestamp,
            "status": "completed",
            "message": f"✅ Transferencia exitosa de ${amount:,.2f} COP a {recipient_name}"
        }
        
        logger.info(f"Transfer completed: {transaction_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error in transfer: {str(e)}")
        return {
            "success": False,
            "error": f"Error procesando transferencia: {str(e)}"
        }


def purchase_product(product_name: str, quantity: int = 1) -> dict:
    """
    Execute a product purchase
    
    Args:
        product_name: Name of product to purchase
        quantity: Quantity to purchase
        
    Returns:
        dict: Purchase result with order ID and details
    """
    try:
        logger.info(f"Executing purchase: {quantity}x {product_name}")
        
        # Simulate product catalog with prices
        product_catalog = {
            "iphone 15 pro": {"price": 25999, "name": "iPhone 15 Pro 256GB"},
            "iphone 15": {"price": 21999, "name": "iPhone 15 128GB"},
            "iphone": {"price": 21999, "name": "iPhone 15 128GB"},
            "macbook": {"price": 35999, "name": "MacBook Air M3"},
            "airpods": {"price": 5499, "name": "AirPods Pro 2"},
            "ipad": {"price": 15999, "name": "iPad Air"},
            "apple watch": {"price": 12999, "name": "Apple Watch Series 9"},
        }
        
        # Find product
        product_key = product_name.lower()
        product = None
        
        for key, value in product_catalog.items():
            if key in product_key:
                product = value
                break
        
        if not product:
            return {
                "success": False,
                "error": f"Producto '{product_name}' no encontrado en el catálogo"
            }
        
        # Calculate total
        total = product["price"] * quantity
        
        # Simulate security validation
        if total > 100000:
            return {
                "success": False,
                "error": "El monto excede el límite de compra de $100,000 COP"
            }
        
        # Generate order ID
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Simulate successful purchase
        result = {
            "success": True,
            "order_id": order_id,
            "product": product["name"],
            "quantity": quantity,
            "unit_price": product["price"],
            "total": total,
            "currency": "COP",
            "timestamp": timestamp,
            "status": "confirmed",
            "delivery": "2-3 días hábiles",
            "message": f"✅ Compra exitosa: {quantity}x {product['name']} por ${total:,.2f} COP"
        }
        
        logger.info(f"Purchase completed: {order_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error in purchase: {str(e)}")
        return {
            "success": False,
            "error": f"Error procesando compra: {str(e)}"
        }


def get_available_tools():
    """
    Get tool definitions for Bedrock Tool Use
    
    Returns:
        list: Tool specifications for Bedrock
    """
    return [
        {
            "toolSpec": {
                "name": "transfer_money",
                "description": "Ejecuta una transferencia de dinero. Úsala cuando el usuario solicite enviar dinero, hacer una transferencia, o pagar a alguien.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "amount": {
                                "type": "number",
                                "description": "Monto a transferir en pesos colombianos (COP)"
                            },
                            "recipient_name": {
                                "type": "string",
                                "description": "Nombre del destinatario (ej: 'mamá', 'Juan Pérez', 'hermano')"
                            },
                            "concept": {
                                "type": "string",
                                "description": "Concepto o descripción de la transferencia (opcional)"
                            }
                        },
                        "required": ["amount", "recipient_name"]
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "purchase_product",
                "description": "Ejecuta la compra de un producto. Úsala cuando el usuario quiera comprar algo.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "Nombre del producto a comprar (ej: 'iPhone 15 Pro', 'MacBook', 'AirPods')"
                            },
                            "quantity": {
                                "type": "integer",
                                "description": "Cantidad a comprar (default: 1)"
                            }
                        },
                        "required": ["product_name"]
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "answer_faq",
                "description": "Responde preguntas frecuentes sobre Comfama: afiliación, créditos, subsidios, servicios. Úsala cuando el usuario haga preguntas sobre cómo funciona Comfama, requisitos, procesos, etc.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "Pregunta del usuario sobre Comfama (ej: '¿Cómo me afilio?', '¿Qué créditos ofrecen?', '¿Qué subsidios hay?')"
                            }
                        },
                        "required": ["question"]
                    }
                }
            }
        }
    ]


def execute_tool(tool_name: str, tool_input: dict) -> dict:
    """
    Execute a tool by name
    
    Args:
        tool_name: Name of tool to execute
        tool_input: Input parameters for the tool
        
    Returns:
        dict: Tool execution result
    """
    logger.info(f"Executing tool: {tool_name} with input: {tool_input}")
    
    if tool_name == "transfer_money":
        return transfer_money(**tool_input)
    elif tool_name == "purchase_product":
        return purchase_product(**tool_input)
    elif tool_name == "answer_faq":
        return answer_faq(**tool_input)
    else:
        return {
            "success": False,
            "error": f"Tool '{tool_name}' not found"
        }


# ============================================
# FAQ DATABASE
# ============================================

FAQ_DATABASE = {
    'faq-identidad-001': {
        'id': 'faq-identidad-001',
        'category': 'identidad',
        'question': '¿Quién eres?',
        'shortAnswer': 'Soy Comfi, el asistente digital de Comfama.',
        'detailedAnswer': '''Soy Comfi, el asistente digital de Comfama (Caja de Compensación Familiar de Antioquia, Colombia).

Estoy aquí para ayudarte con:
• Información sobre afiliación
• Consultas sobre créditos
• Detalles de subsidios
• Servicios de Comfama
• Transferencias y compras

¿En qué te puedo ayudar hoy?''',
        'tags': ['quien eres', 'que eres', 'como te llamas', 'tu nombre', 'identidad', 'presentate']
    },
    'faq-identidad-002': {
        'id': 'faq-identidad-002',
        'category': 'identidad',
        'question': '¿Qué es Comfama?',
        'shortAnswer': 'Comfama es la Caja de Compensación Familiar de Antioquia, Colombia.',
        'detailedAnswer': '''Comfama es la Caja de Compensación Familiar de Antioquia, una entidad sin ánimo de lucro que brinda servicios de bienestar social a trabajadores y sus familias en Colombia.

Servicios principales:
🏠 Subsidio de vivienda
💰 Créditos (vivienda, educación, libre inversión)
📚 Programas educativos
🏥 Servicios de salud
🎉 Recreación y turismo
👨‍👩‍👧‍👦 Programas familiares

Comfama opera en Antioquia y atiende a miles de familias colombianas.''',
        'tags': ['que es comfama', 'comfama', 'caja de compensacion', 'antioquia', 'colombia']
    },
    'faq-afiliacion-001': {
        'id': 'faq-afiliacion-001',
        'category': 'afiliacion',
        'question': '¿Cómo me afilio a Comfama?',
        'shortAnswer': 'Tu empleador te afilia automáticamente al pagar aportes parafiscales.',
        'detailedAnswer': '''La afiliación a Comfama es automática cuando tu empleador realiza los aportes parafiscales (4% del salario). No necesitas hacer ningún trámite adicional.

Pasos:
1. Tu empleador te registra en el sistema
2. Recibes tu número de afiliación
3. Puedes activar tu cuenta digital
4. Accedes a todos los beneficios''',
        'tags': ['afiliación', 'registro', 'empleador', 'alta', 'inscripción', 'como afiliarme']
    },
    'faq-afiliacion-002': {
        'id': 'faq-afiliacion-002',
        'category': 'afiliacion',
        'question': '¿Cuál es mi tarifa de afiliación?',
        'shortAnswer': 'Tu tarifa depende de tu salario. Es el 4% que aporta tu empleador.',
        'detailedAnswer': '''La tarifa de afiliación es el 4% de tu salario mensual, que aporta tu empleador directamente. Tú no pagas nada de tu bolsillo.

Ejemplo:
• Salario: $2,000,000 COP
• Aporte mensual: $80,000 COP (4%)
• Pagado por: Tu empleador

Este aporte te da acceso a todos los servicios de Comfama.''',
        'tags': ['tarifa', 'aporte', 'salario', 'costo', 'cuota', 'cuanto pago']
    },
    'faq-creditos-001': {
        'id': 'faq-creditos-001',
        'category': 'creditos',
        'question': '¿Qué tipos de créditos ofrece Comfama?',
        'shortAnswer': 'Ofrecemos créditos de vivienda, educación, libre inversión y vehículo.',
        'detailedAnswer': '''Comfama ofrece diferentes líneas de crédito para apoyar tu bienestar:

🏠 Crédito de Vivienda
• Compra de vivienda nueva o usada
• Mejoramiento de vivienda
• Tasas preferenciales
• Hasta 20 años plazo

📚 Crédito de Educación
• Pregrado y posgrado
• Cursos y diplomados
• Sin codeudor
• Hasta 5 años plazo

💰 Crédito de Libre Inversión
• Para cualquier necesidad
• Aprobación rápida
• Hasta 4 años plazo
• Tasas competitivas

🚗 Crédito de Vehículo
• Compra de vehículo nuevo o usado
• Hasta 5 años plazo
• Tasas preferenciales''',
        'tags': ['crédito', 'préstamo', 'financiación', 'tipos', 'opciones', 'que creditos hay']
    },
    'faq-creditos-002': {
        'id': 'faq-creditos-002',
        'category': 'creditos',
        'question': '¿Qué requisitos necesito para solicitar un crédito?',
        'shortAnswer': 'Ser afiliado activo, tener capacidad de pago y presentar documentación.',
        'detailedAnswer': '''Los requisitos varían según el tipo de crédito, pero en general necesitas:

Requisitos Generales:
✅ Ser afiliado activo de Comfama
✅ Tener al menos 6 meses de afiliación
✅ Capacidad de pago demostrable
✅ No tener créditos en mora

Documentación:
📄 Cédula de ciudadanía
📄 Certificado laboral (no mayor a 30 días)
📄 Últimos 3 desprendibles de pago
📄 Extractos bancarios (últimos 3 meses)

Requisitos Específicos por Tipo:
🏠 Vivienda: Promesa de compraventa, avalúo
📚 Educación: Carta de admisión, costos
🚗 Vehículo: Cotización del vehículo''',
        'tags': ['requisitos', 'documentos', 'elegibilidad', 'que necesito', 'solicitar credito']
    },
    'faq-subsidios-001': {
        'id': 'faq-subsidios-001',
        'category': 'subsidios',
        'question': '¿Qué subsidios ofrece Comfama?',
        'shortAnswer': 'Ofrecemos subsidios de vivienda, educación, salud y recreación.',
        'detailedAnswer': '''Comfama ofrece diversos subsidios para mejorar tu calidad de vida:

🏠 Subsidio de Vivienda
• Compra de vivienda VIS
• Mejoramiento de vivienda
• Hasta $30 millones
• Según nivel de ingresos

📚 Subsidio de Educación
• Útiles escolares
• Uniformes
• Matrículas
• Cursos y capacitaciones

🏥 Subsidio de Salud
• Medicamentos
• Exámenes médicos
• Tratamientos especiales
• Según necesidad

🎉 Subsidio de Recreación
• Vacaciones recreativas
• Eventos culturales
• Actividades deportivas
• Para toda la familia

Nota: Los subsidios dependen de tu nivel de ingresos y composición familiar.''',
        'tags': ['subsidios', 'beneficios', 'ayudas', 'que subsidios hay']
    }
}


def answer_faq(question: str) -> dict:
    """
    Answer frequently asked questions
    
    Args:
        question: User's question
        
    Returns:
        dict: FAQ answer with details
    """
    try:
        logger.info(f"Searching FAQ for: {question}")
        
        # Simple keyword matching (can be improved with semantic search)
        question_lower = question.lower()
        
        # Find best matching FAQ
        best_match = None
        best_score = 0
        
        for faq_id, faq in FAQ_DATABASE.items():
            score = 0
            
            # Check if question matches
            if any(keyword in question_lower for keyword in faq['tags']):
                score += 1
            
            # Check if question text is similar
            faq_question_lower = faq['question'].lower()
            common_words = set(question_lower.split()) & set(faq_question_lower.split())
            score += len(common_words) * 0.5
            
            if score > best_score:
                best_score = score
                best_match = faq
        
        if best_match and best_score > 0.5:
            result = {
                "success": True,
                "faq_id": best_match['id'],
                "category": best_match['category'],
                "question": best_match['question'],
                "shortAnswer": best_match['shortAnswer'],
                "detailedAnswer": best_match['detailedAnswer'],
                "confidence": min(best_score / 3.0, 1.0),  # Normalize score
                "message": f"✅ Encontré información sobre: {best_match['question']}"
            }
            
            logger.info(f"FAQ match found: {best_match['id']} (score: {best_score})")
            return result
        else:
            return {
                "success": False,
                "error": "No encontré una respuesta específica a tu pregunta. ¿Puedes reformularla o ser más específico?",
                "suggestions": [
                    "¿Cómo me afilio a Comfama?",
                    "¿Qué tipos de créditos ofrecen?",
                    "¿Qué subsidios están disponibles?"
                ]
            }
        
    except Exception as e:
        logger.error(f"Error in answer_faq: {str(e)}")
        return {
            "success": False,
            "error": f"Error buscando respuesta: {str(e)}"
        }

