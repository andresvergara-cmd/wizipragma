# 🤝 Guía de Contribución - CENTLI

¡Gracias por tu interés en contribuir a CENTLI! Esta guía te ayudará a empezar.

---

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Empezar](#cómo-empezar)
- [Workflow de Desarrollo](#workflow-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Testing](#testing)
- [Documentación](#documentación)
- [Pull Requests](#pull-requests)

---

## 📜 Código de Conducta

Este proyecto sigue el [Contributor Covenant](https://www.contributor-covenant.org/). Al participar, se espera que mantengas este código.

---

## 🚀 Cómo Empezar

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU-USUARIO/centli.git
cd centli
```

### 2. Configurar Entorno

**Backend**:
```bash
cd src_aws/app_inference
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Herramientas de desarrollo
```

**Frontend**:
```bash
cd frontend
npm install
```

### 3. Configurar AWS

```bash
# Configurar perfil AWS
aws configure --profile centli-dev

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores
```

### 4. Ejecutar Tests

```bash
# Backend
cd src_aws/app_inference
pytest

# Frontend
cd frontend
npm test
```

---

## 🔄 Workflow de Desarrollo

### 1. Crear Branch

```bash
# Actualizar main
git checkout main
git pull upstream main

# Crear branch para tu feature
git checkout -b feature/nombre-descriptivo
# o
git checkout -b fix/descripcion-del-bug
```

### Convención de Nombres de Branches

- `feature/` - Nuevas funcionalidades
- `fix/` - Corrección de bugs
- `docs/` - Cambios en documentación
- `refactor/` - Refactorización de código
- `test/` - Agregar o mejorar tests
- `chore/` - Tareas de mantenimiento

### 2. Hacer Cambios

```bash
# Hacer tus cambios
# Ejecutar tests
pytest  # Backend
npm test  # Frontend

# Verificar linting
flake8 src_aws/  # Python
npm run lint  # JavaScript
```

### 3. Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git add .
git commit -m "feat: agregar nueva herramienta de pago"
# o
git commit -m "fix: corregir error en streaming de audio"
```

**Tipos de Commit**:
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `style:` - Formato, punto y coma, etc.
- `refactor:` - Refactorización de código
- `test:` - Agregar tests
- `chore:` - Mantenimiento

### 4. Push y Pull Request

```bash
git push origin feature/nombre-descriptivo
```

Luego crea un Pull Request en GitHub.

---

## 📝 Estándares de Código

### Python

**Style Guide**: PEP 8

```python
# ✅ Bueno
def transfer_money(amount: float, recipient: str) -> dict:
    """
    Execute a money transfer.
    
    Args:
        amount: Amount in MXN
        recipient: Recipient name
        
    Returns:
        dict: Transfer result with transaction ID
    """
    if amount <= 0:
        raise ValueError("Amount must be positive")
    
    return {
        "success": True,
        "transaction_id": generate_id()
    }

# ❌ Malo
def transferMoney(amt,rec):
    if amt<=0:return False
    return {"success":True,"id":genId()}
```

**Herramientas**:
```bash
# Linting
flake8 src_aws/

# Formatting
black src_aws/

# Type checking
mypy src_aws/
```

### JavaScript/React

**Style Guide**: Airbnb JavaScript Style Guide

```javascript
// ✅ Bueno
const sendMessage = (message, type = 'TEXT') => {
  if (!message || !message.trim()) {
    throw new Error('Message cannot be empty');
  }
  
  return {
    action: 'sendMessage',
    data: {
      message: message.trim(),
      type,
      timestamp: Date.now()
    }
  };
};

// ❌ Malo
function sendMessage(msg,t){
  return {action:"sendMessage",data:{message:msg,type:t}}
}
```

**Herramientas**:
```bash
# Linting
npm run lint

# Formatting
npm run format

# Type checking (si usas TypeScript)
npm run type-check
```

---

## 🧪 Testing

### Backend (Python)

**Estructura**:
```
tests/
├── unit/
│   ├── test_action_tools.py
│   ├── test_audio_processor.py
│   └── test_bedrock_config.py
└── integration/
    └── test_tool_use_complete.py
```

**Ejemplo de Test**:
```python
import pytest
from action_tools import transfer_money

def test_transfer_money_success():
    result = transfer_money(amount=500, recipient_name="Juan")
    
    assert result["success"] is True
    assert "transaction_id" in result
    assert result["amount"] == 500
    assert result["recipient"] == "Juan"

def test_transfer_money_invalid_amount():
    with pytest.raises(ValueError):
        transfer_money(amount=-100, recipient_name="Juan")
```

**Ejecutar Tests**:
```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=src_aws/app_inference

# Tests específicos
pytest tests/unit/test_action_tools.py -v
```

### Frontend (React)

**Ejemplo de Test**:
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import ChatWidget from './ChatWidget';

test('sends message when button clicked', () => {
  const mockSendMessage = jest.fn();
  render(<ChatWidget sendMessage={mockSendMessage} />);
  
  const input = screen.getByPlaceholderText('Escribe un mensaje...');
  const button = screen.getByRole('button', { name: /enviar/i });
  
  fireEvent.change(input, { target: { value: 'Hola' } });
  fireEvent.click(button);
  
  expect(mockSendMessage).toHaveBeenCalledWith('Hola', 'TEXT');
});
```

**Ejecutar Tests**:
```bash
# Todos los tests
npm test

# Con cobertura
npm test -- --coverage

# Watch mode
npm test -- --watch
```

---

## 📚 Documentación

### Documentar Código

**Python**:
```python
def nueva_funcion(param1: str, param2: int) -> dict:
    """
    Descripción breve de la función.
    
    Descripción más detallada si es necesario.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
        
    Returns:
        dict: Descripción del valor de retorno
        
    Raises:
        ValueError: Cuándo se lanza esta excepción
        
    Example:
        >>> nueva_funcion("test", 42)
        {'result': 'success'}
    """
    pass
```

**JavaScript**:
```javascript
/**
 * Descripción breve de la función.
 * 
 * @param {string} param1 - Descripción del parámetro 1
 * @param {number} param2 - Descripción del parámetro 2
 * @returns {Object} Descripción del valor de retorno
 * @throws {Error} Cuándo se lanza esta excepción
 * 
 * @example
 * nuevaFuncion('test', 42);
 * // returns { result: 'success' }
 */
function nuevaFuncion(param1, param2) {
  // ...
}
```

### Actualizar Documentación

Si tu cambio afecta la funcionalidad:

1. Actualizar README.md si es necesario
2. Actualizar docs/ relevantes
3. Agregar ejemplos de uso
4. Actualizar CHANGELOG.md

---

## 🔍 Pull Requests

### Checklist

Antes de crear un PR, verifica:

- [ ] Tests pasan (`pytest` y `npm test`)
- [ ] Linting pasa (`flake8` y `npm run lint`)
- [ ] Código documentado
- [ ] README actualizado (si aplica)
- [ ] CHANGELOG.md actualizado
- [ ] Commits siguen Conventional Commits
- [ ] Branch actualizado con `main`

### Template de PR

```markdown
## Descripción
Breve descripción de los cambios.

## Tipo de Cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Documentación

## ¿Cómo se ha probado?
Describe las pruebas que ejecutaste.

## Checklist
- [ ] Tests pasan
- [ ] Linting pasa
- [ ] Documentación actualizada
- [ ] CHANGELOG actualizado
```

### Proceso de Review

1. **Automated Checks**: CI/CD ejecuta tests automáticamente
2. **Code Review**: Al menos 1 aprobación requerida
3. **Testing**: Revisor prueba los cambios
4. **Merge**: Squash and merge a `main`

---

## 🎯 Áreas de Contribución

### 🐛 Bug Fixes

Busca issues con label `bug` o `good first issue`.

### ✨ Nuevas Features

Antes de empezar:
1. Abre un issue para discutir la feature
2. Espera feedback del equipo
3. Implementa según el feedback

### 📝 Documentación

Siempre bienvenida:
- Mejorar README
- Agregar ejemplos
- Traducir documentación
- Crear tutoriales

### 🧪 Tests

- Aumentar cobertura
- Agregar tests de integración
- Mejorar tests existentes

### 🎨 UI/UX

- Mejorar diseño
- Agregar animaciones
- Mejorar accesibilidad
- Responsive design

---

## 🆘 Ayuda

### Preguntas

- **GitHub Issues**: Para bugs y features
- **Discussions**: Para preguntas generales
- **Email**: tu-email@ejemplo.com

### Recursos

- [Documentación AWS Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Claude API Docs](https://docs.anthropic.com/)
- [React Docs](https://react.dev/)
- [Python Best Practices](https://docs.python-guide.org/)

---

## 🙏 Agradecimientos

¡Gracias por contribuir a CENTLI! Cada contribución, grande o pequeña, es valiosa.

---

**¿Listo para contribuir? ¡Crea tu primer PR!** 🚀
