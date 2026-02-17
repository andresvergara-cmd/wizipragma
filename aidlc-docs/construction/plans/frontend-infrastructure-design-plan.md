# Infrastructure Design Plan - Unit 4: Frontend Multimodal UI

## Unit Context

**Unit Name**: Frontend Multimodal UI  
**Purpose**: Static web application for multimodal banking interface  
**Tech Stack**: Vanilla JavaScript ES6+, Bootstrap 5 CDN, HTML5/CSS3  
**Dependencies**: Unit 2 (WebSocket API Gateway for backend communication)  
**Context**: 8-hour hackathon, demo quality, simple deployment

---

## Infrastructure Design Steps

### Step 1: Analyze Existing Infrastructure
- [x] Review Unit 1 infrastructure (S3 bucket already created)
- [x] Review Unit 2 infrastructure (WebSocket API Gateway URL)
- [x] Identify shared infrastructure components
- [x] Determine frontend-specific infrastructure needs

### Step 2: Hosting Infrastructure
- [x] Define static file hosting approach (S3, CloudFront, API Gateway)
- [x] Define bucket configuration (public access, CORS, website hosting)
- [x] Define URL structure and access patterns
- [x] Define deployment strategy

### Step 3: Storage Infrastructure
- [x] Define image upload storage (S3 bucket, path structure)
- [x] Define image lifecycle policies (retention, cleanup)
- [x] Define access permissions (public/private)
- [x] Define CORS configuration for uploads

### Step 4: Integration Points
- [x] Define WebSocket API Gateway connection details
- [x] Define authentication token handling
- [x] Define API endpoints for image upload
- [x] Define error handling for backend communication

### Step 5: Deployment Architecture
- [x] Define deployment process (manual, automated)
- [x] Define environment configuration (dev, prod)
- [x] Define rollback strategy
- [x] Define testing approach

---

## Infrastructure Clarification Questions

### Hosting Infrastructure

**Q1: Static File Hosting Approach**  
How should we host the frontend static files?

Options:
A) Use existing S3 bucket from Unit 1 (centli-frontend-bucket) with static website hosting
B) Create new S3 bucket specifically for frontend
C) Use CloudFront distribution in front of S3
D) Use API Gateway HTTP endpoint to serve static files

Given hackathon context, what's the fastest approach?

[Answer]: A) Use existing S3 bucket from Unit 1 (centli-frontend-bucket) with static website hosting. Ya está creado, solo activar website hosting. CloudFront agrega complejidad innecesaria para demo.

---

**Q2: Bucket Configuration**  
What S3 bucket configuration do we need?

- Public read access for static files?
- CORS configuration for WebSocket and image uploads?
- Static website hosting enabled?
- Index document and error document?

[Answer]: Public read access: Sí (para servir HTML/CSS/JS). CORS: Sí (permitir WebSocket desde cualquier origen para demo). Static website hosting: Sí. Index document: index.html. Error document: index.html (SPA behavior).

---

**Q3: URL Structure**  
What URL should users access?

Options:
A) S3 website endpoint: http://centli-frontend-bucket.s3-website-us-east-1.amazonaws.com
B) S3 HTTPS endpoint: https://centli-frontend-bucket.s3.amazonaws.com/index.html
C) CloudFront distribution: https://d1234567890.cloudfront.net
D) Custom domain: https://centli.example.com

Given hackathon demo, which is acceptable?

[Answer]: A) S3 website endpoint para demo rápido. HTTP está OK para hackathon interno. Si necesitamos HTTPS, usar opción B. No CloudFront ni custom domain (tiempo).

---

### Storage Infrastructure

**Q4: Image Upload Storage**  
Where should uploaded images be stored?

Options:
A) Same S3 bucket as frontend (centli-frontend-bucket), separate folder (/uploads/)
B) Separate S3 bucket for user uploads (centli-user-uploads)
C) Unit 1 S3 bucket (centli-data-bucket)
D) No persistent storage (images sent directly to backend, not stored)

[Answer]: A) Same bucket, folder /uploads/. Simplifica permisos y deployment. Estructura: /uploads/{session_id}/{timestamp}_{filename}.jpg

---

**Q5: Image Lifecycle**  
How long should uploaded images be retained?

Options:
A) Permanent (no deletion)
B) 24 hours (demo + cleanup)
C) 7 days
D) 30 days

Given hackathon context and demo data?

[Answer]: B) 24 hours. S3 lifecycle policy para auto-delete después de 1 día. Demo data no necesita persistencia larga.

---

**Q6: Image Access Permissions**  
Should uploaded images be publicly accessible?

Options:
A) Public read (anyone with URL can view)
B) Private (require authentication)
C) Signed URLs (temporary access)
D) No access (backend only)

[Answer]: A) Public read para simplificar. Demo data, no información sensible real. Signed URLs agregan complejidad innecesaria.

---

### Integration Points

**Q7: WebSocket API Gateway URL**  
What WebSocket URL should the frontend use?

From Unit 2 deployment:
- WebSocket URL: wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod

Should this be:
A) Hardcoded in JavaScript
B) Environment variable (injected at build time)
C) Configuration file (config.js)
D) User input (for testing different environments)

Given no build process, what's practical?

[Answer]: C) Configuration file (config.js). Fácil de cambiar sin editar código. Ejemplo: const CONFIG = { WS_URL: 'wss://...', API_URL: 'https://...' };

---

**Q8: Authentication Token**  
How should the frontend obtain authentication tokens?

Options:
A) Mock token generation (client-side, simple JWT)
B) Call authentication API endpoint
C) Hardcoded token for demo
D) User provides token manually

Given hackathon and mock auth approach?

[Answer]: A) Mock token generation client-side. Simple: btoa(JSON.stringify({user_id: userId, timestamp: Date.now()})). No real JWT signing necesario para demo.

---

**Q9: Image Upload API**  
How should images be uploaded to S3?

Options:
A) Direct S3 upload (presigned URL from backend)
B) Upload via API Gateway endpoint (proxy to S3)
C) Direct S3 upload (frontend has S3 credentials)
D) Send image to WebSocket (base64 encoded)

Given security and simplicity?

[Answer]: A) Direct S3 upload con presigned URL. Backend genera presigned URL, frontend hace PUT directo a S3. Más eficiente que proxy. WebSocket no es ideal para archivos grandes.

---

**Q10: Error Handling**  
How should frontend handle backend communication errors?

- WebSocket connection failures?
- Image upload failures?
- API timeout errors?
- Network errors?

[Answer]: WebSocket: auto-reconnect (ya definido en NFR). Image upload: retry button + error toast. API timeout: 30s timeout, mostrar error. Network errors: "Sin conexión, verifica tu red" message.

---

### Deployment Architecture

**Q11: Deployment Process**  
How should we deploy frontend updates?

Options:
A) Manual AWS CLI (aws s3 sync)
B) AWS SAM deployment (include in template.yaml)
C) GitHub Actions CI/CD
D) Manual upload via AWS Console

Given hackathon timeline?

[Answer]: A) Manual AWS CLI. Script: deploy-frontend.sh. Rápido, simple, suficiente para demo. SAM template puede incluir bucket config pero deploy manual de archivos.

---

**Q12: Environment Configuration**  
Do we need multiple environments?

Options:
A) Single environment (prod only)
B) Two environments (dev, prod)
C) Three environments (dev, staging, prod)

Given hackathon context?

[Answer]: A) Single environment (prod). No tiempo para múltiples ambientes. Desarrollo local (file:// o local server), deploy directo a prod para demo.

---

**Q13: Rollback Strategy**  
How should we handle rollback if deployment fails?

Options:
A) S3 versioning enabled (rollback to previous version)
B) Keep backup of previous deployment locally
C) No rollback (fix forward)
D) Git tag + redeploy previous version

[Answer]: C) No rollback formal. Fix forward (deploy fix rápido). S3 versioning opcional pero no crítico para demo. Git history suficiente para recuperar versión anterior si necesario.

---

**Q14: Testing Approach**  
How should we test the deployed frontend?

Options:
A) Manual testing checklist after each deployment
B) Automated smoke tests
C) No formal testing (test during development)
D) User acceptance testing

Given hackathon timeline?

[Answer]: A) Manual testing checklist. Verificar: página carga, WebSocket conecta, voice funciona, chat funciona, image upload funciona. 5 minutos de testing post-deploy.

---

### Monitoring and Observability

**Q15: Frontend Monitoring**  
What monitoring do we need for the frontend?

Options:
A) CloudWatch RUM (Real User Monitoring)
B) S3 access logs
C) CloudFront logs (if using CloudFront)
D) No monitoring (console logs only)

Given hackathon context?

[Answer]: D) No monitoring externo. Console logs en browser suficiente. S3 access logs opcional pero no necesario para demo. Focus en funcionalidad, no observability.

---

**Q16: Error Tracking**  
Should we track frontend errors?

Options:
A) Sentry or similar error tracking service
B) CloudWatch Logs (send errors from frontend)
C) Console only (no external tracking)
D) Custom error logging endpoint

[Answer]: C) Console only. No tiempo para setup de error tracking. Browser DevTools suficiente para debugging durante demo.

---

### Security and Compliance

**Q17: CORS Configuration**  
What CORS configuration does S3 bucket need?

- Allow all origins (*) or specific origins?
- Allow which methods (GET, POST, PUT)?
- Allow which headers?

Given demo context?

[Answer]: Allow all origins (*) para simplificar. Methods: GET (static files), PUT (image upload). Headers: Content-Type, Authorization. Configuración permisiva OK para demo interno.

---

**Q18: Content Security Policy**  
Should we implement CSP headers?

Options:
A) Strict CSP (whitelist all sources)
B) Basic CSP (allow CDN sources)
C) No CSP (for demo simplicity)

[Answer]: C) No CSP para demo. Agrega complejidad. Bootstrap CDN, WebSocket, S3 todos necesitan whitelisting. Skip para hackathon.

---

**Q19: HTTPS Requirement**  
Do we need HTTPS for the frontend?

- S3 website endpoint is HTTP only
- S3 object endpoint supports HTTPS
- CloudFront provides HTTPS

Given WebSocket uses WSS (secure), should frontend be HTTPS?

[Answer]: Idealmente HTTPS pero HTTP OK para demo interno. Si browser bloquea WSS desde HTTP origin, usar S3 object endpoint (HTTPS) en lugar de website endpoint. Probar primero, cambiar si necesario.

---

**Q20: Secrets Management**  
How should we handle sensitive configuration?

- WebSocket URL
- S3 bucket names
- API endpoints

Options:
A) Hardcoded in config.js (acceptable for demo)
B) Environment variables (requires build process)
C) AWS Secrets Manager
D) Parameter Store

[Answer]: A) Hardcoded en config.js. No secrets reales (todo es demo data). WebSocket URL y bucket names son públicos anyway. No necesidad de secrets management complejo.

---

## Success Criteria

- [x] All infrastructure questions answered
- [x] Hosting infrastructure defined
- [x] Storage infrastructure defined
- [x] Integration points specified
- [x] Deployment architecture documented
- [x] User approval obtained

---

**Plan Status**: COMPLETED  
**Completion Date**: 2026-02-17T15:45:00Z  
**Total Questions**: 20 questions answered with pragmatic hackathon approach  
**Next Step**: Generate infrastructure design artifacts
