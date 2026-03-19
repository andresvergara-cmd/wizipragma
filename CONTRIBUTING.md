# Guía de Contribución - Comfi

## Cómo Empezar

### 1. Clonar

```bash
git clone <repo-url>
cd comfi
```

### 2. Configurar Entorno

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

**Tests**:
```bash
pip install pytest boto3 moto
python -m pytest tests/unit/ -v
```

---

## Workflow de Desarrollo

1. Crear branch: `git checkout -b feature/nueva-funcionalidad`
2. Hacer cambios y probar localmente
3. Correr tests: `python -m pytest tests/unit/ -v`
4. Commit: `git commit -am 'feat: descripción del cambio'`
5. Push: `git push origin feature/nueva-funcionalidad`
6. Crear Pull Request

---

## Estándares de Código

- **Python**: PEP 8, type hints, docstrings
- **JavaScript/React**: Componentes funcionales, hooks
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`)

---

## Estructura de Archivos

| Directorio | Contenido |
|------------|-----------|
| `src_aws/app_message/` | Lambda de producción (orquestador) |
| `src_aws/app_connect/` | Lambda $connect |
| `src_aws/app_disconnect/` | Lambda $disconnect |
| `src_aws/app_inference/` | Código legacy (NO usar en producción) |
| `frontend/` | React 18 + Vite |
| `tests/` | Tests unitarios |
| `docs/` | Documentación técnica |
| `scripts/` | Scripts de deploy y testing |
| `aidlc-docs/` | Documentación de diseño (AI-DLC) |
| `knowledge-base-docs/` | Documentos fuente para Knowledge Base |

> No agregar archivos temporales o de trabajo al root del proyecto.
