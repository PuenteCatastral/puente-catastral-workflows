"""
Workflow de Avalúo Catastral Unificado.
"""

def create_avaluo_catastral_workflow():
    """Crear workflow de avalúo catastral unificado."""
    return {
        "workflow_id": "avaluo_catastral_v1",
        "name": "Avalúo Catastral Unificado",
        "description": "Generar avalúo catastral considerando información completa de Catastro y RPP",
        "version": "1.0.0",
        "status": "active",
        "steps": [
            {
                "step_id": "collect_avaluo_request",
                "name": "Recopilar Solicitud de Avalúo",
                "step_type": "action",
                "description": "Recolección de información para solicitud de avalúo",
                "required_inputs": ["clave_catastral", "proposito_avaluo", "solicitante", "tipo_avaluo"],
                "optional_inputs": ["urgencia"],
                "next_steps": ["search_property_records"]
            },
            {
                "step_id": "search_property_records",
                "name": "Buscar Registros de Propiedad",
                "step_type": "integration",
                "description": "Búsqueda de información completa en Catastro y RPP",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["property_records_check"]
            },
            {
                "step_id": "property_records_check",
                "name": "Verificación de Registros",
                "step_type": "conditional",
                "description": "Verificar si se encontraron los registros necesarios",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["gather_market_data", "incomplete_records_found"]
            },
            {
                "step_id": "gather_market_data",
                "name": "Recopilar Datos de Mercado",
                "step_type": "integration",
                "description": "Obtener información de mercado inmobiliario de la zona",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["perform_valuation"]
            },
            {
                "step_id": "perform_valuation",
                "name": "Realizar Valuación",
                "step_type": "action",
                "description": "Valuación considerando todos los datos disponibles",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["valuation_review"]
            },
            {
                "step_id": "valuation_review",
                "name": "Revisión de Valuación",
                "step_type": "approval",
                "description": "Revisión técnica del avalúo por supervisor",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["generate_appraisal_report", "valuation_requires_correction"]
            },
            {
                "step_id": "generate_appraisal_report",
                "name": "Generar Reporte de Avalúo",
                "step_type": "action",
                "description": "Generar reporte oficial de avalúo",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["avaluo_completado"]
            },
            {
                "step_id": "avaluo_completado",
                "name": "Avalúo Completado",
                "step_type": "terminal",
                "description": "Avalúo catastral unificado completado exitosamente",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": []
            },
            {
                "step_id": "incomplete_records_found",
                "name": "Registros Incompletos",
                "step_type": "terminal",
                "description": "No se encontró información suficiente para realizar el avalúo",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": []
            },
            {
                "step_id": "valuation_requires_correction",
                "name": "Valuación Requiere Corrección",
                "step_type": "terminal",
                "description": "La valuación fue rechazada y requiere correcciones",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": []
            }
        ],
        "start_step_id": "collect_avaluo_request"
    }