"""
Tests básicos para workflows PUENTE.
"""

import pytest
from puente_catastral.catastral_workflows import (
    create_actualizacion_catastral_workflow,
    create_certificado_libertad_workflow,
    create_avaluo_catastral_workflow
)


def test_actualizacion_catastral_workflow():
    """Test workflow de actualización catastral."""
    workflow = create_actualizacion_catastral_workflow()
    
    assert workflow["workflow_id"] == "actualizacion_catastral_v1"
    assert workflow["name"] == "Actualización Catastral Unificada"
    assert len(workflow["steps"]) > 0
    assert workflow["start_step_id"] == "collect_catastral_data"


def test_certificado_libertad_workflow():
    """Test workflow de certificado de libertad."""
    workflow = create_certificado_libertad_workflow()
    
    assert workflow["workflow_id"] == "certificado_libertad_v1"
    assert workflow["name"] == "Certificado de Libertad de Gravamen"
    assert len(workflow["steps"]) > 0
    assert workflow["start_step_id"] == "collect_search_criteria"


def test_avaluo_catastral_workflow():
    """Test workflow de avalúo catastral."""
    workflow = create_avaluo_catastral_workflow()
    
    assert workflow["workflow_id"] == "avaluo_catastral_v1"
    assert workflow["name"] == "Avalúo Catastral Unificado"
    assert len(workflow["steps"]) > 0
    assert workflow["start_step_id"] == "collect_avaluo_request"