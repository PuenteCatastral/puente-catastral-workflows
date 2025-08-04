"""
Workflow de Certificado de Libertad de Gravamen Unificado.
"""

def create_certificado_libertad_workflow():
    """Crear workflow de certificado de libertad de gravamen unificado."""
    return {
        "workflow_id": "certificado_libertad_v1",
        "name": "Certificado de Libertad de Gravamen",
        "description": "Generar certificado unificado consultando Catastro y RPP simultáneamente",
        "version": "1.0.0",
        "status": "active",
        "steps": [
            {
                "step_id": "collect_search_criteria",
                "name": "Recopilar Criterios de Búsqueda",
                "step_type": "action",
                "description": "Recolección de criterios para búsqueda de la propiedad",
                "required_inputs": ["search_type", "solicitante_nombre"],
                "optional_inputs": ["clave_catastral", "folio_real", "direccion", "propietario"],
                "next_steps": ["search_unified_records"]
            },
            {
                "step_id": "search_unified_records",
                "name": "Buscar Registros Unificados",
                "step_type": "integration",
                "description": "Búsqueda simultánea en Catastro y RPP",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["search_results_check"]
            },
            {
                "step_id": "search_results_check",
                "name": "Verificación de Resultados",
                "step_type": "conditional",
                "description": "Verificar si se encontró la propiedad",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["verify_linking_status", "property_not_found"]
            },
            {
                "step_id": "verify_linking_status",
                "name": "Verificar Estado de Vinculación",
                "step_type": "integration",
                "description": "Verificar que los registros estén correctamente vinculados",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["analyze_lien_status"]
            },
            {
                "step_id": "analyze_lien_status",
                "name": "Analizar Estado de Gravámenes",
                "step_type": "action",
                "description": "Analizar información de gravámenes de ambos sistemas",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["lien_analysis_result"]
            },
            {
                "step_id": "lien_analysis_result",
                "name": "Resultado de Análisis de Gravámenes",
                "step_type": "conditional",
                "description": "Evaluar si la propiedad está libre de gravámenes",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["generate_clean_certificate", "generate_lien_report"]
            },
            {
                "step_id": "generate_clean_certificate",
                "name": "Generar Certificado Libre",
                "step_type": "action",
                "description": "Generar certificado oficial de libertad de gravamen",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["sign_certificate"]
            },
            {
                "step_id": "generate_lien_report",
                "name": "Generar Reporte de Gravámenes",
                "step_type": "action",
                "description": "Generar reporte detallado de gravámenes encontrados",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["sign_certificate"]
            },
            {
                "step_id": "sign_certificate",
                "name": "Firmar Certificado",
                "step_type": "action",
                "description": "Aplicar firma digital al certificado",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": ["certificado_emitido"]
            },
            {
                "step_id": "certificado_emitido",
                "name": "Certificado Emitido",
                "step_type": "terminal",
                "description": "Certificado de libertad de gravamen emitido exitosamente",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": []
            },
            {
                "step_id": "property_not_found",
                "name": "Propiedad No Encontrada",
                "step_type": "terminal",
                "description": "No se pudo localizar la propiedad con los criterios proporcionados",
                "required_inputs": [],
                "optional_inputs": [],
                "next_steps": []
            }
        ],
        "start_step_id": "collect_search_criteria"
    }