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
        amount: Amount to transfer in MXN
        recipient_name: Name of recipient
        concept: Transfer concept/description
        
    Returns:
        dict: Transfer result with transaction ID and status
    """
    try:
        logger.info(f"Executing transfer: ${amount} MXN to {recipient_name}")
        
        # Simulate security validation
        if amount <= 0:
            return {
                "success": False,
                "error": "El monto debe ser mayor a cero"
            }
        
        if amount > 50000:
            return {
                "success": False,
                "error": "El monto excede el límite diario de $50,000 MXN"
            }
        
        # Generate transaction ID
        transaction_id = f"TRF-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Simulate successful transfer
        result = {
            "success": True,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": "MXN",
            "recipient": recipient_name,
            "concept": concept or "Transferencia",
            "timestamp": timestamp,
            "status": "completed",
            "message": f"✅ Transferencia exitosa de ${amount:,.2f} MXN a {recipient_name}"
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
                "error": "El monto excede el límite de compra de $100,000 MXN"
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
            "currency": "MXN",
            "timestamp": timestamp,
            "status": "confirmed",
            "delivery": "2-3 días hábiles",
            "message": f"✅ Compra exitosa: {quantity}x {product['name']} por ${total:,.2f} MXN"
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
                                "description": "Monto a transferir en pesos mexicanos (MXN)"
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
    else:
        return {
            "success": False,
            "error": f"Tool '{tool_name}' not found"
        }
