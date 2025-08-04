# PUENTE Catastral Workflows

Workflows para unificación de procesos del **Catastro** y **Registro Público de la Propiedad (RPP)** en MuniStream.

## Workflows Disponibles

### 1. Actualización Catastral Unificada
- **ID**: `actualizacion_catastral_v1`
- **Descripción**: Actualizar registro catastral con sincronización automática bidireccional al RPP
- **Funcionalidad**: Vinculación automática en tiempo real entre sistemas

### 2. Certificado de Libertad de Gravamen
- **ID**: `certificado_libertad_v1`
- **Descripción**: Generar certificado unificado consultando Catastro y RPP simultáneamente
- **Funcionalidad**: Consulta integrada de gravámenes

### 3. Avalúo Catastral Unificado
- **ID**: `avaluo_catastral_v1`
- **Descripción**: Generar avalúo catastral considerando información completa de Catastro y RPP
- **Funcionalidad**: Valuación integral con datos unificados

## Instalación

Este plugin se carga automáticamente en MuniStream cuando se configura en `plugins.yaml`:

```yaml
plugins:
  - name: puente-catastral-workflows
    repo_url: https://github.com/PuenteCatastral/puente-catastral-workflows.git
    enabled: true
    version: 1.0.0
    workflows:
      - module: puente_catastral.catastral_workflows
        function: create_actualizacion_catastral_workflow
      - module: puente_catastral.catastral_workflows
        function: create_certificado_libertad_workflow
      - module: puente_catastral.catastral_workflows
        function: create_avaluo_catastral_workflow
```

## Metodologías

- **SoC**: Un workflow por archivo
- **DRY**: Imports centralizados
- **KISS**: Código simple y directo