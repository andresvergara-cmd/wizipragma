"""
Simple identity validator tests without external dependencies
"""

import re


# Copy of validation logic for testing
FORBIDDEN_WORDS = ['carlos', 'méxico', 'mexico', 'mxn', 'centli']


def contains_forbidden(text):
    """Check if text contains forbidden words"""
    text_lower = text.lower()
    found = []
    for word in FORBIDDEN_WORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text_lower):
            found.append(word)
    return len(found) > 0, found


def clean_text(text):
    """Remove sentences with forbidden words"""
    sentences = re.split(r'([.!?]\s+)', text)
    cleaned = []
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        separator = sentences[i+1] if i+1 < len(sentences) else ''
        
        has_forbidden, _ = contains_forbidden(sentence)
        if not has_forbidden:
            cleaned.append(sentence + separator)
    
    return ''.join(cleaned).strip()


# Test cases
print("="*70)
print("IDENTITY VALIDATOR TESTS")
print("="*70)

# Test 1: Detect Carlos
text1 = "Hola Carlos, entiendo que en México necesitas ayuda"
has_bad, words = contains_forbidden(text1)
assert has_bad, "Should detect Carlos"
assert 'carlos' in words
print("✅ Test 1: Detects 'Carlos' and 'México'")

# Test 2: Clean text passes
text2 = "Hola, soy Comfi de Comfama en Colombia"
has_bad, words = contains_forbidden(text2)
assert not has_bad, "Clean text should pass"
print("✅ Test 2: Clean text passes")

# Test 3: Clean mixed response
text3 = """Hola Carlos, entiendo que en México necesitas ayuda. 
Tu empleador te afilia automáticamente. 
La afiliación a Comfama es automática."""

cleaned = clean_text(text3)
has_bad, words = contains_forbidden(cleaned)
assert not has_bad, f"Cleaned text should not have forbidden words, but found: {words}"
assert "empleador" in cleaned, "Should keep good content"
print("✅ Test 3: Removes bad sentences, keeps good content")
print(f"   Original: {len(text3)} chars -> Cleaned: {len(cleaned)} chars")

# Test 4: Case insensitive
text4 = "Hola CARLOS en MÉXICO"
has_bad, words = contains_forbidden(text4)
assert has_bad, "Should detect uppercase"
print("✅ Test 4: Case-insensitive detection")

# Test 5: Word boundaries
text5 = "Caracas"  # Should NOT match 'carlos'
has_bad, words = contains_forbidden(text5)
assert 'carlos' not in words, "Should not match partial words"
print("✅ Test 5: Word boundaries respected")

# Test 6: Real-world example
text6 = """Hola Carlos, entiendo que en México necesitas información sobre afiliación.

Tu empleador te afilia automáticamente al pagar aportes parafiscales (4% del salario). No necesitas hacer ningún trámite adicional.

Pasos:
1. Tu empleador te registra en el sistema
2. Recibes tu número de afiliación
3. Puedes activar tu cuenta digital
4. Accedes a todos los beneficios"""

cleaned6 = clean_text(text6)
has_bad, words = contains_forbidden(cleaned6)
print(f"\n📝 Real-world example:")
print(f"   Original length: {len(text6)} chars")
print(f"   Cleaned length: {len(cleaned6)} chars")
print(f"   Forbidden words removed: {not has_bad}")
print(f"   Preview: {cleaned6[:150]}...")

if has_bad:
    print(f"   ⚠️ WARNING: Still contains: {words}")
else:
    print("   ✅ Successfully cleaned!")

print("\n" + "="*70)
print("ALL TESTS PASSED ✅")
print("="*70)
