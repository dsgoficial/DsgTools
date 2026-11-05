# -*- coding: utf-8 -*-
"""
Proteção contra recursos remotos e formulários perigosos em projeto de
terceiro (avaliação de segurança do CDCiber, 2026, achados 4.3, 4.4 e 4.6.2).
Configuração em securitySettings.
"""
from .layerInspector import LayerInspector, avaliarFormularioUi  # noqa: F401
from .networkGuard import NetworkGuard  # noqa: F401
