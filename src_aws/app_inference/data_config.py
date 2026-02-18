"""
Module: Config definitions for data context
"""

# ───────────────────────────────────────────── IMPORTS ─────────────────────────────────────────────
import os
import calendar
from decimal import Decimal
from datetime import datetime
from collections import defaultdict
import boto3
from loguru import logger
from boto3.dynamodb.conditions import Key


# ────────────────────────────────── ENV VARIABLES + AWS RESOURCES ──────────────────────────────────
REGION_NAME = os.environ.get('REGION_NAME')
dynamodb_client = boto3.resource('dynamodb', region_name=REGION_NAME)


# ──────────────────────────────────────────── METHODS ──────────────────────────────────────────────
def get_user_data(table, primary_key, primary_value: str) -> list:
    """
    Query user data from DynamoDB based on primary key value.
        
    Returns:
        list: User data record or empty list if not found/error
    """
    try:
        response = table.query(
            KeyConditionExpression=Key(primary_key).eq(str(primary_value)),
            Limit=1
        )
        print(response)

        item_list = response.get('Items')[0]
        logger.info(f'Items recovered: {len(item_list)}')

        return item_list
    except Exception as e:
        logger.warning(
            f"Error retrieving primary key: {primary_key}. Error: {str(e)}"
        )
        return []


def scan_table(table) -> list:
    """
    Scan complete DynamoDB table with pagination handling.

    Returns:
        list: Complete list of all table items
    """
    try:
        items_list = []
        response = table.scan()
        items_list.extend(response['Items'])

        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey']
            )

            items_list.extend(response['Items'])

        logger.info(f'Items Number: {len(items_list)}')

        return items_list
    except Exception as e:
        logger.warning(f'Error scanning {table} table. Error: {str(e)}')
        return []


def format_user_context(user: dict) -> str:
    """
    Format comprehensive user profile data into structured text context.

    Returns:
        str: Formatted multi-section user profile text
    """
    # Handle empty or invalid user data
    if not user or not isinstance(user, dict):
        return "─────────────────────── PERFIL DEL USUARIO ───────────────────────\nNo hay información de perfil disponible."
    
    blocks = []

    blocks.append("─────────────────────── PERFIL DEL USUARIO ───────────────────────")
    name = f"{user.get('firstName', '')} {user.get('lastName', '')}".strip()
    blocks.append(f"Nombre: {name}")
    blocks.append(f"ID: {user.get('userId', 'N/A')}")
    if user.get('email'):
        blocks.append(f"Correo: {user['email']}")
    if 'personalInfo' in user:
        pi = user['personalInfo']
        if pi.get('location'):
            blocks.append(f"Ubicación: {pi['location']}")
        if pi.get('occupation'):
            blocks.append(f"Ocupación: {pi['occupation']}")
        if pi.get('birthDate'):
            blocks.append(f"Fecha de nacimiento: {pi['birthDate']}")
        estado = pi.get('maritalStatus', 'N/A')
        hijos = int(pi.get('children', 0))
        blocks.append(f"Estado civil: {estado}, hijos: {hijos}")

    blocks.append("\n───────────────────── INFORMACIÓN FINANCIERA ─────────────────────")
    
    # Financial Profile (nuevo formato)
    fin_profile = user.get('financialProfile', {})
    if fin_profile:
        monthly_income = float(fin_profile.get('monthlyIncome', 0))
        currency = fin_profile.get('currency', 'MXN')
        blocks.append(f"Ingreso mensual: {currency} ${monthly_income:,.2f}")
        if fin_profile.get('savingsGoal'):
            savings_goal = float(fin_profile.get('savingsGoal', 0))
            blocks.append(f"Meta de ahorro: {currency} ${savings_goal:,.2f}")
        if fin_profile.get('riskTolerance'):
            blocks.append(f"Tolerancia al riesgo: {fin_profile['riskTolerance']}")
    
    # Financial Info (formato antiguo - fallback)
    fin = user.get('financialInfo', {})
    if fin and not fin_profile:
        blocks.append(f"Ingreso anual: USD {int(fin.get('incomeAnnual', 0))}")
        blocks.append(f"Puntaje crediticio: {int(fin.get('creditScore', 0))}")
        blocks.append(f"Tiene hipoteca: {'Sí' if fin.get('hasMortgage') else 'No'}")

    credit = user.get('creditLine', {})
    blocks.append(f"Límite de crédito: USD {int(credit.get('limit', 0))}")
    blocks.append(f"Crédito disponible: USD {int(credit.get('available', 0))}")
    blocks.append(f"Crédito aprobado: {'Sí' if credit.get('isApproved') else 'No'}")

    # CUENTAS BANCARIAS
    accounts = user.get('accounts', [])
    if accounts:
        blocks.append("\n─────────────────────── CUENTAS BANCARIAS ────────────────────────")
        total_balance = 0
        for acc in accounts:
            acc_type = acc.get('accountType', 'N/A')
            bank = acc.get('bankName', 'N/A')
            balance = float(acc.get('balance', 0))
            currency = acc.get('currency', 'MXN')
            total_balance += balance
            blocks.append(f"• {acc_type} ({bank}): {currency} ${balance:,.2f}")
        blocks.append(f"SALDO TOTAL: MXN ${total_balance:,.2f}")

    imp = user.get('importantDates', {})
    if imp:
        blocks.append("\n─────────────────────── FECHAS IMPORTANTES ───────────────────────")
        if imp.get('anniversary'):
            blocks.append(f"Aniversario: {imp['anniversary']}")
        if imp.get('creditCardDueDate'):
            blocks.append(f"Pago tarjeta: {imp['creditCardDueDate']}")
        if imp.get('mortgageDueDate'):
            blocks.append(f"Pago hipoteca: {imp['mortgageDueDate']}")
        if imp.get('childrenBirthdays'):
            fechas_hijos = ", ".join(imp['childrenBirthdays'])
            blocks.append(f"Cumpleaños hijos: {fechas_hijos}")

    habits = user.get('habits', {})
    prefs = user.get('preferences', {})
    if habits or prefs:
        blocks.append("\n───────────────────── HÁBITOS Y PREFERENCIAS ─────────────────────")
        if habits.get('preferredPaymentMethod'):
            blocks.append(f"Método de pago preferido: {habits['preferredPaymentMethod']}")
        if habits.get('savingsRate') is not None:
            blocks.append(f"Tasa de ahorro: {float(habits['savingsRate'])*100:.0f}%")
        if habits.get('investmentStyle'):
            blocks.append(f"Estilo de inversión: {habits['investmentStyle']}")
        if habits.get('spendingFrequency'):
            blocks.append(f"Frecuencia de gasto: {habits['spendingFrequency']}")
        if habits.get('shoppingHabits'):
            blocks.append(f"Hábitos de compra: {', '.join(habits['shoppingHabits'])}")

        if prefs.get('communicationChannel'):
            blocks.append(f"Canal de comunicación: {prefs['communicationChannel']}")
        if prefs.get('language'):
            blocks.append(f"Idioma: {prefs['language']}")
        if prefs.get('notificationFrequency'):
            blocks.append(f"Frecuencia de notificación: {prefs['notificationFrequency']}")
        if prefs.get('timezone'):
            blocks.append(f"Zona horaria: {prefs['timezone']}")

    goals = user.get('goals', {})
    if goals:
        blocks.append("\n──────────────────────── METAS FINANCIERAS ───────────────────────")
        if goals.get('shortTerm'):
            blocks.append(f"Corto plazo: {', '.join(goals['shortTerm'])}")
        if goals.get('mediumTerm'):
            blocks.append(f"Mediano plazo: {', '.join(goals['mediumTerm'])}")
        if goals.get('longTerm'):
            blocks.append(f"Largo plazo: {', '.join(goals['longTerm'])}")
        if goals.get('targetSavings'):
            blocks.append(f"Meta de ahorro: USD {int(goals['targetSavings'])}")

    return "\n".join(blocks)


def summarize_transactions(transactions, user_id: str, last_transactions: int = 10):
    """    
    Processes user transactions to create monthly spending summaries by category
    and identifies recent transaction patterns for financial context analysis.

    Returns:
        tuple:
            Summary includes monthly totals by category and recent transaction details
    """
    filtered = [t for t in transactions if t['userId'] == user_id]
    
    # OPTIMIZATION: Sort by date and limit to last 50 transactions
    filtered.sort(key=lambda x: x.get('date', ''), reverse=True)
    filtered = filtered[:50]
    logger.info(f"Processing {len(filtered)} most recent transactions (optimized from full set)")

    monthly_summary = defaultdict(lambda: defaultdict(Decimal))
    unique_categories = set()
    recent_tx = []

    for tx in filtered:
        dt = datetime.fromisoformat(tx['date'].replace("Z", "+00:00"))
        year = dt.year
        month_num = dt.month
        month_name = calendar.month_name[month_num]
        month_key = f"{year}-{month_name}"

        monthly_summary[(year, month_num, month_key)][tx['industry']] += tx['amount']
        unique_categories.add(tx['industry'])
        recent_tx.append((dt, tx['industry'], tx['amount']))


    sorted_months = sorted(monthly_summary.keys())
    summary_lines = ["──────────────────────── RESUMEN DE GASTOS ───────────────────────"]
    for y, m, month_key in sorted_months:  # ✅ aquí usamos y, m del bucle actual
        cats = monthly_summary[(y, m, month_key)]
        total = sum(cats.values())
        cat_str = ", ".join([f"{k}: USD {float(v):.2f}" for k, v in cats.items()])
        summary_lines.append(f"• {month_key}: USD {float(total):.2f} ({cat_str})")

    recent_tx.sort(key=lambda x: x[0], reverse=True)
    recent_lines = [f"\n──────────────────── ÚLTIMAS {last_transactions} TRANSACCIONES ────────────────────"]
    for dt, ind, amt in recent_tx[:last_transactions]:
        recent_lines.append(f"• {dt.date()} | {ind}: USD {float(amt):.2f}")

    return "\n".join(summary_lines + recent_lines), unique_categories


def format_retailer_context_pairs(retailers: list, retailers_in_tx: list):
    """
    Format relevant retailer benefits based on user transaction categories.
    
    Filters retailers by transaction categories and formats benefit information
    in paired display for efficient context presentation.
        
    Returns:
        str: Formatted retailer benefits grouped by industry with paired display
    """
    relevant = [r for r in retailers if r.get("industry") in retailers_in_tx]
    
    grouped = {}
    for r in relevant:
        industry = r.get("industry", "Otros")
        benefits = r.get("benefits", [])
        benefits_text = "; ".join(b.get("description", "") for b in benefits[:2])
        
        if industry not in grouped:
            grouped[industry] = []
        grouped[industry].append(f"{r.get('name')}: {benefits_text}")
    
    result = ["──────────────────── Retailers y Beneficios Relevantes ────────────────────"]
    for industry, items in grouped.items():
        result.append(f"\nIndustria: {industry}")
        for i in range(0, len(items), 2):
            pair = " || ".join(items[i:i+2])
            result.append(f"- {pair}")
    
    return "\n".join(result)


def get_user_context(table_names, user_id: str, last_txn: int = 10):
    """
    Generate comprehensive user context by combining profile, transactions, and retailer data.

    Returns:
        str: Complete formatted user context combining all data sources
    """
    user_table = dynamodb_client.Table(table_names.get('profile'))
    user_data = get_user_data(user_table, 'userId', user_id)
    user_profile = format_user_context(user_data)

    txn_table = dynamodb_client.Table(table_names.get('transactions'))
    txn_user = scan_table(txn_table)
    summarize_txn, uniq_categories = summarize_transactions(txn_user, user_id, last_txn)

    ret_table = dynamodb_client.Table(table_names.get('retailers'))
    retailers = scan_table(ret_table)
    retailers_data = format_retailer_context_pairs(retailers, list(uniq_categories))

    context = "\n\n\n".join([user_profile, summarize_txn, retailers_data])

    return context
