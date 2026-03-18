# Guía de Contribución - Comfi

Gracias por tu interés en contribuir a Comfi, el asistente virtual de Comfama.

---

## Cómo Empezar

### 1. Fork y Clone

```bash
git clone https://github.com/TU-USUARIO/comfi.git
cd comfi
```

### 2. Configurar Entorno

**Backend**:
```bash
cd src_aws/app_inference
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

---

## Workflow de Desarrollo

1. Crear branch: `git checkout -b feature/nueva-funcionalidad`
2. Hacer cambios y probar localmente
3. Correr tests: `pytest tests/unit/ -v`
4. Commit: `git commit -am 'feat: descripción del cambio'`
5. Push: `git push origin feature/nueva-funcionalidad`
6. Crear Pull Request a `main`

---

## Estándares de Código

- **Python**: PEP 8, type hints, docstrings
- **JavaScript/React**: ESLint, componentes funcionales
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`)
- **Tests**: Cobertura mínima 80%

---

## Estructura de Archivos

- Código de aplicación: `src_aws/`, `frontend/`
- Tests: `tests/`
- Documentación técnica: `docs/`
- Scripts de deployment: `scripts/`
- Documentación de diseño (AI-DLC): `aidlc-docs/`
- Archivos de trabajo históricos: `archive/`

No agregar archivos temporales o de trabajo al root del proyecto.

---

## Agregar un Nuevo Tool

1. Definir la función en `src_aws/app_inference/action_tools.py`
2. Agregar el tool spec con `inputSchema`
3. Registrar en `execute_tool()`
4. Agregar tests en `tests/unit/`
5. Desplegar con el script correspondiente en `scripts/`
