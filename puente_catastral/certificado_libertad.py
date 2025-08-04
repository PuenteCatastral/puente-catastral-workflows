"""
Workflow de Certificado de Libertad de Gravamen Unificado.
"""

from typing import Dict, Any

# Import CivicStream workflow components
try:
    from app.workflows.base import (
        ActionStep, ConditionalStep, IntegrationStep, TerminalStep
    )
    from app.workflows.workflow import Workflow
except ImportError:
    # Fallback for development
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend/app'))
    from workflows.base import (
        ActionStep, ConditionalStep, IntegrationStep, TerminalStep
    )
    from workflows.workflow import Workflow


def create_certificado_libertad_workflow() -> Workflow:
    """Crear workflow de certificado de libertad de gravamen unificado."""
    workflow = Workflow(
        workflow_id="certificado_libertad_v1",
        name="Certificado de Libertad de Gravamen",
        description="Generar certificado unificado consultando Catastro y RPP simultáneamente"
    )
    
    # Paso 1: Recopilar criterios de búsqueda
    step_collect_criteria = ActionStep(
        step_id="collect_search_criteria",
        name="Recopilar Criterios de Búsqueda",
        description="Recolección de criterios para búsqueda de la propiedad",
        action=lambda instance, context: {"status": "awaiting_input"},
        requires_citizen_input=True,
        input_form={
            "title": "Certificado de Libertad de Gravamen",
            "description": "Proporcione información para localizar la propiedad",
            "fields": [
                {
                    "id": "search_type",
                    "name": "search_type",
                    "label": "Tipo de Búsqueda",
                    "type": "select",
                    "required": True,
                    "options": ["Clave Catastral", "Folio Real", "Dirección", "Propietario"],
                    "helpText": "Seleccione el tipo de criterio de búsqueda"
                },
                {
                    "id": "clave_catastral",
                    "name": "clave_catastral",
                    "label": "Clave Catastral",
                    "type": "text",
                    "required": False,
                    "pattern": "^[0-9]{2}-[0-9]{3}-[0-9]{3}$",
                    "helpText": "Clave catastral si se conoce"
                },
                {
                    "id": "solicitante_nombre",
                    "name": "solicitante_nombre",
                    "label": "Nombre del Solicitante",
                    "type": "text",
                    "required": True,
                    "helpText": "Nombre de quien solicita el certificado"
                }
            ]
        }
    )
    
    # Paso 2: Buscar registros unificados
    step_search_records = IntegrationStep(
        step_id="search_unified_records",
        name="Buscar Registros Unificados",
        description="Búsqueda simultánea en Catastro y RPP",
        action=lambda instance, context: {"status": "found", "property_found": True}
    )
    
    # Paso 3: Verificar resultados
    step_results_check = ConditionalStep(
        step_id="search_results_check",
        name="Verificación de Resultados",
        description="Verificar si se encontró la propiedad",
        condition=lambda instance, context: context.get("property_found", False)
    )
    
    # Paso 4: Analizar estado de gravámenes
    step_analyze_liens = ActionStep(
        step_id="analyze_lien_status",
        name="Analizar Estado de Gravámenes",
        description="Analizar información de gravámenes de ambos sistemas",
        action=lambda instance, context: {"status": "analyzed", "liens_found": False}
    )
    
    # Paso 5: Decisión sobre gravámenes
    step_lien_decision = ConditionalStep(
        step_id="lien_analysis_result",
        name="Resultado de Análisis de Gravámenes",
        description="Evaluar si la propiedad está libre de gravámenes",
        condition=lambda instance, context: not context.get("liens_found", True)
    )
    
    # Paso 6: Generar certificado libre
    step_generate_clean = ActionStep(
        step_id="generate_clean_certificate",
        name="Generar Certificado Libre",
        description="Generar certificado oficial de libertad de gravamen",
        action=lambda instance, context: {"status": "certificate_generated"}
    )
    
    # Paso 7: Generar reporte de gravámenes
    step_generate_report = ActionStep(
        step_id="generate_lien_report",
        name="Generar Reporte de Gravámenes",
        description="Generar reporte detallado de gravámenes encontrados",
        action=lambda instance, context: {"status": "report_generated"}
    )
    
    # Paso 8: Firmar certificado
    step_sign = ActionStep(
        step_id="sign_certificate",
        name="Firmar Certificado",
        description="Aplicar firma digital al certificado",
        action=lambda instance, context: {"status": "signed"}
    )
    
    # Pasos terminales
    step_completed = TerminalStep(
        step_id="certificado_emitido",
        name="Certificado Emitido",
        description="Certificado de libertad de gravamen emitido exitosamente"
    )
    
    step_not_found = TerminalStep(
        step_id="property_not_found",
        name="Propiedad No Encontrada",
        description="No se pudo localizar la propiedad con los criterios proporcionados"
    )
    
    # Agregar pasos al workflow
    workflow.add_step(step_collect_criteria)
    workflow.add_step(step_search_records)
    workflow.add_step(step_results_check)
    workflow.add_step(step_analyze_liens)
    workflow.add_step(step_lien_decision)
    workflow.add_step(step_generate_clean)
    workflow.add_step(step_generate_report)
    workflow.add_step(step_sign)
    workflow.add_step(step_completed)
    workflow.add_step(step_not_found)
    
    # Definir flujo
    workflow.add_transition(step_collect_criteria, step_search_records)
    workflow.add_transition(step_search_records, step_results_check)
    workflow.add_transition(step_results_check, step_analyze_liens, condition=True)
    workflow.add_transition(step_results_check, step_not_found, condition=False)
    workflow.add_transition(step_analyze_liens, step_lien_decision)
    workflow.add_transition(step_lien_decision, step_generate_clean, condition=True)
    workflow.add_transition(step_lien_decision, step_generate_report, condition=False)
    workflow.add_transition(step_generate_clean, step_sign)
    workflow.add_transition(step_generate_report, step_sign)
    workflow.add_transition(step_sign, step_completed)
    
    return workflow