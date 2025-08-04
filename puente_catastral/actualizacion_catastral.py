"""
Workflow de Actualización Catastral Unificada.
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


def create_actualizacion_catastral_workflow() -> Workflow:
    """Crear workflow de actualización catastral unificada."""
    workflow = Workflow(
        workflow_id="actualizacion_catastral_v1",
        name="Actualización Catastral Unificada",
        description="Actualizar registro catastral con sincronización automática bidireccional al RPP"
    )
    
    # Paso 1: Recopilar datos catastrales
    step_collect_data = ActionStep(
        step_id="collect_catastral_data",
        name="Recopilar Datos Catastrales",
        description="Recolección de información catastral del ciudadano",
        action=lambda instance, context: {"status": "awaiting_input"},
        requires_citizen_input=True,
        input_form={
            "title": "Actualización de Registro Catastral",
            "description": "Proporcione los datos del inmueble a actualizar",
            "fields": [
                {
                    "id": "clave_catastral",
                    "name": "clave_catastral",
                    "label": "Clave Catastral",
                    "type": "text",
                    "required": True,
                    "pattern": "^[0-9]{2}-[0-9]{3}-[0-9]{3}$",
                    "placeholder": "09-123-456",
                    "helpText": "Formato: XX-XXX-XXX"
                },
                {
                    "id": "tipo_actualizacion",
                    "name": "tipo_actualizacion",
                    "label": "Tipo de Actualización",
                    "type": "select",
                    "required": True,
                    "options": ["Cambio de propietario", "Modificación de superficie", "Cambio de uso de suelo", "Actualización de valor"],
                    "helpText": "Seleccione el tipo de actualización a realizar"
                },
                {
                    "id": "observaciones",
                    "name": "observaciones",
                    "label": "Observaciones",
                    "type": "textarea",
                    "required": False,
                    "helpText": "Información adicional sobre la actualización"
                }
            ]
        }
    )
    
    # Paso 2: Validar datos catastrales
    step_validate_data = ActionStep(
        step_id="validate_catastral_data",
        name="Validar Datos Catastrales",
        description="Validación de la información catastral proporcionada",
        action=lambda instance, context: {"status": "validated", "validation_result": "success"}
    )
    
    # Paso 3: Buscar registros RPP
    step_search_rpp = IntegrationStep(
        step_id="search_rpp_records",
        name="Buscar Registros RPP",
        description="Búsqueda automática de registros correspondientes en RPP",
        action=lambda instance, context: {"status": "found", "rpp_records": ["sample_record"]}
    )
    
    # Paso 4: Proceso de vinculación automática
    step_auto_linking = ActionStep(
        step_id="auto_linking_process",
        name="Proceso de Vinculación Automática",
        description="Algoritmo de vinculación automática entre Catastro y RPP",
        action=lambda instance, context: {"status": "processed", "match_score": 95}
    )
    
    # Paso 5: Decisión de vinculación
    step_linking_decision = ConditionalStep(
        step_id="linking_decision",
        name="Decisión de Vinculación",
        description="Evaluar resultado de vinculación automática",
        condition=lambda instance, context: context.get("match_score", 0) >= 90
    )
    
    # Paso 6: Actualizar registro catastral
    step_update_catastral = IntegrationStep(
        step_id="update_catastral_record",
        name="Actualizar Registro Catastral",
        description="Actualizar información en sistema catastral",
        action=lambda instance, context: {"status": "updated"}
    )
    
    # Paso 7: Sincronizar al RPP
    step_sync_rpp = IntegrationStep(
        step_id="sync_to_rpp",
        name="Sincronizar al RPP",
        description="Sincronización bidireccional con RPP",
        action=lambda instance, context: {"status": "synchronized"}
    )
    
    # Paso 8: Verificar sincronización
    step_verify_sync = ActionStep(
        step_id="verify_synchronization",
        name="Verificar Sincronización",
        description="Verificar que la sincronización fue exitosa",
        action=lambda instance, context: {"status": "verified", "sync_success": True}
    )
    
    # Paso 9: Enviar notificación
    step_notification = ActionStep(
        step_id="send_notification",
        name="Enviar Notificación",
        description="Notificar al ciudadano sobre actualización exitosa",
        action=lambda instance, context: {"status": "notification_sent"}
    )
    
    # Pasos terminales
    step_completed = TerminalStep(
        step_id="actualizacion_completada",
        name="Actualización Completada",
        description="Actualización catastral unificada completada exitosamente"
    )
    
    step_manual_review = TerminalStep(
        step_id="manual_review_required",
        name="Revisión Manual Requerida",
        description="La vinculación automática requiere revisión manual"
    )
    
    step_rollback = TerminalStep(
        step_id="rollback_changes",
        name="Revertir Cambios",
        description="Sincronización falló, cambios revertidos automáticamente"
    )
    
    # Agregar pasos al workflow
    workflow.add_step(step_collect_data)
    workflow.add_step(step_validate_data)
    workflow.add_step(step_search_rpp)
    workflow.add_step(step_auto_linking)
    workflow.add_step(step_linking_decision)
    workflow.add_step(step_update_catastral)
    workflow.add_step(step_sync_rpp)
    workflow.add_step(step_verify_sync)
    workflow.add_step(step_notification)
    workflow.add_step(step_completed)
    workflow.add_step(step_manual_review)
    workflow.add_step(step_rollback)
    
    # Definir flujo
    workflow.add_transition(step_collect_data, step_validate_data)
    workflow.add_transition(step_validate_data, step_search_rpp)
    workflow.add_transition(step_search_rpp, step_auto_linking)
    workflow.add_transition(step_auto_linking, step_linking_decision)
    workflow.add_transition(step_linking_decision, step_update_catastral, condition=True)
    workflow.add_transition(step_linking_decision, step_manual_review, condition=False)
    workflow.add_transition(step_update_catastral, step_sync_rpp)
    workflow.add_transition(step_sync_rpp, step_verify_sync)
    workflow.add_transition(step_verify_sync, step_notification)
    workflow.add_transition(step_notification, step_completed)
    
    return workflow