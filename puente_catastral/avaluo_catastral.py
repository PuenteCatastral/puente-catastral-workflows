"""
Workflow de Avalúo Catastral Unificado.
"""

from typing import Dict, Any

# Import CivicStream workflow components
try:
    from app.workflows.base import (
        ActionStep, ConditionalStep, IntegrationStep, TerminalStep, ApprovalStep
    )
    from app.workflows.workflow import Workflow
except ImportError:
    # Fallback for development
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend/app'))
    from workflows.base import (
        ActionStep, ConditionalStep, IntegrationStep, TerminalStep, ApprovalStep
    )
    from workflows.workflow import Workflow


def create_avaluo_catastral_workflow() -> Workflow:
    """Crear workflow de avalúo catastral unificado."""
    workflow = Workflow(
        workflow_id="avaluo_catastral_v1",
        name="Avalúo Catastral Unificado",
        description="Generar avalúo catastral considerando información completa de Catastro y RPP"
    )
    
    # Paso 1: Recopilar solicitud de avalúo
    step_collect_request = ActionStep(
        step_id="collect_avaluo_request",
        name="Recopilar Solicitud de Avalúo",
        description="Recolección de información para solicitud de avalúo",
        action=lambda instance, context: {"status": "awaiting_input"},
        requires_citizen_input=True,
        input_form={
            "title": "Solicitud de Avalúo Catastral",
            "description": "Proporcione información para realizar el avalúo",
            "fields": [
                {
                    "id": "clave_catastral",
                    "name": "clave_catastral",
                    "label": "Clave Catastral",
                    "type": "text",
                    "required": True,
                    "pattern": "^[0-9]{2}-[0-9]{3}-[0-9]{3}$",
                    "helpText": "Clave catastral del inmueble a valuar"
                },
                {
                    "id": "proposito_avaluo",
                    "name": "proposito_avaluo",
                    "label": "Propósito del Avalúo",
                    "type": "select",
                    "required": True,
                    "options": ["Compraventa", "Crédito hipotecario", "Herencia", "Donación", "Actualización catastral"],
                    "helpText": "Para qué se utilizará el avalúo"
                },
                {
                    "id": "solicitante",
                    "name": "solicitante",
                    "label": "Nombre del Solicitante",
                    "type": "text",
                    "required": True,
                    "helpText": "Nombre de quien solicita el avalúo"
                },
                {
                    "id": "tipo_avaluo",
                    "name": "tipo_avaluo",
                    "label": "Tipo de Avalúo",
                    "type": "select",
                    "required": True,
                    "options": ["Físico (con inspección)", "Documental (sin inspección)"],
                    "helpText": "Tipo de avalúo solicitado"
                }
            ]
        }
    )
    
    # Paso 2: Buscar registros de propiedad
    step_search_records = IntegrationStep(
        step_id="search_property_records",
        name="Buscar Registros de Propiedad",
        description="Búsqueda de información completa en Catastro y RPP",
        action=lambda instance, context: {"status": "found", "records_complete": True}
    )
    
    # Paso 3: Verificar registros
    step_records_check = ConditionalStep(
        step_id="property_records_check",
        name="Verificación de Registros",
        description="Verificar si se encontraron los registros necesarios",
        condition=lambda instance, context: context.get("records_complete", False)
    )
    
    # Paso 4: Recopilar datos de mercado
    step_market_data = IntegrationStep(
        step_id="gather_market_data",
        name="Recopilar Datos de Mercado",
        description="Obtener información de mercado inmobiliario de la zona",
        action=lambda instance, context: {"status": "gathered", "market_data": "sample_data"}
    )
    
    # Paso 5: Realizar valuación
    step_valuation = ActionStep(
        step_id="perform_valuation",
        name="Realizar Valuación",
        description="Valuación considerando todos los datos disponibles",
        action=lambda instance, context: {"status": "completed", "valuation_result": "success"}
    )
    
    # Paso 6: Revisión de valuación
    step_review = ApprovalStep(
        step_id="valuation_review",
        name="Revisión de Valuación",
        description="Revisión técnica del avalúo por supervisor",
        required_role="valuation_supervisor",
        timeout_hours=24
    )
    
    # Paso 7: Generar reporte de avalúo
    step_generate_report = ActionStep(
        step_id="generate_appraisal_report",
        name="Generar Reporte de Avalúo",
        description="Generar reporte oficial de avalúo",
        action=lambda instance, context: {"status": "report_generated"}
    )
    
    # Pasos terminales
    step_completed = TerminalStep(
        step_id="avaluo_completado",
        name="Avalúo Completado",
        description="Avalúo catastral unificado completado exitosamente"
    )
    
    step_incomplete = TerminalStep(
        step_id="incomplete_records_found",
        name="Registros Incompletos",
        description="No se encontró información suficiente para realizar el avalúo"
    )
    
    step_correction = TerminalStep(
        step_id="valuation_requires_correction",
        name="Valuación Requiere Corrección",
        description="La valuación fue rechazada y requiere correcciones"
    )
    
    # Agregar pasos al workflow
    workflow.add_step(step_collect_request)
    workflow.add_step(step_search_records)
    workflow.add_step(step_records_check)
    workflow.add_step(step_market_data)
    workflow.add_step(step_valuation)
    workflow.add_step(step_review)
    workflow.add_step(step_generate_report)
    workflow.add_step(step_completed)
    workflow.add_step(step_incomplete)
    workflow.add_step(step_correction)
    
    # Definir flujo
    workflow.add_transition(step_collect_request, step_search_records)
    workflow.add_transition(step_search_records, step_records_check)
    workflow.add_transition(step_records_check, step_market_data, condition=True)
    workflow.add_transition(step_records_check, step_incomplete, condition=False)
    workflow.add_transition(step_market_data, step_valuation)
    workflow.add_transition(step_valuation, step_review)
    workflow.add_transition(step_review, step_generate_report)
    workflow.add_transition(step_generate_report, step_completed)
    
    return workflow