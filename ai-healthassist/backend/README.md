# AI-HealthAssist Backend Deployment — v1.9

## Runtime
FastAPI + Python. GitHub Pages hosts the static frontend only; run this backend on a separate HTTPS service.

## Required configuration

```bash
export AIH_CORS_ORIGINS="https://safdar404.github.io"
export AIH_ENV="production"
```

For production, store database credentials and signing secrets in the hosting provider's secret manager. Never commit `.env` files or credentials.

## Minimum production controls

- HTTPS/TLS termination
- Restrictive CORS: allow only the production frontend origin
- API authentication/authorization for protected endpoints
- Rate limiting and request-size limits
- Structured audit logging without sensitive patient data
- Database backups and migrations
- Health/readiness endpoint
- Monitoring and alerting
- Dependency and container vulnerability scanning
- Separate development/staging/production environments

## Suggested service layout

```text
GitHub Pages frontend
        |
      HTTPS
        |
   Reverse Proxy / WAF
        |
      FastAPI
     /  |   \
 Safety ML  Audit
        |
 PostgreSQL + PostGIS
```

## Deployment gate

The clinical model remains **research-only**. Production deployment of a clinical decision-support model requires appropriate clinical validation, governance, privacy/security review, and applicable regulatory assessment. This document describes software deployment controls; it does not establish clinical validation.
