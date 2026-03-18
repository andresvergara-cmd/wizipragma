#!/usr/bin/env python3
"""
Test script for FAQ backend functionality
Tests the answer_faq function without requiring AWS dependencies
"""

# FAQ Database (copy from action_tools.py)
FAQ_DATABASE = {
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
• Hasta 5 años plazo''',
        'tags': ['crédito', 'préstamo', 'financiación', 'tipos', 'opciones', 'que creditos hay']
    }
}

def answer_faq(question: str) -> dict:
    """Test version of answer_faq"""
    question_lower = question.lower()
    
    best_match = None
    best_score = 0
    
    for faq_id, faq in FAQ_DATABASE.items():
        score = 0
        
        if any(keyword in question_lower for keyword in faq['tags']):
            score += 1
        
        faq_question_lower = faq['question'].lower()
        common_words = set(question_lower.split()) & set(faq_question_lower.split())
        score += len(common_words) * 0.5
        
        if score > best_score:
            best_score = score
            best_match = faq
    
    if best_match and best_score > 0.5:
        return {
            "success": True,
            "faq_id": best_match['id'],
            "question": best_match['question'],
            "shortAnswer": best_match['shortAnswer'],
            "confidence": min(best_score / 3.0, 1.0)
        }
    else:
        return {
            "success": False,
            "error": "No encontré una respuesta específica"
        }

# Run tests
if __name__ == "__main__":
    import json
    
    tests = [
        "¿Cómo me afilio a Comfama?",
        "¿Qué créditos ofrecen?",
        "como me registro",
        "tipos de prestamos",
        "¿Cuál es el clima hoy?"
    ]
    
    print("🧪 Testing FAQ Backend\n")
    print("=" * 60)
    
    for i, test_question in enumerate(tests, 1):
        print(f"\n📝 Test {i}: {test_question}")
        print("-" * 60)
        result = answer_faq(test_question)
        
        if result['success']:
            print(f"✅ Match encontrado!")
            print(f"   FAQ ID: {result['faq_id']}")
            print(f"   Pregunta: {result['question']}")
            print(f"   Confianza: {result['confidence']:.2%}")
            print(f"   Respuesta: {result['shortAnswer'][:80]}...")
        else:
            print(f"❌ No match")
            print(f"   Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("✅ Tests completados!")
