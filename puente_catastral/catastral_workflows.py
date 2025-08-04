"""
Workflows catastrales PUENTE para MuniStream.
Módulo principal que incorpora todos los workflows.
"""

from .actualizacion_catastral import create_actualizacion_catastral_workflow
from .certificado_libertad import create_certificado_libertad_workflow
from .avaluo_catastral import create_avaluo_catastral_workflow