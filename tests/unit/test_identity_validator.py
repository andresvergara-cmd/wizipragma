"""
Unit tests for identity_validator module
"""

import sys
import os

# Add src_aws/app_inference to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src_aws/app_inference'))

from identity_validator import (
    contains_forbidden_identity,
    validate_response,
    clean_response,
    get_fallback_response,
    validate_and_clean_response
)


def test_contains_forbidden_identity_carlos():
    """Test detection of 'Carlos' in text"""
    text = "Hola Carlos, entiendo que en México necesitas ayuda"
    has_forbidden, words = contains_forbidden_identity(text)
    
    assert has_forbidden == True
    assert 'carlos' in words
    assert 'méxico' in words or 'mexico' in words
    print("✅ Test passed: Detects 'Carlos' and 'México'")


def test_contains_forbidden_identity_clean():
    """Test that clean text passes"""
    text = "Hola, soy Comfi de Comfama en Colombia"
    has_forbidden, words = contains_forbidden_identity(text)
    
    assert has_forbidden == False
    assert len(words) == 0
    print("✅ Test passed: Clean text has no forbidden words")


def test_validate_response_invalid():
    """Test validation of invalid response"""
    response = "Hola Carlos, entiendo que en México necesitas información sobre créditos"
    result = validate_response(response)
    
    assert result["valid"] == False
    assert len(result["forbidden_words"]) > 0
    print(f"✅ Test passed: Invalid response detected with words: {result['forbidden_words']}")


def test_validate_response_valid():
    """Test validation of valid response"""
    response = "Hola, soy Comfi de Comfama. ¿En qué puedo ayudarte hoy?"
    result = validate_response(response)
    
    assert result["valid"] == True
    print("✅ Test passed: Valid response accepted")


def test_clean_response_removes_bad_sentences():
    """Test that cleaning removes sentences with forbidden words"""
    response = """Hola Carlos, entiendo que en México necesitas ayuda. 
    Tu empleador te afilia automáticamente al pagar aportes parafiscales. 
    La afiliación a Comfama es automática."""
    
    cleaned = clean_response(response)
    
    # Should not contain Carlos or México
    has_forbidden, words = contains_forbidden_identity(cleaned)
    assert has_forbidden == False
    
    # Should still contain the good parts
    assert "empleador" in cleaned
    assert "Comfama" in cleaned
    
    print("✅ Test passed: Bad sentences removed, good content preserved")
    print(f"   Original: {len(response)} chars")
    print(f"   Cleaned: {len(cleaned)} chars")


def test_get_fallback_response():
    """Test fallback response generation"""
    question = "¿Cómo me afilio?"
    fallback = get_fallback_response(question)
    
    assert "Comfi" in fallback
    assert "Comfama" in fallback
    assert "Colombia" in fallback
    assert question in fallback
    
    # Should not contain forbidden words
    has_forbidden, _ = contains_forbidden_identity(fallback)
    assert has_forbidden == False
    
    print("✅ Test passed: Fallback response is clean and helpful")


def test_validate_and_clean_response_mixed():
    """Test full validation and cleaning of mixed response"""
    response = """Hola Carlos, entiendo que en México necesitas información. 
    Tu empleador te afilia automáticamente al pagar aportes parafiscales (4% del salario). 
    No necesitas hacer ningún trámite adicional.
    
    Pasos:
    1. Tu empleador te registra en el sistema
    2. Recibes tu número de afiliación
    3. Puedes activar tu cuenta digital
    4. Accedes a todos los beneficios"""
    
    question = "¿Cómo me afilio a Comfama?"
    cleaned = validate_and_clean_response(response, question)
    
    # Should not contain forbidden words
    has_forbidden, words = contains_forbidden_identity(cleaned)
    assert has_forbidden == False, f"Cleaned response still has forbidden words: {words}"
    
    # Should contain useful information
    assert "empleador" in cleaned or "Comfi" in cleaned
    
    print("✅ Test passed: Mixed response cleaned successfully")
    print(f"   Original length: {len(response)}")
    print(f"   Cleaned length: {len(cleaned)}")
    print(f"   Preview: {cleaned[:150]}...")


def test_validate_and_clean_response_all_bad():
    """Test that completely bad response gets fallback"""
    response = "Hola Carlos, soy tu asistente en México. Uso MXN para las transacciones."
    question = "¿Cuál es mi saldo?"
    
    cleaned = validate_and_clean_response(response, question)
    
    # Should not contain forbidden words
    has_forbidden, words = contains_forbidden_identity(cleaned)
    assert has_forbidden == False, f"Fallback still has forbidden words: {words}"
    
    # Should be a fallback response
    assert "Comfi" in cleaned
    assert "Comfama" in cleaned
    
    print("✅ Test passed: Completely bad response replaced with fallback")


def test_case_insensitive():
    """Test that detection is case-insensitive"""
    texts = [
        "Hola CARLOS",
        "En MÉXICO",
        "Uso MXN",
        "Soy Carlos",
        "méxico y carlos"
    ]
    
    for text in texts:
        has_forbidden, words = contains_forbidden_identity(text)
        assert has_forbidden == True, f"Failed to detect in: {text}"
    
    print("✅ Test passed: Case-insensitive detection works")


def test_word_boundaries():
    """Test that word boundaries are respected"""
    # These should NOT trigger (partial matches)
    safe_texts = [
        "Caracas",  # Contains 'cara' but not 'carlos'
        "mexicali",  # Contains 'mexic' but as part of city name
    ]
    
    for text in safe_texts:
        has_forbidden, words = contains_forbidden_identity(text)
        # Note: 'mexicali' might still trigger 'mexico' - this is expected
        # We're mainly testing that 'carlos' doesn't match 'caracas'
        if 'carlos' in words:
            assert False, f"False positive for 'carlos' in: {text}"
    
    print("✅ Test passed: Word boundaries respected (no false positives for 'carlos')")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("RUNNING IDENTITY VALIDATOR TESTS")
    print("="*70 + "\n")
    
    tests = [
        test_contains_forbidden_identity_carlos,
        test_contains_forbidden_identity_clean,
        test_validate_response_invalid,
        test_validate_response_valid,
        test_clean_response_removes_bad_sentences,
        test_get_fallback_response,
        test_validate_and_clean_response_mixed,
        test_validate_and_clean_response_all_bad,
        test_case_insensitive,
        test_word_boundaries
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {test.__name__}")
            print(f"   Error: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {test.__name__}")
            print(f"   Error: {str(e)}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
