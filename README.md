# Sigte-api-roles

## Introducción

Sigte-api-roles es el api de roles construida en python con fastapi, que va en conjunto al api-auth.

## Table of Contents

- [Instalación](#instalación)
- [Configuración](#configuración)
  - [Variables de Entorno](#variables-de-entorno)


## Instalación

Para instalar y ejecutar  Sigte-api-roles:

1. Clone o descargue el código fuente del proyecto.
2. Navegue al directorio del proyecto y modifique el archivo `docker-compose.yml` según sea necesario.

## Configuración

### Variables de Entorno

Configure las siguientes variables de entorno en su archivo `docker-compose.yml`:

```yaml
version: '3.8'

services:
  fastapi:
    build: .
    ports:
      - "9001:9001"
    environment:
      - PG_URL=postgresql://usr:pass@host/db
    volumes:
      - .:/app

```

Variables del `docker-compose.yml`:

| Variable                       | Valores Esperados | Valores por Defecto |
|--------------------------------|-------------------|---------------------|
| `PG_URL`                 | postgresql://usr:pass@host/db | - |


### Entidad necesaria
Sigte utiliza una base de datos PostgreSQL para almacenar la información.
A continuación se muestra el script de creación de la tabla

```sql
    create table if not exists public.roles
(
    id          serial,
    name        varchar(50),
    description varchar(255),
    code        integer,
    status      boolean
);

alter table public.roles
    owner to postgres;
```

### Acceso a la doc del servicio
`http//host:port/docs`

## Uso
**Resumen de uso:**
 
 1. Configurar archivo `docker-compose.yml` con las variables de entorno correspondientes.
 2. Crear la entidad en la base de datos
 3. Ejecutar el comando:
 ```bash
    docker compose build
 ```

4. Si el build termina con exito ejecutar:
```bash
docker compose up -d
```

5. Acceder a la url configurada.
