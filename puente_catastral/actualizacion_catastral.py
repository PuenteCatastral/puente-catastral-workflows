"""
Workflow de Actualización Catastral Unificada.
"""

def create_actualizacion_catastral_workflow():
    """Crear workflow de actualización catastral unificada."""
    return {
        "workflow_id": "actualizacion_catastral_v1",
        "name": "Actualización Catastral Unificada",
        "description": "Actualizar registro catastral con sincronización automática bidireccional al RPP",
        "version": "1.0.0",
        "status": "active",
        "steps": [
            {
                "step_id": "collect_catastral_data",
                "name": "Recopilar Datos Catastrales",
                "step_type": "action",
                "description": "Recolección de información catastral del ciudadano",
                "required_inputs": ["clave_catastral", "tipo_actualizacion", "datos_propiedades"],
                "optional_inputs": ["observaciones"],
                "next_steps": ["validate_catastral_data"]
            },
            {
                "step_id": "validate_catastral_data",
                "name": "Validar Datos Catastrales",
                "step_type": "action", 
                "description": "Validación de la información catastral proporcionada",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["search_rpp_records"]
            },
            {
                "step_id": "search_rpp_records",
                "name": "Buscar Registros RPP",
                "step_type": "integration",
                "description": "Búsqueda automática de registros correspondientes en RPP",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["auto_linking_process"]
            },
            {
                "step_id": "auto_linking_process",
                "name": "Proceso de Vinculación Automática",
                "step_type": "action",
                "description": "Algoritmo de vinculación automática entre Catastro y RPP",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["linking_decision"]
            },
            {
                "step_id": "linking_decision",
                "name": "Decisión de Vinculación",
                "step_type": "conditional",
                "description": "Evaluar resultado de vinculación automática",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["update_catastral_record", "manual_review_required"]
            },
            {
                "step_id": "update_catastral_record",
                "name": "Actualizar Registro Catastral",
                "step_type": "integration",
                "description": "Actualizar información en sistema catastral",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["sync_to_rpp"]
            },
            {
                "step_id": "sync_to_rpp",
                "name": "Sincronizar al RPP",
                "step_type": "integration",
                "description": "Sincronización bidireccional con RPP",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["verify_synchronization"]
            },
            {
                "step_id": "verify_synchronization",
                "name": "Verificar Sincronización",
                "step_type": "action",
                "description": "Verificar que la sincronización fue exitosa",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["send_notification", "rollback_changes"]
            },
            {
                "step_id": "send_notification",
                "name": "Enviar Notificación",
                "step_type": "action",
                "description": "Notificar al ciudadano sobre actualización exitosa",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["actualizacion_completada"]
            },
            {
                "step_id": "actualizacion_completada",
                "name": "Actualización Completada",
                "step_type": "terminal",
                "description": "Actualización catastral unificada completada exitosamente",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": []
            },
            {
                "step_id": "manual_review_required",
                "name": "Revisión Manual Requerida",
                "step_type": "terminal",
                "description": "La vinculación automática requiere revisión manual",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": []
            },
            {
                "step_id": "rollback_changes",
                "name": "Revertir Cambios",
                "step_type": "terminal",
                "description": "Sincronización falló, cambios revertidos automáticamente",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": []
            }
        ],
        "start_step_id": "collect_catastral_data"
    }