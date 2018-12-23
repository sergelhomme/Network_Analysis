# -*- coding: utf-8 -*-
#-----------------------------------------------------------
#
# NetworkAnalysis
# Copyright Serge Lhomme
# EMAIL: serge.lhomme (at) u-pec.fr
# WEB  : http://sergelhomme.fr/deven.html
#
# Tools for analyzing networks characteristics
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
#---------------------------------------------------------------------

def classFactory(iface):
  from .network_analysis import NetworkAnalysis
  return NetworkAnalysis(iface)
