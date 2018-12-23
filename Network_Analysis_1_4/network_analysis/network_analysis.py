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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PyQt4 import QtXml
from qgis.gui import *

import os
import sys
currentPath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/tools'))
import networkx as nx
import community as com
import gravity as gravi
import operator
import numpy as np
import random
import itertools as iter
import csv
import processing
import urllib
import string
import copy
try :
    import scipy
    from scipy.cluster.hierarchy import ward, linkage, fcluster
    from scipy.spatial.distance import squareform, pdist
    global testscipy
    testscipy = 1
except : 
    global testscipy
    testscipy = 0
try :
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
    global testmatplotview
    testmatplotview = 1
except :
    testmatplotview = 0
try :
    import forceatlas as fca
except :
    "Catch error"

from testdialog import testDialog
from testdialog2 import testDialog2
from testdialog2b import testDialog2b
from testdialog3 import testDialog3
from testdialog4 import testDialog4
from testdialog5 import testDialog5
from testdialogstat import testDialogstat
from testdialogstat2 import testDialogstat2
from testdialogtool import testDialogtool
from testdialogtoolb import testDialogtoolb
from testdialogtool2 import testDialogtool2
from testdialogtoolTTP import testDialogtoolTTP
from testdialogtooldraw import testDialogtooldraw
from testdialogtoollc import testDialogtoollc
from testdialogdraw2 import testDialogdraw2
from testdialogtoolID import testDialogtoolID
from testdialogtoolET import testDialogtoolET
from testdialogtoolGS import testDialogtoolGS
if testmatplotview == 1 :
    from testmatplot import testMatplot
    from testmatplot2 import testMatplot2

class NetworkAnalysis:

  def __init__(self, iface):
    self.iface = iface

  def initGui(self):
    self.action = QAction("Basic Analysis", self.iface.mainWindow())
    QObject.connect(self.action, SIGNAL("activated()"), self.run)
    self.actionb = QAction("Vulnerability Analysis", self.iface.mainWindow())
    QObject.connect(self.actionb, SIGNAL("activated()"), self.runb)
    self.actionc = QAction("Community Detection / Partition", self.iface.mainWindow())
    QObject.connect(self.actionc, SIGNAL("activated()"), self.runc)
    self.actiond = QAction("Network Optimization", self.iface.mainWindow())
    QObject.connect(self.actiond, SIGNAL("activated()"), self.rund)
    self.actione = QAction("Statistics", self.iface.mainWindow())
    QObject.connect(self.actione, SIGNAL("activated()"), self.rune)
    self.actionf = QAction("Tools", self.iface.mainWindow())
    QObject.connect(self.actionf, SIGNAL("activated()"), self.runf)

    self.iface.addPluginToMenu("&Network Analysis...", self.action)
    self.iface.addPluginToMenu("&Network Analysis...", self.actionb)
    self.iface.addPluginToMenu("&Network Analysis...", self.actionc)
    self.iface.addPluginToMenu("&Network Analysis...", self.actiond)
    self.iface.addPluginToMenu("&Network Analysis...", self.actione)
    self.iface.addPluginToMenu("&Network Analysis...", self.actionf)

  def unload(self):
    self.iface.removePluginMenu("&Network Analysis...",self.action)
    self.iface.removePluginMenu("&Network Analysis...",self.actionb)
    self.iface.removePluginMenu("&Network Analysis...",self.actionc)
    self.iface.removePluginMenu("&Network Analysis...",self.actiond)
    self.iface.removePluginMenu("&Network Analysis...",self.actione)
    self.iface.removePluginMenu("&Network Analysis...",self.actionf)
  #----------------------------------------------------------------------------------------------------------------------------------------                 Basic Analysis             ----------------------------------------------------------------------------------------------------------------------------------- 
  def run(self): 
        global canvas
        canvas = self.iface.mapCanvas()
        global allLayers
        allLayers = canvas.layers()
        global count
        count = canvas.layerCount()
        global lay
        lay=[]
        for i in allLayers:
           lay=lay+[str(i.name())]
        global table_noeud
        self.dlg = testDialog(self.iface.mainWindow())
        self.dlg.ui.comboBox.addItems(lay)
        self.dlg.ui.comboBox_2.addItems(lay)
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("accepted()"), self.calcul)
        self.dlg.show()

  def calcul(self):
        typ, ok = QInputDialog.getItem(None,"Indicator Type","Nodes indicator or Edges indicator ?", ["Nodes", "Edges"], editable = False)       
        table_noeud=self.dlg.ui.comboBox.currentText()
        table_arc=self.dlg.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        fields2=[""]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
          fields2=fields2+[str(field[i].name())]
        if ok :
            if str(typ) == "Nodes" :
                self.dlg2 = testDialog2(self.iface.mainWindow())
                self.dlg2.ui.comboBox.addItems(fields)
                self.dlg2.ui.comboBox_2.addItems(fields)
                self.dlg2.ui.comboBox_3.addItems(["No","Yes"])
                self.dlg2.ui.comboBox_4.addItems(["No","Yes"])
                self.dlg2.ui.comboBox_5.addItems(fields2)
                self.dlg2.ui.comboBox_6.addItems(["Degree","Closeness","Fareness","Betweenness","Clustering","Eigenvector", "Square_clustering", "Eccentricity", "Page_rank", "Average_neighbor_degree", "Hub_dependence", "Core_Number", "Closeness_vitality"])  
                self.dlg2.ui.comboBox_7.addItems(["Yes","No"])
                QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2)
                self.dlg2.show()
            if str(typ) == "Edges" :
                self.dlg2 = testDialog2(self.iface.mainWindow())
                self.dlg2.ui.comboBox.addItems(fields)
                self.dlg2.ui.comboBox_2.addItems(fields)
                self.dlg2.ui.comboBox_3.addItems(["No","Yes"])
                self.dlg2.ui.comboBox_4.addItems(["No","Yes"])
                self.dlg2.ui.comboBox_5.addItems(fields2)
                self.dlg2.ui.comboBox_6.addItems(["Betweenness", "Current-Flow Betweenness", "Indice de cohesion", "Degree", "Flow_Analysis", "Gravity"])  
                self.dlg2.ui.comboBox_7.addItems(["Yes","No"])
                QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2arc)
                self.dlg2.show()

  def calcul2(self):
        arc_start=self.dlg2.ui.comboBox.currentText()
        arc_end=self.dlg2.ui.comboBox_2.currentText()
        oriente=self.dlg2.ui.comboBox_3.currentText()
        poids=self.dlg2.ui.comboBox_4.currentText()
        ponderation=self.dlg2.ui.comboBox_5.currentText()
        indicateur=self.dlg2.ui.comboBox_6.currentText()
        norm=self.dlg2.ui.comboBox_7.currentText()
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        table=[]
        if str(poids)=="No":
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          table=table+[(attrsstart,attrsend)] 
         G=nx.Graph()
         if str(oriente)=="Yes" :
          G=nx.DiGraph()
         G.add_edges_from(table)
        if str(poids)=="Yes":
         distind=provider.fieldNameIndex(str(ponderation))
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind,distind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          attrsdist=feat.attributes()[distind]
          table=table+[(attrsstart,attrsend,attrsdist)] 
         G=nx.Graph()
         if str(oriente)=="Yes" :
          G=nx.DiGraph()
         G.add_weighted_edges_from(table)
        t=nx.number_of_nodes(G)
        if str(indicateur)=="Betweenness" and str(poids)=="No" and str(norm)=="No" :
            b=nx.betweenness_centrality(G,normalized=False)
        if str(indicateur)=="Betweenness" and str(poids)=="Yes" and str(norm)=="No" :
            b=nx.betweenness_centrality(G, normalized=False, weight='weight')
        if str(indicateur)=="Betweenness" and str(poids)=="No" and str(norm)=="Yes" :
            b=nx.betweenness_centrality(G)
        if str(indicateur)=="Betweenness" and str(poids)=="Yes" and str(norm)=="Yes" :
            b=nx.betweenness_centrality(G,weight='weight')
        if str(indicateur)=="Eigenvector" and str(oriente)=="No" and str(norm)=="Yes" :
            b=nx.eigenvector_centrality(G)
        if str(indicateur)=="Eigenvector" and str(oriente)=="Yes" and str(norm)=="Yes" :
            b=nx.eigenvector_centrality(G)
            G2=nx.reverse(G, copy=True)
            b2=nx.eigenvector_centrality(G2)
        if str(indicateur)=="Eigenvector" and str(norm)=="No" :
            QMessageBox.information(None, " Message : ", "Eigenvector need to be normalized.")
            b=77777
        if str(indicateur)=="Closeness" and str(poids)=="No" and str(norm)=="No":
            b=nx.closeness_centrality(G, normalized=False)
        if str(indicateur)=="Closeness" and str(poids)=="Yes" and str(norm)=="No":
            b=nx.closeness_centrality(G, normalized=False, distance='weight')
        if str(indicateur)=="Closeness" and str(poids)=="No" and str(norm)=="Yes":
            b=nx.closeness_centrality(G, normalized=True)
        if str(indicateur)=="Closeness" and str(poids)=="Yes" and str(norm)=="Yes":
            b=nx.closeness_centrality(G, normalized= True, distance='weight')
        if str(indicateur)=="Clustering" and str(poids)=="No" and str(oriente)=="No" and str(norm)=="Yes":
            b=nx.clustering(G)
        if str(indicateur)=="Clustering" and str(poids)=="Yes" and str(oriente)=="No" and str(norm)=="Yes":
            b=nx.clustering(G, weight='weight')
        if str(indicateur)=="Clustering" and str(oriente)=="Yes":
            QMessageBox.information(None, " Message : ", "Here, edges need to be undirected.")
            b=77777
        if str(indicateur)=="Clustering" and str(norm)=="No":
            QMessageBox.information(None, " Message : ", "Clustering coefficient indices need to be normalized.")
            b=77777
        if str(indicateur)=="Square_clustering" and str(poids)=="No" and str(oriente)=="No" and str(norm)=="Yes":
            b=nx.square_clustering(G)
        if str(indicateur)=="Square_clustering" and str(poids)=="Yes" and str(oriente)=="No" and str(norm)=="Yes":
            QMessageBox.information(None, " Message : ", "Need to be implemented.")
            b=77777
        if str(indicateur)=="Square_clustering" and str(oriente)=="Yes":
            QMessageBox.information(None, " Message : ", "Graph needs to be undirected.")
            b=77777
        if str(indicateur)=="Square_clustering" and str(norm)=="No":
            QMessageBox.information(None, " Message : ", "Square clustering coefficient needs to be normalized.")
            b=77777
        if str(indicateur)=="Eccentricity" and str(norm)=="Yes":
            QMessageBox.information(None, " Message : ", "Try with no normalization.")
            b=77777
        if str(indicateur)=="Eccentricity" and str(norm)=="No" and str(poids)=="No":
            spl=nx.shortest_path_length(G)
            try:
                 b=nx.eccentricity(G, sp=spl)
            except nx.NetworkXError as e:
                 b=77777
                 QMessageBox.information(None, " Message : ", "Error : " + str(e))
        if str(indicateur)=="Eccentricity" and str(norm)=="No" and str(poids)=="Yes":
            spl=nx.shortest_path_length(G, weight='weight')
            try :
                 b=nx.eccentricity(G, sp=spl)
            except nx.NetworkXError as e:
                 b=77777
                 QMessageBox.information(None, " Message : ", "Error : " + str(e))
        if str(indicateur)=="Page_rank" and str(poids)=="No" and str(norm)=="Yes":
            b=nx.pagerank(G)
        if str(indicateur)=="Page_rank" and str(poids)=="Yes" and str(norm)=="Yes":
            b=nx.pagerank(G, weight='weight')
        if str(indicateur)=="Page_rank" and str(norm)=="No":
            QMessageBox.information(None, " Message : ", "Page rank indices need to be normalized.")
            b=77777
        if str(indicateur)=="Average_neighbor_degree" and str(poids)=="No" and str(norm)=="No":
            b=nx.average_neighbor_degree(G)
        if str(indicateur)=="Average_neighbor_degree" and str(poids)=="Yes" and str(norm)=="No":
            b=nx.average_neighbor_degree(G, weight='weight')
        if str(indicateur)=="Average_neighbor_degree" and str(norm)=="Yes":
            QMessageBox.information(None, " Message : ", "Average neighbor degree indices can not be normalized.")
            b=77777
        if str(indicateur)=="Hub_dependence" and str(oriente)=="No" and str(norm)=="Yes" and str(poids)=="Yes":
            t=nx.number_of_nodes(G)
            b=[0]*(t+1)
            for j in range(t):
               num=j+1
               listarc=G.edges(int(num),data=True)
               b2=[0]*(t+1)
               tot=0
               for i in range(len(listarc)):
                    w=listarc[i][2]
                    w2=w['weight']
                    b2[listarc[i][0]]=b2[listarc[i][0]]+w2
                    b2[listarc[i][1]]=b2[listarc[i][1]]+w2
                    tot=tot+w2
               b3=sorted(b2)
               if b3[t]!=0:
                  cal=b3[t-1]/float(b3[t])
               if b3[t]==0:
                  cal=NULL
               b2=[0]*(t+1)
               b[num]=cal
        if str(indicateur)=="Hub_dependence" and str(oriente)=="Yes" and str(norm)=="Yes" and str(poids)=="Yes":
            b=[0]*(t+1)
            bbb=[0]*(t+1)
            for j in range(t):
               num=j+1
               listarcout=G.out_edges(int(num),data=True)
               b2=[0]*(t+1)
               tot=0
               for i in range(len(listarcout)):
                    w=listarcout[i][2]
                    w2=w['weight']
                    b2[listarcout[i][0]]=b2[listarcout[i][0]]+w2
                    b2[listarcout[i][1]]=b2[listarcout[i][1]]+w2
                    tot=tot+w2
               b3=sorted(b2)
               if b3[t]!=0:
                  cal=b3[t-1]/float(b3[t])
               if b3[t]==0:
                  cal=NULL
               b2=[0]*(t+1)
               b[num]=cal
            for j in range(t):
               num=j+1
               listarcin=G.in_edges(int(num),data=True)
               b2=[0]*(t+1)
               tot=0
               for i in range(len(listarcin)):
                    w=listarcin[i][2]
                    w2=w['weight']
                    b2[listarcin[i][0]]=b2[listarcin[i][0]]+w2
                    b2[listarcin[i][1]]=b2[listarcin[i][1]]+w2
                    tot=tot+w2
               b3=sorted(b2)
               if b3[t]!=0:
                  cal=b3[t-1]/float(b3[t])
               if b3[t]==0:
                  cal=NULL
               b2=[0]*(t+1)
               bbb[num]=cal
            indicateur="Out_Hub_dependence"
        if str(indicateur)=="Hub_dependence" and str(norm)=="No":
            QMessageBox.information(None, " Message : ", "Hub dependence indices need to be normalized.")
            b=77777
        if str(indicateur)=="Hub_dependence" and str(poids)=="No":
            QMessageBox.information(None, " Message : ", "Weighted graph is necessary.")
            b=77777
        if str(indicateur)=="Closeness_vitality" and str(poids)=="No" and str(norm)=="No":
            b=nx.closeness_vitality(G)
        if str(indicateur)=="Closeness_vitality" and str(poids)=="Yes" and str(norm)=="No":
            b=nx.closeness_vitality(G, weight='weight')
        if str(indicateur)=="Closeness_vitality" and str(norm)=="Yes":
            QMessageBox.information(None, " Message : ", "No normalization for closeness vitality.")	
            b=77777
        if str(indicateur)=="Fareness" and str(poids)=="No" and str(norm)=="No":
            spl=nx.shortest_path_length(G)
            b2=[0]*len(G.nodes())
            try:
              for i in range(len(G.nodes())):
                 for j in range(len(G.nodes())):
                     b2[i]=b2[i]+(spl[i+1][j+1]/(2*(float(t)-1)))
                     b2[j]=b2[j]+(spl[i+1][j+1]/(2*(float(t)-1)))
              err=0
            except :
                 QMessageBox.information(None, " Message : ","Graph not connected: infinite path length")
                 err=1
            b=77777
        if str(indicateur)=="Fareness" and str(poids)=="Yes" and str(norm)=="No":
            spl=nx.shortest_path_length(G, weight='weight')
            b2=[0]*len(G.nodes())
            try:
              for i in range(len(G.nodes())):
                 for j in range(len(G.nodes())):
                     b2[i]=b2[i]+(spl[i+1][j+1]/(2*(float(t)-1)))
                     b2[j]=b2[j]+(spl[i+1][j+1]/(2*(float(t)-1)))
              err=0
            except :
                 QMessageBox.information(None, " Message : ","Graph not connected: infinite path length")
                 err=1
            b=77777
        if str(indicateur)=="Fareness" and str(norm)=="Yes":
            QMessageBox.information(None, " Message : ", "No normalization for fareness.")
            b=77777
        if str(indicateur)=="Degree" and str(norm)=="No" and str(oriente)=="No" and str(poids)=="No":
            b=G.degree()
        if str(indicateur)=="Degree" and str(norm)=="No" and str(oriente)=="No" and str(poids)=="Yes":
            b=G.degree(weight='weight')
        if str(indicateur)=="Degree" and str(norm)=="Yes" and str(oriente)=="No" and str(poids)=="No":
            b=nx.degree_centrality(G)
        if str(indicateur)=="Degree" and str(norm)=="Yes" and str(oriente)=="No" and str(poids)=="Yes":
            QMessageBox.information(None, " Message : ", "Not implemented in this version")
            b=77777
        if str(indicateur)=="Degree" and str(norm)=="Yes" and str(oriente)=="Yes":
            QMessageBox.information(None, " Message : ", "No normalization for degree if graph is oriented.")
            b=77777
        if str(indicateur)=="Degree" and str(norm)=="No" and str(oriente)=="Yes" and str(poids)=="Yes":
            b=G.degree(weight='weight')
            b2=G.out_degree(weight='weight')
            b3=G.in_degree(weight='weight')
        if str(indicateur)=="Degree" and str(norm)=="No" and str(oriente)=="Yes" and str(poids)=="No":
            b=G.degree()
            b2=G.out_degree()
            b3=G.in_degree()
        if str(indicateur)=="Core_Number" and str(norm)=="Yes":
            QMessageBox.information(None, " Message : ", "No normalization for core number.")
            b = 77777
        if str(indicateur)=="Core_Number" and str(norm)=="No":
            b = nx.core_number(G)
            if str(poids)=="Yes":
                QMessageBox.information(None, " Message : ", "This indicator does not take into account weight")
        if b!=77777 :
         taille=t
         aLayer2 = allLayers[int(ind_noeud)]
         provider2 = aLayer2.dataProvider()
         nbcol=int(provider2.fields().count())
         provider2.addAttributes([QgsField(str(indicateur), QVariant.Double)])
         aLayer2.startEditing()
         for k in range(taille):
           aLayer2.changeAttributeValue(k,nbcol,b[k+1])
         aLayer2.commitChanges()
        if str(indicateur)=="Fareness" and str(norm)=="No" :
         if err==0: 
          taille=t
          aLayer2 = allLayers[int(ind_noeud)]
          provider2 = aLayer2.dataProvider()
          nbcol=int(provider2.fields().count())
          provider2.addAttributes([QgsField(str(indicateur), QVariant.Double)])
          aLayer2.startEditing()
          for k in range(taille):
            aLayer2.changeAttributeValue(k,nbcol,float(b2[k]))
          aLayer2.commitChanges()
        if str(indicateur)=="Out_Hub_dependence":
         taille=t
         aLayer2 = allLayers[int(ind_noeud)]
         provider2 = aLayer2.dataProvider()
         nbcol=int(provider2.fields().count())
         provider2.addAttributes([QgsField("In_Hub_dependence", QVariant.Double)])
         aLayer2.startEditing()
         for k in range(taille):
           aLayer2.changeAttributeValue(k,nbcol,bbb[k+1])
         aLayer2.commitChanges()
        if str(indicateur)=="Eigenvector" and str(oriente)=="Yes" :
         taille=len(b)
         aLayer2 = allLayers[int(ind_noeud)]
         provider2 = aLayer2.dataProvider()
         nbcol=int(provider2.fields().count())
         provider2.addAttributes([QgsField("Left_Eigenvector", QVariant.Double)])
         aLayer2.startEditing()
         for k in range(taille):
           aLayer2.changeAttributeValue(k,nbcol,float(b2[k+1]))
         aLayer2.commitChanges()
        if str(indicateur)=="Degree" and str(norm)=="No" and str(oriente)=="Yes":
             taille=len(b)
             aLayer2 = allLayers[int(ind_noeud)]
             provider2 = aLayer2.dataProvider()
             provider2.addAttributes([QgsField("out_degree", QVariant.Double)])
             aLayer2.startEditing()
             for k in range(taille):
                 aLayer2.changeAttributeValue(k,nbcol+1,b2[k+1])
             aLayer2.commitChanges() 
             taille=len(b)
             aLayer2 = allLayers[int(ind_noeud)]
             provider2 = aLayer2.dataProvider()
             provider2.addAttributes([QgsField("in_degree", QVariant.Double)])
             aLayer2.startEditing()
             for k in range(taille):
                 aLayer2.changeAttributeValue(k,nbcol+2,b3[k+1])
             aLayer2.commitChanges() 
        QMessageBox.information(None, " Message : ", "End")

  def calcul2arc(self):
        arc_start=self.dlg2.ui.comboBox.currentText()
        arc_end=self.dlg2.ui.comboBox_2.currentText()
        oriente=self.dlg2.ui.comboBox_3.currentText()
        poids=self.dlg2.ui.comboBox_4.currentText()
        ponderation=self.dlg2.ui.comboBox_5.currentText()
        indicateur=self.dlg2.ui.comboBox_6.currentText()
        norm=self.dlg2.ui.comboBox_7.currentText()
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        table=[]
        if str(poids)=="No":
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          table=table+[(attrsstart,attrsend)] 
         G=nx.Graph()
         if str(oriente)=="Yes" :
          G=nx.DiGraph()
         G.add_edges_from(table)
        if str(poids)=="Yes":
         distind=provider.fieldNameIndex(str(ponderation))
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind,distind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          attrsdist=feat.attributes()[distind]
          table=table+[(attrsstart,attrsend,attrsdist)] 
         G=nx.Graph()
         if str(oriente)=="Yes" :
          G=nx.DiGraph()
         G.add_weighted_edges_from(table)
        t=nx.number_of_nodes(G)
        if str(indicateur)=="Betweenness" and str(poids)=="No" and str(norm)=="No" :
            b=nx.edge_betweenness_centrality(G,normalized=False)
        if str(indicateur)=="Betweenness" and str(poids)=="Yes" and str(norm)=="No" :
            b=nx.edge_betweenness_centrality(G, normalized=False, weight='weight')
        if str(indicateur)=="Betweenness" and str(poids)=="No" and str(norm)=="Yes" :
            b=nx.edge_betweenness_centrality(G)
        if str(indicateur)=="Betweenness" and str(poids)=="Yes" and str(norm)=="Yes" :
            b=nx.edge_betweenness_centrality(G,weight='weight')
        if str(indicateur)=="Current-Flow Betweenness" and str(poids)=="No" and str(norm)=="No" and str(oriente)=="No" :
            b=nx.edge_current_flow_betweenness_centrality(G,normalized=False)
        if str(indicateur)=="Current-Flow Betweenness" and str(poids)=="Yes" and str(norm)=="No" and str(oriente)=="No":
            b=nx.edge_current_flow_betweenness_centrality(G, normalized=False, weight='weight')
        if str(indicateur)=="Current-Flow Betweenness" and str(poids)=="No" and str(norm)=="Yes" and str(oriente)=="No":
            b=nx.edge_current_flow_betweenness_centrality(G)
        if str(indicateur)=="Current-Flow Betweenness"  and str(poids)=="Yes" and str(norm)=="Yes" and str(oriente)=="No":
            b=nx.edge_current_flow_betweenness_centrality(G,weight='weight')
        if str(indicateur)=="Current-Flow Betweenness" and str(oriente)=="Yes":
            b=77777
            QMessageBox.information(None, " Message : ", "No implementation for directed graph.")
        if str(indicateur)=="Degree" and str(oriente)=="No" and str(poids)=="No" and str(norm)=="No":
            b = dict()
            deg = G.degree()
            for i in range(len(table)):
                b[table[i][0],table[i][1]] = deg[int(table[i][0])] + deg[int(table[i][1])] - 2
        if str(indicateur)=="Degree" and str(oriente)=="No" and str(poids)=="Yes" and str(norm)=="No":
            b = dict()
            deg=G.degree(weight='weight')
            for i in range(len(table)):
                b[table[i][0],table[i][1]] = deg[int(table[i][0])] + deg[int(table[i][1])] - (2 * table[i][2])
        if str(indicateur)=="Degree" and str(oriente)=="Yes" and str(poids)=="No" and str(norm)=="No":
            b = dict()
            b2 = dict()
            b2b = dict()
            b3 = dict()
            b3b = dict()
            deg = G.degree()
            deg3 = G.out_degree()
            deg2 = G.in_degree()
            for i in range(len(table)):
                b[table[i][0],table[i][1]] = deg[int(table[i][0])] + deg[int(table[i][1])] - 2
                b2[table[i][0],table[i][1]] = deg2[int(table[i][0])] 
                b2b[table[i][0],table[i][1]] = deg3[int(table[i][0])] - 1 
                b3[table[i][0],table[i][1]] = deg2[int(table[i][1])] - 1 
                b3b[table[i][0],table[i][1]] = deg3[int(table[i][1])] 
        if str(indicateur)=="Degree" and str(oriente)=="Yes" and str(poids)=="Yes" and str(norm)=="No":
            b = dict()
            b2 = dict()
            b2b = dict()
            b3 = dict()
            b3b = dict()
            deg = G.degree(weight='weight')
            deg3 = G.out_degree(weight='weight')
            deg2 = G.in_degree(weight='weight')
            for i in range(len(table)):
                b[table[i][0],table[i][1]] = deg[int(table[i][0])] + deg[int(table[i][1])] - (2 * table[i][2])
                b2[table[i][0],table[i][1]] = deg2[int(table[i][0])] 
                b2b[table[i][0],table[i][1]] = deg3[int(table[i][0])] -  table[i][2] 
                b3[table[i][0],table[i][1]] = deg2[int(table[i][1])] -  table[i][2] 
                b3b[table[i][0],table[i][1]] = deg3[int(table[i][1])] 
        if str(indicateur)=="Degree" and str(norm)=="Yes":
            b = 77777
            QMessageBox.information(None, " Message : ", "No normalization here.")
        if str(indicateur)=="Indice de cohesion" and str(norm)=="Yes" and str(poids)=="No":
            b = dict()
            for i in range(len(table)):
                noeud1=table[i][0]
                noeud2=table[i][1]
                neib1=G.neighbors(noeud1)
                neib2=G.neighbors(noeud2)
                val=0
                for j in range(len(neib1)):
                    for k in range(len(neib2)):
                        if neib1[j]==neib2[k]:
                            val = val + 1
                b[table[i][0],table[i][1]] = (2*val)/float((len(neib1)-1)+(len(neib2)-1))
        if str(indicateur)=="Indice de cohesion" and str(norm)=="No" :
            b = 77777
            QMessageBox.information(None, " Message : ", "Indice de cohesion needs to be normalized.")
        if str(indicateur)=="Indice de cohesion" and str(poids)=="Yes" :
            b = 77777
            QMessageBox.information(None, " Message : ", "Indice de cohesion doesn't take into account weights. Try again.")
        if str(indicateur)=="Flow_Analysis" and str(poids) == "Yes" :
            atable = np.array(table)
            tot = sum(atable[:,2])
            tritable=sorted(table, reverse=True, key=operator.itemgetter(2))
            b = dict() #rank
            b2 = dict() #tx
            b3 = dict() #txcum
            b4 = dict() #rank_start_Node
            b5 = dict() #rank_end_Node
            b6 = dict() #best_rank
            b[tritable[0][0],tritable[0][1]] = 1
            b2[tritable[0][0],tritable[0][1]] = tritable[0][2] / float(tot)
            b3[tritable[0][0],tritable[0][1]] = tritable[0][2] / float(tot)
            b4[tritable[0][0],tritable[0][1]] = 1
            b5[tritable[0][0],tritable[0][1]] = 1
            b6[tritable[0][0],tritable[0][1]] = 1
            classnode = [1] * len(G.nodes())
            classnode[tritable[0][0]-1] = classnode[tritable[0][0]-1] + 1
            classnode[tritable[0][1]-1] = classnode[tritable[0][1]-1] + 1	
            if str(oriente) == "Yes":
                b7 = dict()#In_rank
                b8 = dict()#Out_rank
                b7[tritable[0][0],tritable[0][1]] = 1
                b8[tritable[0][0],tritable[0][1]] = 1
                classnodeIn = [1] * len(G.nodes())
                classnodeOut = [1] * len(G.nodes())		
                classnodeOut[tritable[0][0]-1] = classnodeOut[tritable[0][0]-1] + 1
                classnodeIn[tritable[0][1]-1] = classnodeIn[tritable[0][1]-1] + 1				
            stock = tritable[0][2]
            for i in range(len(table)-1):
                if tritable[i+1][2] != tritable[i][2] :
                    b[tritable[i+1][0],tritable[i+1][1]] = i + 2
                if tritable[i+1][2] == tritable[i][2] :
                    b[tritable[i+1][0],tritable[i+1][1]] = b[tritable[i][0],tritable[i][1]]
                b2[tritable[i+1][0],tritable[i+1][1]] = tritable[i+1][2] / float(tot)
                b3[tritable[i+1][0],tritable[i+1][1]] = (stock + tritable[i+1][2]) / float(tot)
                b4[tritable[i+1][0],tritable[i+1][1]] = classnode[tritable[i+1][0]-1]
                b5[tritable[i+1][0],tritable[i+1][1]] = classnode[tritable[i+1][1]-1]
                if classnode[tritable[i+1][0]-1] <= classnode[tritable[i+1][1]-1] :
                    b6[tritable[i+1][0],tritable[i+1][1]] = classnode[tritable[i+1][0]-1]
                if classnode[tritable[i+1][1]-1] < classnode[tritable[i+1][0]-1] :
                    b6[tritable[i+1][0],tritable[i+1][1]] = classnode[tritable[i+1][1]-1]
                classnode[tritable[i+1][0]-1] = classnode[tritable[i+1][0]-1] + 1
                classnode[tritable[i+1][1]-1] = classnode[tritable[i+1][1]-1] + 1
                if str(oriente) == "Yes" :
                    b7[tritable[i+1][0],tritable[i+1][1]] = classnodeIn[tritable[i+1][1]-1]
                    b8[tritable[i+1][0],tritable[i+1][1]] = classnodeOut[tritable[i+1][0]-1]	
                    classnodeOut[tritable[i+1][0]-1] = classnodeOut[tritable[i+1][0]-1] + 1
                    classnodeIn[tritable[i+1][1]-1] = classnodeIn[tritable[i+1][1]-1] + 1
                stock = stock + tritable[i+1][2]
        if str(indicateur)=="Flow_Analysis" and str(poids) == "No" :
            b = 77777
            QMessageBox.information(None, " Message : ", "Flow Analysis requires weights")
        if str(indicateur)=="Gravity" and poids == "Yes" :
            b = 77777
            b2 = 0
            testzero,ok1 = QInputDialog.getItem(None,"Model","Missing values as zero ? : ", ["Yes","No"], editable = False)
            if ok1 :
                if testzero == "No" :
                    fielddist,ok = QInputDialog.getItem(None,"Distance Field","Choose your distance field : ", fields, editable = False)
                    if ok :
                        distind = provider.fieldNameIndex(str(fielddist))
                        dist = []
                        feat = QgsFeature()
                        fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([distind]) )
                        while fit1.nextFeature(feat):
                            dist = dist + [float(feat.attributes()[distind])]
                        if str(oriente) == "Yes" :
                            met,ok2 = QInputDialog.getItem(None,"Method","Choose your method : ", ["Total interaction constrained","Double Constrained"], editable = False)
                            if ok2 :
                                if met == "Total interaction constrained" :
                                    res, val, al = gravi.gravitaire_oriente_uncomplete(G,table,dist)
                                    QMessageBox.information(None, " Message : ", "R = " + str(val[0][1])+"<br> Alpha = " + str(al) )
                                    b = list(res)
                                if met == "Double Constrained" :
                                    num,ok3 = QInputDialog.getInt(None,"Iteration","Enter the number of iterations : ", 100)
                                    if ok3 :
                                        res, val, al = gravi.gravitaire_oriente_uncomplete2(G,table,dist,num)
                                        b = list(res)
                                        QMessageBox.information(None, " Message : ", "R = " + str(val[0][1])+"<br> Alpha = " + str(al) )
                        if str(oriente) == "No" :
                            met,ok2 = QInputDialog.getItem(None,"Method","Choose your method : ", ["Total interaction constrained","Double Constrained"], editable = False)
                            if ok2 :
                                if met == "Total interaction constrained" :
                                    res, val, al = gravi.gravitaire_uncomplete(G,table,dist)
                                    QMessageBox.information(None, " Message : ", "R = " + str(val[0][1])+"<br> Alpha = " + str(al) )
                                    b = list(res)
                                if met == "Double Constrained" :
                                    num,ok3 = QInputDialog.getInt(None,"Iteration","Enter the number of iterations : ", 100)
                                    if ok3 :
                                        res, val, al = gravi.gravitaire_uncomplete2(G,table,dist,num)
                                        b = list(res)
                                        QMessageBox.information(None, " Message : ", "R = " + str(val[0][1])+"<br> Alpha = " + str(al) )
                if testzero == "Yes" :
                    geom = []
                    x = []
                    y = []
                    feat2 = QgsFeature()
                    aLayer2 = allLayers[int(ind_noeud)]
                    provider2 = aLayer2.dataProvider()
                    fit2 = provider2.getFeatures()
                    while fit2.nextFeature(feat2):
                        geom = geom + [feat2.geometry().exportToWkt()]
                        x = x + [feat2.geometry().asPoint().x()]
                        y = y + [feat2.geometry().asPoint().y()]
                    if str(oriente)=="No" :
                        tablenew = []
                        dist = []
                        id = []
                        for i in range(len(geom)- 1) :
                            for j in range(len(geom)- i - 1):
                                id = id + [[i+1 , i+j+2]]
                                tablenew = tablenew + [[i+1 , i+j+2 , 0]]
                                dist = dist + [ np.sqrt( ((x[i]-x[i+j+1]) * (x[i]-x[i+j+1])) + ((y[i]-y[i+j+1]) * (y[i]-y[i+j+1])) ) ]
                        dist2 = []
                        for i in range(len(table)) :
                            try :
                                u = id.index([int(table[i][0]),int(table[i][1])])
                            except :
                                u = id.index([int(table[i][1]),int(table[i][0])])
                            tablenew[u][2] = table[i][2]
                            dist2 = dist2 + [dist[u]]
                        Gnew = nx.Graph()
                        Gnew.add_weighted_edges_from(tablenew)
                        met,ok2 = QInputDialog.getItem(None, "Method", "Choose your method : ", ["Total interaction constrained","Double Constrained"], editable = False)
                        if ok2 :
                            if met == "Total interaction constrained" :
                                res, val, al = gravi.gravitaire(Gnew,tablenew,table,dist,dist2)
                                b2 = list(res)
                                QMessageBox.information(None, " Message : ", "R = " + str(val[0][1])+"<br> Alpha = " + str(al) )
                            if met == "Double Constrained" :
                                num,ok3 = QInputDialog.getInt(None,"Iteration","Enter the number of iterations : ", 100)
                                if ok3 :
                                    res, val, al = gravi.gravitaire2(Gnew,tablenew,table,dist,dist2,num)
                                    b2 = list(res)
                                    QMessageBox.information(None, " Message : ", "R = " + str(val[0][1])+"<br> Alpha = " + str(al) )
                    if str(oriente)=="Yes":
                        tablenew = []
                        dist = []
                        id = []
                        for i in range(len(geom)) :
                            for j in range(len(geom)):
                                if i != j :
                                    id = id + [[i+1 , j+1]]
                                    tablenew = tablenew + [[i+1 , j+1 , 0]]
                                    dist = dist + [ np.sqrt( ((x[i]-x[j]) * (x[i]-x[j])) + ((y[i]-y[j]) * (y[i]-y[j])) ) ]
                        dist2 = []
                        for i in range(len(table)) :
                            u = id.index([int(table[i][0]),int(table[i][1])])
                            tablenew[u][2] = table[i][2]
                            dist2 = dist2 + [dist[u]]
                        Gnew = nx.DiGraph()
                        Gnew.add_weighted_edges_from(tablenew)
                        met,ok2 = QInputDialog.getItem(None, "Method", "Choose your method : ", ["Total interaction constrained","Double Constrained"], editable = False)
                        if ok2 :
                            if met == "Total interaction constrained" :
                                res, val, al = gravi.gravitaire_oriente(Gnew,tablenew,table,dist,dist2)
                                b2 = list(res)
                                QMessageBox.information(None, " Message : ", "R = " + str(val[0][1])+"<br> Alpha = " + str(al) )
                            if met == "Double Constrained" :
                                num,ok3 = QInputDialog.getInt(None,"Iteration","Enter the number of iterations : ", 100)
                                if ok3 :
                                    res, val, al = gravi.gravitaire_oriente2(Gnew,tablenew,table,dist,dist2,num)
                                    b2 = list(res)
                                    QMessageBox.information(None, " Message : ", "R = " + str(val[0][1])+"<br> Alpha = " + str(al) )
        if str(indicateur)=="Gravity" and str(poids) == "No" :
            b = 77777
            QMessageBox.information(None, " Message : ", "Gravity model requires weights")
        if b != 77777 and str(indicateur) == "Gravity" :
            nbcol=int(provider.fields().count())
            provider.addAttributes( [ QgsField(str(indicateur), QVariant.Double) ] )
            aLayer.startEditing()
            for i in range(len(table)):
                aLayer.changeAttributeValue(i,nbcol,float(b[i]))
            aLayer.commitChanges()
            b = 77777
        if b == 77777 and str(indicateur) == "Gravity" and b2 != 0 :
           epsg = canvas.mapRenderer().destinationCrs().authid()
           vl = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges", "memory")
           pr = vl.dataProvider()
           vl.startEditing()
           pr.addAttributes( [ QgsField("StartNode", QVariant.Int) ] )
           pr.addAttributes( [ QgsField("EndNode", QVariant.Int) ] )
           pr.addAttributes( [ QgsField("Flow", QVariant.Double) ] )
           pr.addAttributes( [ QgsField("Gravity", QVariant.Double) ] )
           vl.commitChanges()
           vl.startEditing()
           for i in range(len(b2)):
                fet = QgsFeature()
                fet.setGeometry( QgsGeometry.fromPolyline([ QgsPoint( float(x[tablenew[i][0]-1]) , float(y[tablenew[i][0]-1])) , QgsPoint( float(x[tablenew[i][1]-1]) , float(y[tablenew[i][1]-1])) ]) )
                fet.setAttributes( [ tablenew[i][0], tablenew[i][1], tablenew[i][2], float(b2[i]) ] )
                pr.addFeatures( [ fet ] ) 
           vl.commitChanges()
           QgsMapLayerRegistry.instance().addMapLayer(vl)
        if b != 77777 and str(indicateur) != "Flow_Analysis" :
            nbcol=int(provider.fields().count())
            provider.addAttributes( [ QgsField(str(indicateur), QVariant.Double) ] )
            aLayer.startEditing()
            for i in range(len(table)):
                try :
                    aLayer.changeAttributeValue(i,nbcol,float(b[table[i][0],table[i][1]]))
                except:
                    aLayer.changeAttributeValue(i,nbcol,float(b[table[i][1],table[i][0]]))
            aLayer.commitChanges()
            if str(indicateur) == "Degree" and str(oriente) == "Yes" :
                provider.addAttributes( [ QgsField("Deg_In_Out", QVariant.Double) ] )
                provider.addAttributes( [ QgsField("Deg_Out_Out", QVariant.Double) ] )
                provider.addAttributes( [ QgsField("Deg_In_In", QVariant.Double) ] )
                provider.addAttributes( [ QgsField("Deg_Out_In", QVariant.Double) ] )
                aLayer.startEditing()
                for i in range(len(table)):
                    aLayer.changeAttributeValue(i,nbcol + 1,float(b2[table[i][0],table[i][1]]))
                    aLayer.changeAttributeValue(i,nbcol + 2,float(b2b[table[i][0],table[i][1]]))
                    aLayer.changeAttributeValue(i,nbcol + 3,float(b3[table[i][0],table[i][1]]))
                    aLayer.changeAttributeValue(i,nbcol + 4,float(b3b[table[i][0],table[i][1]]))
                aLayer.commitChanges()
        if b != 77777 and str(indicateur) == "Flow_Analysis" :
            nbcol=int(provider.fields().count())
            provider.addAttributes( [ QgsField("Flow_Rank", QVariant.Int) ] )
            provider.addAttributes( [ QgsField("Flow_Ratio", QVariant.Double) ] )
            provider.addAttributes( [ QgsField("Flow_CumRatio", QVariant.Double) ] )
            provider.addAttributes( [ QgsField("Rank_SN", QVariant.Int) ] )
            provider.addAttributes( [ QgsField("Rank_EN", QVariant.Int) ] )
            provider.addAttributes( [ QgsField("Best_Node_Rank", QVariant.Int) ] )
            if str(oriente)=="Yes":
                provider.addAttributes( [ QgsField("In_rank", QVariant.Int) ] )
                provider.addAttributes( [ QgsField("Out_Rank", QVariant.Int) ] )
            aLayer.startEditing()
            for i in range(len(table)):
                aLayer.changeAttributeValue(i,nbcol,int(b[table[i][0],table[i][1]]))
                aLayer.changeAttributeValue(i,nbcol+1, b2[table[i][0],table[i][1]])
                aLayer.changeAttributeValue(i,nbcol+2, b3[table[i][0],table[i][1]])
                aLayer.changeAttributeValue(i,nbcol+3, int(b4[table[i][0],table[i][1]]))
                aLayer.changeAttributeValue(i,nbcol+4, int(b5[table[i][0],table[i][1]]))
                aLayer.changeAttributeValue(i,nbcol+5, int(b6[table[i][0],table[i][1]]))
                if str(oriente)=="Yes":
                    aLayer.changeAttributeValue(i,nbcol+6, int(b7[table[i][0],table[i][1]]))
                    aLayer.changeAttributeValue(i,nbcol+7, int(b8[table[i][0],table[i][1]]))
            aLayer.commitChanges()
        QMessageBox.information(None, " Message : ", "End")
  #----------------------------------------------------------------------------------------------------------------------------------------                Vulnerability Analysis             -----------------------------------------------------------------------------------------------------------------------------------
  def runb(self): 
        global canvas
        canvas = self.iface.mapCanvas()
        global allLayers
        allLayers = canvas.layers()
        global count
        count = canvas.layerCount()
        global lay
        lay=[]
        for i in allLayers:
           lay=lay+[str(i.name())]
        global table_noeud
        self.dlg = testDialog(self.iface.mainWindow())
        self.dlg.ui.comboBox.addItems(lay)
        self.dlg.ui.comboBox_2.addItems(lay)
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("accepted()"), self.calculb)
        self.dlg.show()

  def calculb(self):
        table_noeud=self.dlg.ui.comboBox.currentText()
        global table_arc
        table_arc=self.dlg.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        fields2=[""]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
          fields2=fields2+[str(field[i].name())]
        self.dlg2 = testDialog2b(self.iface.mainWindow())
        self.dlg2.ui.comboBox.addItems(fields)
        self.dlg2.ui.comboBox_2.addItems(fields)
        self.dlg2.ui.comboBox_3.addItems(["No","Yes"])
        self.dlg2.ui.comboBox_4.addItems(["No","Yes"])
        self.dlg2.ui.comboBox_5.addItems(fields2)
        self.dlg2.ui.comboBox_6.addItems(["Fareness_increase","Closeness_vitality","Dynamic_analysis","Error_attack"])
        QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2b)
        self.dlg2.show()

  def calcul2b(self):
        arc_start=self.dlg2.ui.comboBox.currentText()
        arc_end=self.dlg2.ui.comboBox_2.currentText()
        oriente=self.dlg2.ui.comboBox_3.currentText()
        poids=self.dlg2.ui.comboBox_4.currentText()
        ponderation=self.dlg2.ui.comboBox_5.currentText()
        global indicateur
        indicateur=self.dlg2.ui.comboBox_6.currentText()
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        global table
        table=[]
        if str(poids)=="No":
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          attrsdist=1
          table=table+[(attrsstart,attrsend,attrsdist)] 
         global G
         G=nx.Graph()
         if str(oriente)=="Yes" :
          G=nx.DiGraph()
         G.add_weighted_edges_from(table)
        if str(poids)=="Yes":
         distind=provider.fieldNameIndex(str(ponderation))
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind,distind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          attrsdist=feat.attributes()[distind]
          table=table+[(attrsstart,attrsend,attrsdist)] 
         G=nx.Graph()
         if str(oriente)=="Yes" :
          G=nx.DiGraph()
         G.add_weighted_edges_from(table)
        if str(indicateur)=="Fareness_increase":
            spl=nx.shortest_path_length(G, weight='weight')
            self.dlg5 = testDialog5(self.iface.mainWindow())
            self.dlg5.ui.progressBar.setProperty("value", 0)
            self.dlg5.show()
            b2pro=[0]*len(G.nodes())
            b=[0]*(len(G.nodes())+1)
            tot=0
            try :
                 for i in range(len(G.nodes())):
                     for j in range(len(G.nodes())):
                         b2pro[i]=b2pro[i]+(spl[i+1][j+1])
                         b2pro[j]=b2pro[j]+(spl[i+1][j+1])
                         tot=tot+spl[i+1][j+1]
                 err=0
            except :
                 QMessageBox.information(None, " Message : ", "Graph not connected: infinite path length.")
                 err=1
                 b=77777
            if err==0:
                 for l in range(len(G.nodes())):
                     G2=0
                     G2=nx.Graph()
                     if str(oriente)=="Yes" :
                         G2=nx.DiGraph()
                     G2.add_weighted_edges_from(table)
                     edg=nx.edges(G,l+1)
                     for l2 in range(len(edg)):
                         dep=edg[l2][0]
                         arr=edg[l2][1]
                         G2.edge[dep][arr]['weight']=10000000000000
                     spl2=nx.shortest_path_length(G2, weight='weight')
                     totper=0
                     for l2 in range(len(G.nodes())):
                         for l3 in range(len(G.nodes())):
                             if l2!=l:
                                 if l3!=l:
                                     totper=totper+spl2[l2+1][l3+1]
                     res=totper-(tot-b2pro[l])
                     if res<10000000000000 :
                         b[l+1]=res
                     if res>=10000000000000 :
                         QMessageBox.information(None, " Message : ", "Be careful, removed the node "+str(l+1)+" induces infinite distances : fareness increase = 9999999999999999")
                         b[l+1]=9999999999999999
                     valbar=int(((l+1)/float(len(G.nodes())))*100)
                     self.dlg5.ui.progressBar.setProperty("value", valbar)
            self.dlg5.close() 
        if str(indicateur)=="Closeness_vitality" and str(poids)=="No" :
            b=nx.closeness_vitality(G)
        if str(indicateur)=="Closeness_vitality" and str(poids)=="Yes":
            b=nx.closeness_vitality(G, weight='weight')
        if str(indicateur)=="Dynamic_analysis" and str(poids)=="No" and str(oriente)=="No":
            nbalpha2, ok = QInputDialog.getText(None, "QInputDialog.getText()",  "Decimal number (between 2 and 5) :", QLineEdit.Normal, "2")
            nbalpha=int(nbalpha2)
            cen=nx.betweenness_centrality(G)
            b=[0]+[0]*len(G.nodes())
            self.dlg5 = testDialog5(self.iface.mainWindow())
            self.dlg5.ui.progressBar.setProperty("value", 0)
            self.dlg5.show()
            for l in range(len(G.nodes())) :
                  if nbalpha==2:
                       alpha=0.01
                  if nbalpha==3:
                       alpha=0.001
                  if nbalpha==4:
                       alpha=0.0001
                  if nbalpha==5:
                      alpha=0.00001
                  destruction=len(G.nodes())
                  while destruction >= int(len(G.nodes())/2) :
                      G2=0
                      G2=nx.Graph()
                      G2.add_weighted_edges_from(table)
                      G2.remove_node(l+1)
                      temp=[0]*len(G.nodes())
                      cen2=nx.betweenness_centrality(G2)
                      pile=[]
                      pilesave=[]
                      destruction=0
                      for k in cen2.keys() :  
                               temp[k-1]=cen2[k]-cen[k]
                               if temp[k-1]>alpha :
                                     pile=pile+[k]
                                     pilesave=pilesave+[k]
                                     destruction=destruction+1
                      while (len(pile) != 0) and (destruction<int(len(G.nodes())/2)) :
                                     G2.remove_node(pile[len(pile)-1])
                                     pile.remove(pile[len(pile)-1])
                                     cen2=nx.betweenness_centrality(G2)
                                     for k2 in cen2.keys() :
                                                 temp[k2-1]=cen2[k2]-cen[k2]
                                                 if temp[k2-1]>alpha :
                                                     test=0
                                                     for t in pilesave :
                                                           if k2== t :
                                                                    test=1
                                                     if test==0 :
                                                         pile=pile+[k2]
                                                         pilesave=pilesave+[k2]
                                                         destruction=destruction+1
                      b[l+1]=alpha
                      valbar=int(((l+1)/float(len(G.nodes())))*100)
                      self.dlg5.ui.progressBar.setProperty("value", valbar)
                      if nbalpha==2:
                           alpha=0.01+alpha
                      if nbalpha==3:
                           alpha=0.001+alpha
                      if nbalpha==4:
                           alpha=0.0001+alpha
                      if nbalpha==5:
                           alpha=0.00001+alpha
            self.dlg5.close()
        if str(indicateur)=="Dynamic_analysis" and str(poids)=="Yes" and str(oriente)=="No":
            nbalpha2, ok = QInputDialog.getText(None, "QInputDialog.getText()",  "Decimal number (between 2 and 5) :", QLineEdit.Normal, "2")
            nbalpha=int(nbalpha2)
            cen=nx.betweenness_centrality(G,weight='weight')
            b=[0]+[0]*len(G.nodes())
            self.dlg5 = testDialog5(self.iface.mainWindow())
            self.dlg5.ui.progressBar.setProperty("value", 0)
            self.dlg5.show()
            for l in range(len(G.nodes())) :
                  if nbalpha==2:
                       alpha=0.01
                  if nbalpha==3:
                       alpha=0.001
                  if nbalpha==4:
                       alpha=0.0001
                  if nbalpha==5:
                      alpha=0.00001
                  destruction=len(G.nodes())
                  while destruction >= int(len(G.nodes())/2) :
                      G2=0
                      G2=nx.Graph()
                      G2.add_weighted_edges_from(table)
                      G2.remove_node(l+1)
                      temp=[0]*len(G.nodes())
                      cen2=nx.betweenness_centrality(G2,weight='weight')
                      pile=[]
                      pilesave=[]
                      destruction=0
                      for k in cen2.keys() :  
                               temp[k-1]=cen2[k]-cen[k]
                               if temp[k-1]>alpha :
                                     pile=pile+[k]
                                     pilesave=pilesave+[k]
                                     destruction=destruction+1
                      while (len(pile) != 0) and (destruction<int(len(G.nodes())/2)) :
                                     G2.remove_node(pile[len(pile)-1])
                                     pile.remove(pile[len(pile)-1])
                                     cen2=nx.betweenness_centrality(G2,weight='weight')
                                     for k2 in cen2.keys() :
                                                 temp[k2-1]=cen2[k2]-cen[k2]
                                                 if temp[k2-1]>alpha :
                                                     test=0
                                                     for t in pilesave :
                                                           if k2== t :
                                                                    test=1
                                                     if test==0 :
                                                         pile=pile+[k2]
                                                         pilesave=pilesave+[k2]
                                                         destruction=destruction+1
                      b[l+1]=alpha
                      valbar=int(((l+1)/float(len(G.nodes())))*100)
                      self.dlg5.ui.progressBar.setProperty("value", valbar)
                      if nbalpha==2:
                           alpha=0.01+alpha
                      if nbalpha==3:
                           alpha=0.001+alpha
                      if nbalpha==4:
                           alpha=0.0001+alpha
                      if nbalpha==5:
                           alpha=0.00001+alpha
            self.dlg5.close()
        if str(indicateur)=="Dynamic_analysis" and str(oriente)=="Yes":
             QMessageBox.information(None, " Message : ", "Currently Graph needs to be undirected.")
             b=77777
        if str(indicateur)=="Error_attack":
             if str(oriente)=="No":
                 self.dlg3 = testDialog3(self.iface.mainWindow())
                 self.dlg3.ui.lineEdit.setText("10")
                 self.dlg3.ui.lineEdit_2.setText("0.15")
                 self.dlg3.ui.lineEdit_6.setText("")
                 self.dlg3.ui.lineEdit_3.setText("test")
                 self.dlg3.ui.lineEdit_4.setText("10")
                 self.dlg3.ui.lineEdit_5.setText("7")
                 self.dlg3.ui.lineEdit_7.setText("7")
                 self.dlg3.ui.lineEdit_8.setText("2")
                 self.dlg3.ui.comboBox.addItems(["tiff","svg","jpg"])
                 self.dlg3.ui.directoryButton.clicked.connect(self.openDir)
                 QObject.connect(self.dlg3.ui.buttonBox, SIGNAL("accepted()"), self.calcul3)
                 self.dlg3.show()
             if str(oriente)=="Yes":
                 QMessageBox.information(None, " Message : ", "Currently Graph needs to be undirected.")
                 b=77777
        if str(indicateur)!="Error_attack":
          if b!=77777:
            aLayer2 = allLayers[int(ind_noeud)]
            provider2 = aLayer2.dataProvider()
            nbcol=int(provider2.fields().count())
            provider2.addAttributes([QgsField(str(indicateur), QVariant.Double)])
            aLayer2.startEditing()
            taille=len(G.nodes())
            for k in range(taille):
                  aLayer2.changeAttributeValue(k,nbcol,float(b[k+1]))
            aLayer2.commitChanges()
          QMessageBox.information(None, " Message : ", "End")

  def openDir(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(None, "QFileDialog.getExistingDirectory()", self.dlg3.ui.lineEdit_6.text(), options)
        if directory:
            self.dlg3.ui.lineEdit_6.setText(directory)

  def calcul3(self):
        if str(indicateur)=="Error_attack" and testmatplotview == 0 :
                 QMessageBox.information(None, " Message : ", "Your QGIS version is not compatible")
        if str(indicateur)=="Error_attack" and testmatplotview == 1 :
                 self.dlg5 = testDialog5(self.iface.mainWindow())
                 self.dlg5.ui.progressBar.setProperty("value", 1)
                 self.dlg5.show()
                 format=self.dlg3.ui.comboBox.currentText()
                 nbal=self.dlg3.ui.lineEdit.text()
                 taux=self.dlg3.ui.lineEdit_2.text()
                 tx=float(taux)
                 nomfichier=self.dlg3.ui.lineEdit_3.text()
                 largeur=self.dlg3.ui.lineEdit_4.text()
                 hauteur=self.dlg3.ui.lineEdit_5.text()
                 rep=self.dlg3.ui.lineEdit_6.text()
                 pttaille=self.dlg3.ui.lineEdit_7.text()
                 lignelar=self.dlg3.ui.lineEdit_8.text()
                 nbal2=int(nbal)
                 G2=0
                 G3=0
                 G4=0
                 G4b=0
                 G2=nx.Graph()
                 G3=nx.Graph()
                 G4=nx.Graph()
                 G4b=nx.Graph()
                 G2.add_weighted_edges_from(table)
                 G3.add_weighted_edges_from(table)
                 G4.add_weighted_edges_from(table)
                 G4b.add_weighted_edges_from(table)
                 b=[1.00000]*(len(G.nodes())+1)
                 b3=[1.00000]*(len(G.nodes())+1)
                 b4=[1.00000]*(len(G.nodes())+1)
                 cen=nx.betweenness_centrality(G,weight=True)
                 cens=sorted(cen.items(), reverse=True, key=operator.itemgetter(1))
                 cen3=nx.degree(G)
                 cens3=sorted(cen3.items(), reverse=True, key=operator.itemgetter(1))
                 cen4=nx.betweenness_centrality(G,weight=True)
                 cens4=sorted(cen4.items(), reverse=True, key=operator.itemgetter(1))
                 for l in range(int((len(G.nodes()))*tx)) :
                          nbconnex=0
                          it=cens[l][0]
                          edg=nx.edges(G,it)
                          for l2 in range(len(edg)): 
                                    dep=edg[l2][0]
                                    arr=edg[l2][1]
                                    G2.edge[dep][arr]['weight']=10000000000
                          spl2=nx.shortest_path_length(G2, weight='weight')
                          nbconnex3=0
                          it3=cens3[l][0]
                          edg3=nx.edges(G,it3)
                          for l2 in range(len(edg3)): 
                                    dep=edg3[l2][0]
                                    arr=edg3[l2][1]
                                    G3.edge[dep][arr]['weight']=10000000000
                          spl3=nx.shortest_path_length(G3, weight='weight')
                          nbconnex4=0
                          it4=cens4[0][0]  
                          edg4=nx.edges(G,it4)
                          for l2 in range(len(edg4)): 
                                    dep=edg4[l2][0]
                                    arr=edg4[l2][1]
                                    G4.edge[dep][arr]['weight']=10000000000
                          spl4=nx.shortest_path_length(G4, weight='weight')
                          for l2 in range(len(G.nodes())):
                                   ligne=spl2[l2+1].values()
                                   ligne3=spl3[l2+1].values()
                                   ligne4=spl4[l2+1].values()
                                   for l3 in range(len(G.nodes())):
                                            val=ligne[l3]
                                            val3=ligne3[l3]
                                            val4=ligne4[l3]
                                            if val >=10000000000 :
                                                  nbconnex=nbconnex+1
                                            if val3 >=10000000000 :
                                                  nbconnex3=nbconnex3+1
                                            if val4 >=10000000000 :
                                                  nbconnex4=nbconnex4+1
                          b[int(it)]=nbconnex/float((len(G.nodes())*(len(G.nodes())-1)))
                          b3[int(it3)]=nbconnex3/float((len(G.nodes())*(len(G.nodes())-1)))
                          b4[int(it4)]=nbconnex4/float((len(G.nodes())*(len(G.nodes())-1)))
                          G4b.remove_node(it4)
                          cen4=nx.betweenness_centrality(G4b,weight=True)
                          cens4=sorted(cen4.items(), reverse=True, key=operator.itemgetter(1))
                          valbar=int(((3*(l+1))*100)/float((len(G.nodes())*(3+nbal2))))
                          self.dlg5.ui.progressBar.setProperty("value", valbar)
                 b5tot=[1.00000]*(len(G.nodes())+1)
                 for m in range(nbal2) :
                      G5=0
                      G5=nx.Graph()
                      b5=[0.00000]*(len(G.nodes())+1)
                      G5.add_weighted_edges_from(table)
                      cens5= G.nodes()
                      random.shuffle(cens5)
                      for l in range(int((len(G.nodes()))*tx)) :
                          nbconnex5=0
                          it5=cens5[l]
                          edg5=nx.edges(G,it5)
                          for l2 in range(len(edg5)):
                                    dep=edg5[l2][0]
                                    arr=edg5[l2][1]
                                    G5.edge[dep][arr]['weight']=10000000000
                          spl5=nx.shortest_path_length(G5, weight='weight')
                          for l2 in range(len(G.nodes())):
                                   ligne5=spl5[l2+1].values()
                                   for l3 in range(len(G.nodes())):
                                            val5=ligne5[l3]
                                            if val5 >=10000000000 :
                                                  nbconnex5=nbconnex5+1
                          b5[l]=nbconnex5
                          valbar=int((((3*len(G.nodes()))+(l+1)+(m*len(G.nodes())))*100)/float((len(G.nodes())*(3+nbal2))))
                          self.dlg5.ui.progressBar.setProperty("value", valbar)
                      b5tot=np.array(b5tot)+np.array(b5)
                 b5tot= b5tot/float((len(G.nodes())*(len(G.nodes())-1)*nbal2))
                 taille=len(G.nodes())
                 self.dlg5.close()
                 lar=int(largeur)
                 ht=int(hauteur)
                 pttaille2=int(pttaille)
                 lignelar2=int(lignelar)
                 fig = plt.figure(figsize=(lar, ht))
                 p1, = plt.plot(100*np.array(G.nodes()[0:int((len(G.nodes())+1)*tx)])/float(int(len(G.nodes()))), sorted(b[1:len(G.nodes())+1])[0:int((len(G.nodes())+1)*tx)], 'r', linewidth=lignelar2, marker='o', markersize=pttaille2)
                 p2, = plt.plot(100*np.array(G.nodes()[0:int((len(G.nodes())+1)*tx)])/float(int(len(G.nodes()))), sorted(b3[1:len(G.nodes())+1])[0:int((len(G.nodes())+1)*tx)], color='#00bfbf', linewidth=lignelar2, marker='o', markersize=pttaille2)
                 p3, = plt.plot(100*np.array(G.nodes()[0:int((len(G.nodes())+1)*tx)])/float(int(len(G.nodes()))), sorted(b4[1:len(G.nodes())+1])[0:int((len(G.nodes())+1)*tx)], color='#dbc71c', linewidth=lignelar2, marker='o', markersize=pttaille2)
                 p4, = plt.plot(100*np.array(G.nodes()[0:int((len(G.nodes())+1)*tx)])/float(int(len(G.nodes()))), b5tot[0:len(G.nodes())][0:int((len(G.nodes())+1)*tx)], color = '#51d51d', linewidth=lignelar2, marker='o', markersize=pttaille2)
                 plt.ylabel('Connectivity loss')
                 plt.xlabel('Fraction of nodes removed')
                 plt.legend([p4, p3, p2, p1], ["Random","Cascading", "Degree", "Betweenness"], loc=4)
                 nameFile = str(nomfichier)+"."+str(format)
                 adresse = os.path.join(str(rep), nameFile)
                 plt.savefig(adresse)
                 plt.close()
                 self.dlg4 = testDialog4(self.iface.mainWindow())
                 texthtml='<img src="'+adresse+'">'
                 self.dlg4.ui.textBrowser.setHtml(texthtml)
                 self.dlg4.show()
  #----------------------------------------------------------------------------------------------------------------------------------------                 Community Detection             -----------------------------------------------------------------------------------------------------------------------------------
  def runc(self): 
        global canvas
        canvas = self.iface.mapCanvas()
        global allLayers
        allLayers = canvas.layers()
        global count
        count = canvas.layerCount()
        global lay
        lay=[]
        for i in allLayers:
           lay=lay+[str(i.name())]
        global table_noeud
        self.dlg = testDialog(self.iface.mainWindow())
        self.dlg.ui.comboBox.addItems(lay)
        self.dlg.ui.comboBox_2.addItems(lay)
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("accepted()"), self.calculc)
        self.dlg.show()

  def calculc(self):
        table_noeud=self.dlg.ui.comboBox.currentText()
        global table_arc
        table_arc=self.dlg.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        fields2=[""]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
          fields2=fields2+[str(field[i].name())]
        self.dlg2 = testDialog2b(self.iface.mainWindow())
        self.dlg2.ui.comboBox.addItems(fields)
        self.dlg2.ui.comboBox_2.addItems(fields)
        self.dlg2.ui.comboBox_3.addItems(["No","Yes"])
        self.dlg2.ui.comboBox_4.addItems(["No","Yes"])
        self.dlg2.ui.comboBox_5.addItems(fields2)
        self.dlg2.ui.comboBox_6.addItems(["Louvain method","Edge Betweenness Cluster","Structural Equivalence", "Blockmodeling", "Connected Components", "Spatial Cluster"])
        QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2c)
        self.dlg2.show()

  def calcul2c(self):
        arc_start=self.dlg2.ui.comboBox.currentText()
        arc_end=self.dlg2.ui.comboBox_2.currentText()
        oriente=self.dlg2.ui.comboBox_3.currentText()
        poids=self.dlg2.ui.comboBox_4.currentText()
        ponderation=self.dlg2.ui.comboBox_5.currentText()
        global indicateur
        indicateur=self.dlg2.ui.comboBox_6.currentText()
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        table=[]
        nbelement=0
        if str(poids)=="No":
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          nbelement= nbelement+1
          table=table+[(attrsstart,attrsend)] 
         G=nx.Graph()
         if str(oriente)=="Yes" :
             G=nx.DiGraph()
         G.add_edges_from(table)
        if str(poids)=="Yes":
         distind=provider.fieldNameIndex(str(ponderation))
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind,distind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          attrsdist=feat.attributes()[distind]
          nbelement= nbelement+1
          table=table+[(attrsstart,attrsend,attrsdist)] 
         G=nx.Graph()
         if str(oriente)=="Yes" :
             G=nx.DiGraph()
         G.add_weighted_edges_from(table)
        if str(indicateur) == "Louvain method" :
          if str(oriente)=="No":
             part = com.best_partition(G)
             aLayer2 = allLayers[int(ind_noeud)]
             provider2 = aLayer2.dataProvider()
             nbcol=int(provider2.fields().count())
             provider2.addAttributes([QgsField(str(indicateur), QVariant.Int)])
             aLayer2.startEditing()
             taille=len(G.nodes())
             for k in range(taille):
                 aLayer2.changeAttributeValue(k,nbcol,int(part[k+1]))
             aLayer2.commitChanges()
             mod= com.modularity(part,G)
             QMessageBox.information(None, " Message : ", "Modularity : "+str(mod))
          if str(oriente)=="Yes" :
             QMessageBox.information(None, " Message : ", "Graph needs to be undirected")
        if (indicateur) == "Edge Betweenness Cluster" :
             ncmax,ok = QInputDialog.getInt(None,"Cluster","Enter the number of clusters : ", 5)
             if ok:
                 taillen = len(G.nodes())
                 graphs = list(nx.connected_component_subgraphs(G))
                 nc = len(graphs)
                 while nc < ncmax :
                     b = dict()
                     for i in range(nc) :
                         b.update(nx.edge_betweenness_centrality(graphs[i],normalized=False))
                     trib = sorted(b.items(), key=lambda t: t[1], reverse = True)
                     try :
                         G.remove_edge(trib[0][0][0], trib[0][0][1])
                     except : 
                         G.remove_edge(trib[0][0][1], trib[0][0][0])
                     graphs = list(nx.connected_component_subgraphs(G))
                     nc = len(graphs)
                 aLayer2 = allLayers[int(ind_noeud)]
                 provider2 = aLayer2.dataProvider()
                 nbcol = int(provider2.fields().count())
                 provider2.addAttributes( [QgsField("Cluster_EB", QVariant.Int)] )
                 aLayer2.startEditing()
                 part = dict()
                 for i in range(ncmax) :
                     for j in range(len(graphs[i].nodes())):
                         aLayer2.changeAttributeValue(int(graphs[i].nodes()[j])-1,nbcol,(int(i)))
                         part[int(graphs[i].nodes()[j])] = int(i)
                 aLayer2.commitChanges()
                 mod= com.modularity(part,G)
                 QMessageBox.information(None, " Message : ", "Modularity : "+str(mod))
        if str(indicateur) == "Structural Equivalence" and testscipy == 1 :
            if str(poids) == "Yes" :
                QMessageBox.information(None, " Message : ", "This algorithm does not use weigths")
            nclus,ok = QInputDialog.getInt(None,"Cluster","Number of clusters : ", 5)
            if ok :
                listnode = []
                for i in range(len(G.nodes())):
                    listnode = listnode + [i+1]
                adjar = nx.to_numpy_matrix(G, nodelist=listnode, weight=None)
                adjarr = np.array(adjar)
                QMessageBox.information(None, " Message : ", str(adjarr))
                distmat = np.zeros((len(listnode),len(listnode)))
                for i in range(len(listnode)) : 
                    for j in range(len(listnode)) :
                        dist = np.sqrt( ((sum(adjarr[i] - adjarr[j])) * (sum(adjarr[i] - adjarr[j]))) + ((sum(adjarr[:,i] - adjarr[:,j])) * (sum(adjarr[:,i] - adjarr[:,j]))) )
                        distmat[i,j] = dist
                Y = squareform(distmat)
                Z = linkage(Y, method='average')
                part = fcluster(Z, nclus, criterion='maxclust')
                aLayer2 = allLayers[int(ind_noeud)]
                provider2 = aLayer2.dataProvider()
                nbcol = int(provider2.fields().count())
                provider2.addAttributes( [QgsField("Structural_Eq", QVariant.Int)] )
                aLayer2.startEditing()
                for i in range(len(listnode)) :
                    aLayer2.changeAttributeValue(int(i), nbcol, int(part[i])-1)
                aLayer2.commitChanges()
        if str(indicateur) == "Structural Equivalence" and testscipy == 0 :
            QMessageBox.information(None, " Message : ", "Unfortunately your QGIS version does not implement scipy")
        if str(indicateur) == "Blockmodeling" :
            epsg = canvas.mapRenderer().destinationCrs().authid()
            aLayer2 = allLayers[int(ind_noeud)]
            provider2 = aLayer2.dataProvider()
            field2 = provider2.fields()
            fields2 = []
            for i in range(field2.count()) :
                fields2 = fields2 + [str(field2[i].name())]
            fieldpart,ok = QInputDialog.getItem(None,"Partition Field","Choose your partition field : ", fields2, editable = False)
            if ok :
                modept = ["Centroid", "P Median", "Random"]
                for i in range(len(fields2)):
                    modept = modept + ["Max " + str(fields2[i])]
                mode,ok2 = QInputDialog.getItem(None, "Nodes Design", "Choose your mode for nodes design : ", modept, editable = False)
                if ok2 :
                        part = []
                        geompartx = []
                        geomparty = []
                        geompartxy = []
                        numpart = []
                        partind = provider2.fieldNameIndex(str(fieldpart))
                        modenum = modept.index(mode)
                        if modenum > 2 :
                            nom = mode[4:]
                            modeind = provider2.fieldNameIndex(str(nom))
                            champ = []
                        feat = QgsFeature()
                        fit2 = provider2.getFeatures()
                        i = 1
                        while fit2.nextFeature(feat):
                            val = feat.attributes()[partind]
                            geom = feat.geometry().exportToWkt()
                            try :
                                ind = numpart.index(val)
                                part[ind] = part[ind] +  [i]
                                geom2 = string.split(geom,'(')
                                geom3 = string.split(geom2[1],')')
                                xy = string.split(geom3[0],' ')
                                geompartx[ind] = geompartx[ind] + [float(xy[0])]
                                geomparty[ind] = geomparty[ind] + [float(xy[1])]
                                geompartxy[ind] = geompartxy[ind] + [[float(xy[0]), float(xy[1])]]
                                if modenum > 2 :
                                    val2 = feat.attributes()[modeind]
                                    champ[ind] = champ[ind] + [val2]
                            except :
                                numpart = numpart + [val]
                                part = part +  [[i]]
                                geom2 = string.split(geom,'(')
                                geom3 = string.split(geom2[1],')')
                                xy = string.split(geom3[0],' ')
                                geompartx = geompartx + [[float(xy[0])]]
                                geomparty = geomparty + [[float(xy[1])]]
                                geompartxy = geompartxy + [[[float(xy[0]), float(xy[1])]]]
                                if modenum > 2 :
                                    val2 = feat.attributes()[modeind]
                                    champ = champ + [[val2]]
                            i = i + 1
                        bk = nx.blockmodel(G,part)
                        edg = bk.edges()
                        v2 = QgsVectorLayer("Point?crs=epsg:" + str(epsg), "Nodes", "memory")
                        p2 = v2.dataProvider()
                        p2.addAttributes( [QgsField("ID", QVariant.Int)] )
                        v2.commitChanges()
                        v2.startEditing()
                        xpart = []
                        ypart = []
                        for i in range(len(numpart)):
                            if str(mode) == "Centroid" :
                                valx = np.mean(geompartx[i])
                                valy = np.mean(geomparty[i])
                            if str(mode) == "Random":
                                ind = int(random.randint(0,len(part[i]) - 1 ))
                                valx = geompartx[i][ind]
                                valy = geomparty[i][ind]
                            if str(mode) == "P Median" :
                                axy = np.array(geompartxy[i])
                                distmatrix = pdist(axy)
                                dist = squareform(distmatrix)
                                mindist = sum(dist[0])
                                ind = 0
                                for j in range(len(geompartxy[i])-1):
                                    if mindist > sum(dist[j+1]):
                                        mindist = sum(dist[j+1])
                                        ind = j + 1
                                valx = geompartx[i][ind]
                                valy = geomparty[i][ind]
                            if modenum > 2 :
                                maxc = max(champ[i])
                                ind = champ[i].index(maxc)
                                valx = geompartx[i][ind]
                                valy = geomparty[i][ind]
                            xpart = xpart + [valx]
                            ypart = ypart + [valy]
                            fet = QgsFeature()
                            textgeom = "POINT(" + str(valx) + " " + str(valy) + ")"
                            fet.setGeometry(  QgsGeometry.fromWkt( textgeom ) )
                            fet.setAttributes( [ numpart[i] ] )
                            p2.addFeatures( [ fet ] )
                        v2.commitChanges()
                        v = QgsVectorLayer("LineString?crs=epsg:" + str(epsg), "Edges", "memory")
                        p = v.dataProvider()
                        p.addAttributes( [QgsField("StartNode", QVariant.Int), QgsField("EndNode", QVariant.Int)] )
                        v.commitChanges()
                        v.startEditing()
                        for i in range(len(edg)):
                            dep = edg[i][0]
                            arr = edg[i][1]
                            textgeom = "LINESTRING(" + str(xpart[dep]) + " " + str(ypart[dep]) + "," + str(xpart[arr]) + " " + str(ypart[arr]) + ")"
                            fet.setGeometry(  QgsGeometry.fromWkt( textgeom ) )
                            fet.setAttributes( [ numpart[dep], numpart[arr] ] )
                            p.addFeatures( [ fet ] )
                        v.commitChanges()
                       	QgsMapLayerRegistry.instance().addMapLayer(v2)
                        QgsMapLayerRegistry.instance().addMapLayer(v)
        if str(indicateur) == "Connected Components" :
            if str(oriente)=="No":
                res = nx.connected_components(G)
                aLayer2 = allLayers[int(ind_noeud)]
                provider2 = aLayer2.dataProvider()
                nbcol = int(provider2.fields().count())
                provider2.addAttributes([QgsField(str(indicateur), QVariant.Int)])
                aLayer2.startEditing()
                taille = len(G.nodes())
                for k in range(taille):
                    for j in range(len(res)):
                        try :
                            test = res[j].index(int(k+1))
                            val = j + 1
                        except :
                            "Do Nothing"
                    aLayer2.changeAttributeValue(k,nbcol,int(val))
                aLayer2.commitChanges()					
            if str(oriente)=="Yes":
                QMessageBox.information(None, " Message : ", "Graph needs to be undirected")
        if str(indicateur) == "Spatial Cluster" and str(poids) == "Yes" :
            fieldpart,ok = QInputDialog.getItem(None,"Gravity Field","Choose your gravity field : ", fields, editable = False)
            if ok :
                partind = provider.fieldNameIndex(str(fieldpart))
                fit1 = provider.getFeatures()
                table2 = []
                while fit1.nextFeature(feat):
                    attrsstart = feat.attributes()[startind]
                    attrsend = feat.attributes()[endind]
                    attrsdist = feat.attributes()[partind]
                    table2 = table2 + [(attrsstart,attrsend,attrsdist)] 
                G2=nx.Graph()
                if str(oriente) == "Yes":
                    G2 = nx.DiGraph()
                G2.add_weighted_edges_from(table2)
                iso,ok2 = QInputDialog.getItem(None,"Isolated Node","Do you want to gather isolated nodes to main clusters ? : ", ["No","Yes"], editable = False)
                if ok2 :
                    res, val = gravi.com_spa(G,G2,oriente,iso)
                    aLayer2 = allLayers[int(ind_noeud)]
                    provider2 = aLayer2.dataProvider()
                    nbcol=int(provider2.fields().count())
                    provider2.addAttributes([QgsField(str(indicateur), QVariant.Int)])
                    aLayer2.startEditing()
                    taille=len(G.nodes())
                    for i in range(len(res)) :
                        for j in range(len(res[i])) :
                            aLayer2.changeAttributeValue(res[i][j]-1, nbcol, i)
                    aLayer2.commitChanges()
                    QMessageBox.information(None, " Message : ", "Modularity : "+str(val))
        QMessageBox.information(None, " Message : ", "End")
  #----------------------------------------------------------------------------------------------------------------------------------------                 Optimization             -----------------------------------------------------------------------------------------------------------------------------------
  def rund(self): 
        global canvas
        canvas = self.iface.mapCanvas()
        global allLayers
        allLayers = canvas.layers()
        global count
        count = canvas.layerCount()
        global lay
        lay=[]
        for i in allLayers:
           lay=lay+[str(i.name())]
        global table_noeud
        self.dlg = testDialog(self.iface.mainWindow())
        self.dlg.ui.comboBox.addItems(lay)
        self.dlg.ui.comboBox_2.addItems(lay)
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("accepted()"), self.calculd)
        self.dlg.show()

  def calculd(self):
        table_noeud=self.dlg.ui.comboBox.currentText()
        global table_arc
        table_arc=self.dlg.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        global aLayer2
        aLayer2 = allLayers[int(ind_noeud)]
        global provider2
        provider2 = aLayer2.dataProvider()
        fields=[]
        fields2=[""]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
          fields2=fields2+[str(field[i].name())]
        self.dlg2 = testDialog2b(self.iface.mainWindow())
        self.dlg2.ui.comboBox.addItems(fields)
        self.dlg2.ui.comboBox_2.addItems(fields)
        self.dlg2.ui.comboBox_3.addItems(["No","Yes"])
        self.dlg2.ui.comboBox_4.addItems(["No","Yes"])
        self.dlg2.ui.comboBox_5.addItems(fields2)
        self.dlg2.ui.comboBox_6.addItems(["Delaunay", "Minimum Spanning Tree", "Find Cliques", "All Shortest Paths (Distancier)", "Transportation Problem", "PMedian"])
        QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2d)
        self.dlg2.show()

  def calcul2d(self):
        arc_start=self.dlg2.ui.comboBox.currentText()
        arc_end=self.dlg2.ui.comboBox_2.currentText()
        oriente=self.dlg2.ui.comboBox_3.currentText()
        poids=self.dlg2.ui.comboBox_4.currentText()
        ponderation=self.dlg2.ui.comboBox_5.currentText()
        indicateur=self.dlg2.ui.comboBox_6.currentText()
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        table = []
        table2 = []
        table3 = []
        geo = []
        if str(poids)=="No":
         fit1 = provider.getFeatures()
         while fit1.nextFeature(feat):
          attrsstart = feat.attributes()[startind]
          attrsend = feat.attributes()[endind]
          geo = geo + [feat.geometry().asPolyline()]
          attrsdist = 1
          table = table + [(attrsstart,attrsend,attrsdist)]
          table2 = table2 + [(attrsstart,attrsend)]
          attrs = feat.attributes()
          table3 = table3 + [attrs]
         global G
         G=nx.Graph()
         if str(oriente)=="Yes" :
          G=nx.DiGraph()
         G.add_weighted_edges_from(table)
        if str(poids)=="Yes":
         distind=provider.fieldNameIndex(str(ponderation))
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind,distind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          attrsdist=float(feat.attributes()[distind])
          table=table+[(attrsstart,attrsend,attrsdist)] 
          table2 = table2 + [(attrsstart,attrsend)]
          attrs = feat.attributes()
          table3 = table3 + [attrs]
          geo = geo + [feat.geometry().asPolyline()]
         G=nx.Graph()
         if str(oriente)=="Yes" :
          G=nx.DiGraph()
         G.add_weighted_edges_from(table)
        t=nx.number_of_nodes(G)
        if indicateur=="Delaunay":
            inp = str(provider2.dataSourceUri())
            (myDirectory,nameFile) = os.path.split(inp)
            nameFile2 = "Delaunay.shp"
            out = os.path.join(myDirectory,nameFile2)
            a = processing.runalg('qgis:delaunaytriangulation', inp, out)
            delaunay = self.iface.addVectorLayer(out, "Delaunay", "ogr")
            provider3 = delaunay.dataProvider()
            feat = QgsFeature()
            tabledelaunay = []
            fit1 = provider3.getFeatures()
            while fit1.nextFeature(feat):
                som1=feat.attributes()[0]
                som2=feat.attributes()[1]
                som3=feat.attributes()[2]
                geome=feat.geometry()
                geom=geome.asPolygon()
                x1=geom[0][0][0]
                y1=geom[0][0][1]
                x2=geom[0][1][0]
                y2=geom[0][1][1]
                x3=geom[0][2][0]
                y3=geom[0][2][1]
                tabledelaunay=tabledelaunay+[(som1+1,som2+1,x1,y1,x2,y2)] 
                tabledelaunay=tabledelaunay+[(som1+1,som3+1,x1,y1,x3,y3)] 
                tabledelaunay=tabledelaunay+[(som2+1,som3+1,x2,y2,x3,y3)] 
            epsg=canvas.mapRenderer().destinationCrs().authid()
            vl = QgsVectorLayer("LineString?crs="+str(epsg), "Delaunay", "memory")
            pr = vl.dataProvider()
            tabdelfin=[tabledelaunay[0]]
            point1=QgsPoint(tabledelaunay[0][2],tabledelaunay[0][3])
            point2=QgsPoint(tabledelaunay[0][4],tabledelaunay[0][5])
            fet = QgsFeature()
            fet.setGeometry( QgsGeometry.fromPolyline([point1,point2]) )
            pr.addFeatures( [ fet ] )
            vl.commitChanges()
            QgsMapLayerRegistry.instance().addMapLayer(vl)
            for i in range(len(tabledelaunay)):
                ligne=tabledelaunay[i]
                test=0
                for j in range(len(tabdelfin)): 
                    ligne2=tabdelfin[j]
                    if (ligne2[0]==ligne[0]) and (ligne2[1]==ligne[1]) :
                        test=1
                    if (ligne2[0]==ligne[1]) and (ligne2[1]==ligne[0]) :
                        test=1
                if test==0:
                    tabdelfin=tabdelfin+[ligne]
                    point1=QgsPoint(ligne[2],ligne[3])
                    point2=QgsPoint(ligne[4],ligne[5])
                    fet = QgsFeature()
                    fet.setGeometry( QgsGeometry.fromPolyline([point1,point2]) )
                    pr.addFeatures( [ fet ] )
                    vl.commitChanges()
            vl.startEditing()
            pr.addAttributes( [ QgsField("ID", QVariant.Int) ] )
            pr.addAttributes( [ QgsField("Start", QVariant.Int) ] )
            pr.addAttributes( [ QgsField("End", QVariant.Int) ] )
            vl.commitChanges()
            for i in range(len(tabdelfin)):
                vl.startEditing()
                vl.changeAttributeValue(i+1,0, int(i+1))
                vl.changeAttributeValue(i+1,1,int(tabdelfin[i][0]))
                vl.changeAttributeValue(i+1,2,int(tabdelfin[i][1]))
                vl.commitChanges()
        if indicateur=="Minimum Spanning Tree":
            if str(oriente)=="Yes" :
                QMessageBox.information(None, " Message : ", "Graph needs to be undirected")
            if str(oriente)=="No" :
                epsg=canvas.mapRenderer().destinationCrs().authid()
                v = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "MST", "memory")
                p = v.dataProvider()
                v.startEditing()
                p.addAttributes( [ QgsField("ID", QVariant.Int) ] )
                p.addAttributes( [ QgsField(arc_start, QVariant.Int) ] )
                p.addAttributes( [ QgsField(arc_end, QVariant.Int) ] )
                p.addAttributes( [ QgsField("ID_Net", QVariant.Int) ] )
                v.commitChanges()
                r = nx.minimum_spanning_tree(G)
                res = r.edges(data=True)
                id = 1
                for i in range(len(res)):
                    val=0
                    valsave = 0
                    for j in range(len(table)):
                        if (res[i][0] == table[j][0]) and (res[i][1] == table[j][1]) :
                            valsave = val
                        if (res[i][1] == table[j][0]) and (res[i][0] == table[j][1]) :
                            valsave = val
                        val = val + 1
                    fet = QgsFeature()
                    fet.setGeometry(QgsGeometry.fromPolyline(geo[valsave]))
                    fet.setAttributes([id, int(table[valsave][0]), int(table[valsave][1]), valsave + 1])
                    v.startEditing()
                    p.addFeatures( [ fet ] )
                    v.commitChanges()
                    id = id + 1
                QgsMapLayerRegistry.instance().addMapLayer(v)
        if indicateur=="Find Cliques":
            if str(oriente)=="Yes" :
                QMessageBox.information(None, " Message : ", "Graph needs to be undirected")
            if str(oriente)=="No" :
                testzero,ok1 = QInputDialog.getInt(None,"Model"," Enter the minimun cliques nodes ? : ", 3)
                if ok1 :
                    tablen = []
                    tablengeo = []
                    feat2 = QgsFeature()
                    field2 = provider2.fields()
                    fit2 = provider2.getFeatures()
                    while fit2.nextFeature(feat2):
                        tablengeo = tablengeo + [feat2.geometry().asPoint()]
                        tablen = tablen + [feat2.attributes()]
                    cl = list(nx.find_cliques(G))
                    for i in range(len(cl)):
                        if len(cl[i]) >= int(testzero) :
                            epsg = canvas.mapRenderer().destinationCrs().authid()
                            v = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Clique_"+str(i), "memory")
                            p = v.dataProvider()
                            v.startEditing()
                            for j in range(field.count()):
                                p.addAttributes( [field[j]] )
                            v.commitChanges()
                            for j in range(len(cl[i])-1):
                                for k in range(len(cl[i])-1-j):
                                    try : 
                                        valsave = table2.index((cl[i][j],cl[i][k+j+1]))
                                    except :
                                        valsave = table2.index((cl[i][k+j+1],cl[i][j]))
                                    fet = QgsFeature()
                                    fet.setGeometry(QgsGeometry.fromPolyline(geo[valsave]))
                                    fet.setAttributes(table3[valsave])
                                    v.startEditing()
                                    p.addFeatures( [ fet ] )
                                    v.commitChanges()
                            v2 = QgsVectorLayer("Point?crs=epsg:"+str(epsg), "Clique_n_"+str(i), "memory")
                            p2 = v2.dataProvider()
                            v2.startEditing()
                            for j in range(field2.count()):
                                p2.addAttributes( [field2[j]] )
                            v2.commitChanges()
                            for j in range(len(cl[i])):
                                fet = QgsFeature()
                                fet.setGeometry(QgsGeometry.fromPoint(tablengeo[int(cl[i][j])-1]))
                                fet.setAttributes(tablen[int(cl[i][j])-1])
                                v2.startEditing()
                                p2.addFeatures( [ fet ] )
                                v2.commitChanges()    
                            QgsMapLayerRegistry.instance().addMapLayer(v)
                            QgsMapLayerRegistry.instance().addMapLayer(v2)
        if indicateur == "All Shortest Paths (Distancier)":
            epsg = canvas.mapRenderer().destinationCrs().authid()
            field2 = provider2.fields()
            f = []
            for i in range(field2.count()):
                f = f + [str(field2[i].name())]
            chn1, ok1 = QInputDialog.getItem(None,"Start Field","Choose Start Field : ", f, editable = False)
            if ok1 :
                chn2, ok2 = QInputDialog.getItem(None,"End Field","Choose End Field : ", f, editable = False)
                if ok2 :
                    sstart = []
                    ssend = []
                    sstart2 = []
                    ssend2 = []
                    geompt = []
                    feat2 = QgsFeature()
                    fit2 = provider2.getFeatures()
                    num =  1
                    while fit2.nextFeature(feat2):
                        startind2 = provider2.fieldNameIndex(str(chn1))
                        endind2 = provider2.fieldNameIndex(str(chn2))
                        if float(feat2.attributes()[startind2]) > 0 :
                            sstart = sstart + [feat2.attributes()[startind2]]
                            sstart2 = sstart2 + [num]
                        if float(feat2.attributes()[endind2]) > 0 :
                            ssend = ssend + [feat2.attributes()[endind2]]
                            ssend2 = ssend2 + [num]
                        geompt = geompt + [feat2.geometry().asPoint()]
                        num = num + 1
                    v = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "SPL", "memory")
                    p = v.dataProvider()
                    v.startEditing()
                    p.addAttributes( [ QgsField("ID_Start", QVariant.Int) ] )
                    p.addAttributes( [ QgsField("ID_End", QVariant.Int) ] )
                    p.addAttributes( [ QgsField("DIST_NET", QVariant.Double) ] )
                    v.commitChanges()
                    for i in range(len(sstart2)):
                        for j in range(len(ssend2)):
                            if sstart2[i] != ssend2[j] :
                                try :
                                    val = nx.shortest_path_length(G,sstart2[i],ssend2[j],weight='weight') * sstart[i]
                                except :
                                    val = 99999999999999999999999
                            if sstart2[i] == ssend2[j] :
                                    val = 0
                            fet = QgsFeature()
                            fet.setGeometry( QgsGeometry.fromPolyline([ geompt[sstart2[i]-1] , geompt[ssend2[j]-1] ]) )
                            fet.setAttributes([ sstart2[i],ssend2[j],float(val) ])
                            v.startEditing()
                            p.addFeatures( [ fet ] )
                            v.commitChanges()
                    QgsMapLayerRegistry.instance().addMapLayer(v)
        if indicateur == "Transportation Problem":
            epsg = canvas.mapRenderer().destinationCrs().authid()
            field2 = provider2.fields()
            f = []
            for i in range(field2.count()):
                f = f + [str(field2[i].name())]
            chn1, ok1 = QInputDialog.getItem(None,"Start Field","Choose Start Field : ", f, editable = False)
            if ok1 :
                chn2, ok2 = QInputDialog.getItem(None,"End Field","Choose End Field : ", f, editable = False)
                if ok2 :
                    G2 = nx.DiGraph()
                    sstart = []
                    ssend = []
                    sstart2 = []
                    ssend2 = []
                    geompt = []
                    feat2 = QgsFeature()
                    fit2 = provider2.getFeatures()
                    num =  1
                    while fit2.nextFeature(feat2):
                        startind2 = provider2.fieldNameIndex(str(chn1))
                        endind2 = provider2.fieldNameIndex(str(chn2))
                        if float(feat2.attributes()[startind2]) > 0 :
                            va = feat2.attributes()[startind2]
                            sstart = sstart + [float(va)]
                            sstart2 = sstart2 + [num]
                            G2.add_node(num, demand = -float(va))
                        if float(feat2.attributes()[endind2]) > 0 :
                            va = feat2.attributes()[endind2]
                            ssend = ssend + [float(va)]
                            ssend2 = ssend2 + [num]
                            G2.add_node(num, demand = float(va)) #attention pt de depart et darrivee doivent etre differents
                        geompt = geompt + [feat2.geometry().asPoint()]
                        num = num + 1
                    for i in range(len(sstart2)):
                        for j in range(len(ssend2)):
                            if sstart2[i] != ssend2[j]:
                                try :
                                    val = nx.shortest_path_length(G,sstart2[i],ssend2[j],weight='weight')
                                except :
                                    val = 99999999999999999999999
                                G2.add_edge(sstart2[i], ssend2[j], weight=int(val), capacity=sstart[i]) #attention les distances sont entieres
                    flowCost, flowDict = nx.network_simplex(G2)
                    v = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "TSP", "memory")
                    p = v.dataProvider()
                    v.startEditing()
                    v.startEditing()
                    p.addAttributes( [ QgsField("ID_Start", QVariant.Int) ] )
                    p.addAttributes( [ QgsField("ID_End", QVariant.Int) ] )
                    p.addAttributes( [ QgsField("ASSIGN", QVariant.Double) ] )
                    v.commitChanges()
                    for i in range(len(sstart2)):
                        for j in range(len(ssend2)):
                            if float(flowDict[sstart2[i]][ssend2[j]]) > 0 :
                                fet = QgsFeature()
                                fet.setGeometry( QgsGeometry.fromPolyline([ geompt[sstart2[i]-1] , geompt[ssend2[j]-1] ]) )
                                fet.setAttributes([ sstart2[i],ssend2[j],float(flowDict[sstart2[i]][ssend2[j]]) ])
                                v.startEditing()
                                p.addFeatures( [ fet ] )
                                v.commitChanges()
                    QgsMapLayerRegistry.instance().addMapLayer(v)								
                    QMessageBox.information(None, " Total Cost ", "Total Cost : "+ str(flowCost))
        if indicateur == "PMedian" :
            epsg = canvas.mapRenderer().destinationCrs().authid()
            field2 = provider2.fields()
            f = []
            for i in range(field2.count()):
                f = f + [str(field2[i].name())]
            chn1, ok1 = QInputDialog.getItem(None,"Start Field","Choose Start Field (demand) : ", f, editable = False)
            if ok1 :
                chn2, ok2 = QInputDialog.getItem(None,"End Field","Choose End Field (supply) : ", f, editable = False)
                if ok2 :
                    chn3, ok3 = QInputDialog.getInt(None,"P number","P number : ", 2)
                    if ok3 :
                        sstart = []
                        ssend = []
                        sstart2 = []
                        ssend2 = []
                        geompt = []
                        feat2 = QgsFeature()
                        fit2 = provider2.getFeatures()
                        num =  1
                        while fit2.nextFeature(feat2):
                            startind2 = provider2.fieldNameIndex(str(chn1))
                            endind2 = provider2.fieldNameIndex(str(chn2))
                            if float(feat2.attributes()[startind2]) > 0 :
                                sstart = sstart + [feat2.attributes()[startind2]]
                                sstart2 = sstart2 + [num]
                            if float(feat2.attributes()[endind2]) > 0 :
                                ssend = ssend + [feat2.attributes()[endind2]]
                                ssend2 = ssend2 + [num]
                            geompt = geompt + [feat2.geometry().asPoint()]
                            num = num + 1
                        tabdist = []
                        for i in range(len(sstart2)):
                            ligne = []
                            for j in range(len(ssend2)):
                                if sstart2[i] != ssend2[j]:
                                    try :
                                        val = nx.shortest_path_length(G,sstart2[i],ssend2[j],weight='weight') * sstart[i]
                                    except :
                                        val = 99999999999999999999999
                                if sstart2[i] == ssend2[j] :
                                    val = 0
                                ligne = ligne + [float(val)]
                            tabdist = tabdist + [ligne[:]]
                        #fuzzy algorithm
                        td = copy.deepcopy(tabdist)
                        res = []
                        noeudarr = range(len(ssend2))
                        noeuddep = range(len(sstart2))
                        for i in range(int(chn3)):
                            dcumfinmin = 999999999999999999999999999999999999999999
                            for l in noeudarr:
                                dcum = 0
                                for l2 in range(len(sstart2)):
                                    dcum = dcum + td[l2][l]
                                if dcum < dcumfinmin:
                                    dcumfinmin = dcum
                                    respro = l
                            res = res + [respro] 
                            noeudarr.remove(respro)
                            for l in noeudarr:
                                for l2 in noeuddep :
                                    if td[l2][l] > td[l2][respro]:
                                        td[l2][l] = td[l2][respro]
                        #fuzzy cost
                        dtotmin = 0
                        for l3 in noeuddep:
                            ligne = []
                            for l4 in res:
                                ligne = ligne + [tabdist[l3][l4]]
                            dtotmin = dtotmin + min(ligne)
                        #neighbour algorithm
                        titulaire = copy.deepcopy(res)
                        remplacant = copy.deepcopy(noeudarr)
                        ancien = []
                        while ancien != titulaire :
                            ancien = copy.deepcopy(titulaire)
                            for l in range(len(remplacant)):
                                for l2 in range(len(titulaire)):
                                    newcomb = copy.deepcopy(titulaire)
                                    newcomb[l2] = int(remplacant[l])
                                    dtot = 0
                                    for l3 in noeuddep :
                                        ligne = []
                                        for l4 in newcomb :
                                            ligne = ligne + [tabdist[l3][l4]]
                                        dtot = dtot + min(ligne)
                                    if dtot < dtotmin :
                                        dtotmin = dtot
                                        remplacant[l] = int(titulaire[l2])
                                        titulaire = copy.deepcopy(newcomb[:])
                        v = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Pmedian", "memory")
                        p = v.dataProvider()
                        v.startEditing()
                        v.startEditing()
                        p.addAttributes( [ QgsField("Demand", QVariant.Int) ] )
                        p.addAttributes( [ QgsField("P_supply", QVariant.Int) ] )
                        p.addAttributes( [ QgsField("DIST", QVariant.Double) ] )
                        v.commitChanges()
                        for i in range(len(sstart2)):
                            jmin = 0
                            distjmin = tabdist[i][titulaire[0]]
                            for j in range(int(chn3)-1):
                                if tabdist[i][titulaire[j+1]] < distjmin : 
                                    jmin = j + 1
                                    distjmin = tabdist[i][titulaire[j+1]]
                            if ssend2[titulaire[jmin]] != sstart2[i]:
                                fet = QgsFeature()
                                fet.setGeometry( QgsGeometry.fromPolyline([ geompt[sstart2[i]-1] , geompt[ssend2[titulaire[jmin]]-1] ]) )
                                fet.setAttributes([ sstart2[i],ssend2[titulaire[jmin]],float(distjmin) ])
                                v.startEditing()
                                p.addFeatures( [ fet ] )
                                v.commitChanges()
                        QgsMapLayerRegistry.instance().addMapLayer(v)
                        QMessageBox.information(None, " Total Cost : ", str(dtotmin))
        QMessageBox.information(None, " Message : ", "End")
  #----------------------------------------------------------------------------------------------------------------------------------------                 Statisques             -----------------------------------------------------------------------------------------------------------------------------------
  def rune(self): 
        global canvas
        canvas = self.iface.mapCanvas()
        global allLayers
        allLayers = canvas.layers()
        global count
        count = canvas.layerCount()
        global lay
        lay=[]
        for i in allLayers:
           lay=lay+[str(i.name())]
        global table_noeud
        self.dlg = testDialogstat(self.iface.mainWindow())
        self.dlg.ui.comboBox.addItems(lay)
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("accepted()"), self.calcule)
        self.dlg.show()

  def calcule(self):
        table_etude=self.dlg.ui.comboBox.currentText()
        global ind_etude
        for j in range(count):
          if str(table_etude)==str(lay[j]) :
            ind_etude=j
        global aLayer
        aLayer = allLayers[int(ind_etude)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        fields2=[""]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
          fields2=fields2+[str(field[i].name())]
        self.dlg2 = testDialogstat2(self.iface.mainWindow())
        self.dlg2.ui.comboBox.addItems(fields)
        self.dlg2.ui.comboBox2.addItems(fields2)
        self.dlg2.ui.comboBox3.addItems(["Summarize","Correlation (Pearson)", "Distribution"])  
        QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2e)
        self.dlg2.show()

  def calcul2e(self):
        global champ
        champ=self.dlg2.ui.comboBox.currentText()
        champ2=self.dlg2.ui.comboBox2.currentText()
        indicateur=self.dlg2.ui.comboBox3.currentText()
        champind=provider.fieldNameIndex(str(champ))
        if indicateur == "Summarize" :
            table =[]
            feat = QgsFeature()
            fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([champind]) )
            while fit1.nextFeature(feat):
                attrs=feat.attributes()[champind]
                table=table+[attrs] 
            atable = np.array(table)
            so = np.sum(atable)
            m = np.mean(atable)
            s = np.std(atable)
            mini = min(table)
            maxi = max(table)
            QMessageBox.information(None, " Message : ", "Total : " + str(so) + "<br> <br> Average : " + str(m) + "<br> <br> Standard Deviation : " + str(s)+ "<br> <br> Minimum : " + str(mini)+ "<br> <br> Maximum : " + str(maxi))
            QMessageBox.information(None, " Message : ", "End")
        if indicateur == "Correlation (Pearson)"  and testmatplotview == 1:
            global atable
            global champ
            global champ2
            champind2=provider.fieldNameIndex(str(champ2))
            table =[]
            feat = QgsFeature()
            fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([champind, champind2]) )
            while fit1.nextFeature(feat):
                attrs=feat.attributes()[champind]
                attrs2=feat.attributes()[champind2]
                table=table+[(attrs, attrs2)]
            atable= np.array(table)
            reg = np.polyfit(atable[:,0], atable[:,1], 1)
            corr = np.corrcoef(atable[:,0], atable[:,1])
            self.dlg3 = testMatplot(self.iface.mainWindow())
            ax = self.dlg3.ui.figure.add_subplot(111)
            ax.plot(atable[:,0],atable[:,1], 'ro')
            minix = min(atable[:,0])
            maxix = max(atable[:,0])
            miniy = minix * reg[0] + reg[1]
            maxiy = maxix * reg[0] + reg[1]
            ax.set_xlabel(str(champ))
            ax.set_ylabel(str(champ2))
            ax.text(0.95, 0.93, 'Y = ' + str(reg[0]) + ' X + ' + str(reg[1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
            ax.text(0.95, 0.87, 'R = ' + str(corr[0][1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
            ax.plot([minix,maxix],[miniy,maxiy], 'r')
            self.dlg3.ui.canvas.draw()
            QObject.connect(self.dlg3.ui.bouton1, SIGNAL("clicked()"), self.change2)
            self.dlg3.ui.comboBox.addItems(["Linear","Log-Log"])
            self.dlg3.show()
        if indicateur == "Correlation (Pearson)"  and testmatplotview == 0:
            QMessageBox.information(None, " Message : ", "Your QGIS version is not compatible")
        if indicateur == "Distribution" and testmatplotview == 1 :
            global tabledistrib
            tabledistrib =[]
            feat = QgsFeature()
            fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([champind]) )
            while fit1.nextFeature(feat):
                attrs=feat.attributes()[champind]
                tabledistrib=tabledistrib+[attrs] 
            tritable = sorted(tabledistrib)
            self.dlg3 = testMatplot(self.iface.mainWindow())
            ax = self.dlg3.ui.figure.add_subplot(111)
            ax.plot(tritable, 'ro')
            ax.set_xlabel('Rank')
            ax.set_ylabel(str(champ))
            self.dlg3.ui.canvas.draw()
            QObject.connect(self.dlg3.ui.bouton1, SIGNAL("clicked()"), self.change)
            self.dlg3.ui.comboBox.addItems(["Plot Ranking","Histogram", "Plot distribution", "Plot cumulative distribution"])
            self.dlg3.show()
        if indicateur == "Distribution" and testmatplotview == 0 :
            QMessageBox.information(None, " Message : ", "Your QGIS version is not compatible")

  def change(self):
        valchange=self.dlg3.ui.comboBox.currentText()
        if str(valchange) == "Histogram" :
            num,ok = QInputDialog.getInt(None,"Bins","Enter the number of bins : ", 5)
            if ok:
                atable= np.array(tabledistrib)
                self.dlg3.ui.figure.clear()
                ax = self.dlg3.ui.figure.add_subplot(111)
                ax.hist(atable,num,color='r',normed=False)
                ax.set_xlabel(str(champ))
                ax.set_ylabel('Frequency')
                self.dlg3.ui.canvas.draw()
                self.dlg3.show()
        if str(valchange) == "Plot Ranking" :
            tritable = sorted(tabledistrib)
            self.dlg3.ui.figure.clear()
            ax = self.dlg3.ui.figure.add_subplot(111)
            ax.plot(tritable, 'ro')
            ax.set_xlabel('Rank')
            ax.set_ylabel(str(champ))
            self.dlg3.ui.canvas.draw()
            self.dlg3.show()
        if str(valchange) == "Plot cumulative distribution"	: 
            tritable = sorted(tabledistrib, reverse=True)
            func,ok = QInputDialog.getItem(None,"Function","Do you want to draw function ?", ["No","Linear", "Power Law"], editable = False)
            if ok :
                if func == 'No':
                    self.dlg3.ui.figure.clear()
                    val = set(tritable)
                    trival = sorted(val, reverse=True)
                    ct = [tritable.count(trival[0])/float(len(tritable))]
                    for i in range(len(val)-1):
                        ct = ct + [ct[i]+ (tritable.count(trival[i+1])/float(len(tritable)))]
                    ax = self.dlg3.ui.figure.add_subplot(111)
                    ax.plot(trival, ct, 'ro')
                    ax.set_xlabel(str(champ))
                    ax.set_ylabel('P(X < x)')
                    self.dlg3.ui.canvas.draw()
                if func == 'Linear':
                    self.dlg3.ui.figure.clear()
                    val = set(tritable)
                    trival = sorted(val, reverse=True)
                    ct = [tritable.count(trival[0])/float(len(tritable))]
                    for i in range(len(val)-1):
                        ct = ct + [ct[i]+ (tritable.count(trival[i+1])/float(len(tritable)))]
                    reg = np.polyfit(trival, ct, 1)
                    corr = np.corrcoef(trival, ct)
                    ax = self.dlg3.ui.figure.add_subplot(111)
                    ax.plot(trival, ct, 'ro')
                    ax.set_xlabel(str(champ))
                    ax.set_ylabel('P(X < x)')
                    minix = min(trival)
                    maxix = max(trival)
                    miniy = minix * reg[0] + reg[1]
                    maxiy = maxix * reg[0] + reg[1]
                    ax.text(0.95, 0.93, 'Y = ' + str(reg[0]) + ' X + ' + str(reg[1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
                    ax.text(0.95, 0.87, 'R = ' + str(corr[0][1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
                    ax.plot([minix,maxix],[miniy,maxiy], 'r')
                    self.dlg3.ui.canvas.draw()
                if func == 'Power Law':
                    self.dlg3.ui.figure.clear()
                    val = set(tritable)
                    trival = sorted(val, reverse=True)
                    ct = [tritable.count(trival[0])/float(len(tritable))]
                    for i in range(len(val)-1):
                        ct = ct + [ct[i]+ (tritable.count(trival[i+1])/float(len(tritable)))]
                    reg = np.polyfit(np.log10(trival), np.log10(ct), 1)
                    corr = np.corrcoef(np.log10(trival), np.log10(ct))
                    ax = self.dlg3.ui.figure.add_subplot(111)
                    ax.plot(np.log10(trival), np.log10(ct), 'ro')
                    ax.set_xlabel('Log('+str(champ)+')')
                    ax.set_ylabel('Log(P(X < x))')
                    minix = np.log10(min(trival))
                    maxix = np.log10(max(trival))
                    miniy = minix * reg[0] + reg[1]
                    maxiy = maxix * reg[0] + reg[1]
                    ax.text(0.95, 0.93, 'Y = ' + str(reg[0]) + ' X + ' + str(reg[1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
                    ax.text(0.95, 0.87, 'R = ' + str(corr[0][1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
                    ax.plot([minix,maxix],[miniy,maxiy], 'r')
                    self.dlg3.ui.canvas.draw()
        if str(valchange) == "Plot distribution"	: 
            tritable = sorted(tabledistrib, reverse=True)
            func,ok = QInputDialog.getItem(None,"Function","Do you want to draw function ?", ["No","Linear", "Power Law"], editable = False)
            if ok :
                if func == 'No':
                    self.dlg3.ui.figure.clear()
                    val = set(tritable)
                    trival = sorted(val, reverse=True)
                    ct = [tritable.count(trival[0])/float(len(tritable))]
                    for i in range(len(val)-1):
                        ct = ct + [tritable.count(trival[i+1])/float(len(tritable))]
                    ax = self.dlg3.ui.figure.add_subplot(111)
                    ax.plot(trival, ct, 'ro')
                    ax.set_xlabel(str(champ))
                    ax.set_ylabel('P(X = x)')
                    self.dlg3.ui.canvas.draw()
                if func == 'Linear':
                    self.dlg3.ui.figure.clear()
                    val = set(tritable)
                    trival = sorted(val, reverse=True)
                    ct = [tritable.count(trival[0])/float(len(tritable))]
                    for i in range(len(val)-1):
                        ct = ct + [tritable.count(trival[i+1])/float(len(tritable))]
                    reg = np.polyfit(trival, ct, 1)
                    corr = np.corrcoef(trival, ct)
                    ax = self.dlg3.ui.figure.add_subplot(111)
                    ax.plot(trival, ct, 'ro')
                    ax.set_xlabel(str(champ))
                    ax.set_ylabel('P(X = x)')
                    minix = min(trival)
                    maxix = max(trival)
                    miniy = minix * reg[0] + reg[1]
                    maxiy = maxix * reg[0] + reg[1]
                    ax.text(0.95, 0.93, 'Y = ' + str(reg[0]) + ' X + ' + str(reg[1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
                    ax.text(0.95, 0.87, 'R = ' + str(corr[0][1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
                    ax.plot([minix,maxix],[miniy,maxiy], 'r')
                    self.dlg3.ui.canvas.draw()
                if func == 'Power Law':
                    self.dlg3.ui.figure.clear()
                    val = set(tritable)
                    trival = sorted(val, reverse=True)
                    ct = [tritable.count(trival[0])/float(len(tritable))]
                    for i in range(len(val)-1):
                        ct = ct + [tritable.count(trival[i+1])/float(len(tritable))]
                    reg = np.polyfit(np.log10(trival), np.log10(ct), 1)
                    corr = np.corrcoef(np.log10(trival), np.log10(ct))
                    ax = self.dlg3.ui.figure.add_subplot(111)
                    ax.plot(np.log10(trival), np.log10(ct), 'ro')
                    ax.set_xlabel('Log('+str(champ)+')')
                    ax.set_ylabel('Log(P(X = x))')
                    minix = np.log10(min(trival))
                    maxix = np.log10(max(trival))
                    miniy = minix * reg[0] + reg[1]
                    maxiy = maxix * reg[0] + reg[1]
                    ax.text(0.95, 0.93, 'Y = ' + str(reg[0]) + ' X + ' + str(reg[1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
                    ax.text(0.95, 0.87, 'R = ' + str(corr[0][1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
                    ax.plot([minix,maxix],[miniy,maxiy], 'r')
                    self.dlg3.ui.canvas.draw()

  def change2(self):
        valchange=self.dlg3.ui.comboBox.currentText()
        if str(valchange) == "Log-Log" :
            self.dlg3.ui.figure.clear()
            logatable = np.log10(atable)
            reg = np.polyfit(logatable[:,0], logatable[:,1], 1)
            corr = np.corrcoef(logatable[:,0], logatable[:,1])
            ax = self.dlg3.ui.figure.add_subplot(111)
            ax.plot(logatable[:,0],logatable[:,1], 'ro')
            minix = min(logatable[:,0])
            maxix = max(logatable[:,0])
            miniy = minix * reg[0] + reg[1]
            maxiy = maxix * reg[0] + reg[1]
            ax.set_xlabel('Log('+str(champ)+')')
            ax.set_ylabel('Log('+str(champ2)+')')
            ax.text(0.95, 0.93, 'Y = ' + str(reg[0]) + ' X + ' + str(reg[1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
            ax.text(0.95, 0.87, 'R = ' + str(corr[0][1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
            ax.plot([minix,maxix],[miniy,maxiy], 'r')
            self.dlg3.ui.canvas.draw()
            self.dlg3.show()
        if str(valchange) == "Linear" :
            self.dlg3.ui.figure.clear()
            reg = np.polyfit(atable[:,0], atable[:,1], 1)
            corr = np.corrcoef(atable[:,0], atable[:,1])
            ax = self.dlg3.ui.figure.add_subplot(111)
            ax.plot(atable[:,0],atable[:,1], 'ro')
            minix = min(atable[:,0])
            maxix = max(atable[:,0])
            miniy = minix * reg[0] + reg[1]
            maxiy = maxix * reg[0] + reg[1]
            ax.set_xlabel(str(champ))
            ax.set_ylabel(str(champ2))
            ax.text(0.95, 0.93, 'Y = ' + str(reg[0]) + ' X + ' + str(reg[1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
            ax.text(0.95, 0.87, 'R = ' + str(corr[0][1]), verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=10)
            ax.plot([minix,maxix],[miniy,maxiy], 'r')
            self.dlg3.ui.canvas.draw()
            self.dlg3.show()
  #----------------------------------------------------------------------------------------------------------------------------------------                 Tools             ----------------------------------------------------------------------------------------------------------------------------------- 
  def runf(self): 
        global canvas
        canvas = self.iface.mapCanvas()
        global allLayers
        allLayers = canvas.layers()
        global count
        count = canvas.layerCount()
        global lay
        lay=[]
        for i in allLayers:
           lay=lay+[str(i.name())]
        self.dlg = testDialogtool(self.iface.mainWindow())
        self.dlg.ui.comboBox.addItems(['Correct ID', 'Tables to Graph', 'Edges Table to Graph (Geocoding)', 'Planar Graph', 'Generate Subgraphs', 'Generate Cycles', 'Largest Connected Component', 'Delete Isolated Nodes/Edges', 'To Undirected Graph','Drawing Algo', 'Drawing Curved Arrow'])
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("accepted()"), self.calculf)
        self.dlg.show()

  def calculf(self):
        tool=self.dlg.ui.comboBox.currentText()
        if tool == 'Correct ID' :
            self.dlg2 = testDialog(self.iface.mainWindow())
            self.dlg2.ui.comboBox.addItems(lay)
            self.dlg2.ui.comboBox_2.addItems(lay)
            QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2fid)
            self.dlg2.show()
        if tool == 'Planar Graph' :
            global pg
            pg, ok = QInputDialog.getItem(None,"Planar Graph", "Choose your tool : ",["Create Planar Graph","Simplify Planar Graph", "Remove Leaves", "Remove Zero Degree Nodes"], editable = False )
            if ok :
                if str(pg) == "Create Planar Graph" :
                    self.dlg2 = testDialogtoolb(self.iface.mainWindow())
                    self.dlg2.ui.comboBox.addItems(lay)
                    QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2fpg)
                    self.dlg2.show()
                else :
                    self.dlg2 = testDialog(self.iface.mainWindow())
                    self.dlg2.ui.comboBox.addItems(lay)
                    self.dlg2.ui.comboBox_2.addItems(lay)
                    QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2fpgb)
                    self.dlg2.show()
        if tool == 'Tables to Graph' :
            self.dlg2 = testDialog(self.iface.mainWindow())
            self.dlg2.ui.comboBox.addItems(lay)
            self.dlg2.ui.comboBox_2.addItems(lay)
            QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2f)
            self.dlg2.show()
        if tool == 'Edges Table to Graph (Geocoding)' :
            self.dlg2 = testDialogtoolb(self.iface.mainWindow())
            self.dlg2.ui.comboBox.addItems(lay)
            QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2fet)
            self.dlg2.show()
        if tool == 'Generate Subgraphs' :
            self.dlg2 = testDialog(self.iface.mainWindow())
            self.dlg2.ui.comboBox.addItems(lay)
            self.dlg2.ui.comboBox_2.addItems(lay)
            QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2fgs)
            self.dlg2.show()
        if tool == 'Generate Cycles' :
            self.dlg2 = testDialog(self.iface.mainWindow())
            self.dlg2.ui.comboBox.addItems(lay)
            self.dlg2.ui.comboBox_2.addItems(lay)
            QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2fgc)
            self.dlg2.show()
        if tool == 'Largest Connected Component' :
            self.dlg2 = testDialog(self.iface.mainWindow())
            self.dlg2.ui.comboBox.addItems(lay)
            self.dlg2.ui.comboBox_2.addItems(lay)
            QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2flc)
            self.dlg2.show()
        if tool == 'Delete Isolated Nodes/Edges' :
            self.dlg2 = testDialog(self.iface.mainWindow())
            self.dlg2.ui.comboBox.addItems(lay)
            self.dlg2.ui.comboBox_2.addItems(lay)
            QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2fdin)
            self.dlg2.show()
        if tool == 'To Undirected Graph' :
            self.dlg2 = testDialog(self.iface.mainWindow())
            self.dlg2.ui.comboBox.addItems(lay)
            self.dlg2.ui.comboBox_2.addItems(lay)
            QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2ftoun)
            self.dlg2.show()
        if tool == 'Drawing Algo' :
            self.dlg2 = testDialog(self.iface.mainWindow())
            self.dlg2.ui.comboBox.addItems(lay)
            self.dlg2.ui.comboBox_2.addItems(lay)
            QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2fdraw)
            self.dlg2.show()
        if tool == 'Drawing Curved Arrow' :
            self.dlg2 = testDialog(self.iface.mainWindow())
            self.dlg2.ui.comboBox.addItems(lay)
            self.dlg2.ui.comboBox_2.addItems(lay)
            QObject.connect(self.dlg2.ui.buttonBox, SIGNAL("accepted()"), self.calcul2fcar)
            self.dlg2.show()

  def calcul2f(self):
        table_noeud=self.dlg2.ui.comboBox.currentText()
        table_arc=self.dlg2.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
        global nLayer
        nLayer = allLayers[int(ind_noeud)]
        global provider2
        provider2 = nLayer.dataProvider()
        global field2
        field2=provider2.fields()
        global fields2
        fields2=[]
        for i in range(field2.count()):
          fields2=fields2+[str(field2[i].name())]
        self.dlg3 = testDialogtoolTTP(self.iface.mainWindow())
        self.dlg3.ui.comboBox.addItems(fields2)
        self.dlg3.ui.comboBoxb.addItems(fields2)
        self.dlg3.ui.comboBoxc.addItems(fields2)
        self.dlg3.ui.comboBox2.addItems(fields)
        self.dlg3.ui.comboBox2b.addItems(fields)
        QObject.connect(self.dlg3.ui.buttonBox, SIGNAL("accepted()"), self.calcul3f)
        self.dlg3.show()

  def calcul2flc(self):
        table_noeud=self.dlg2.ui.comboBox.currentText()
        table_arc=self.dlg2.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
        global nLayer
        nLayer = allLayers[int(ind_noeud)]
        global provider2
        provider2 = nLayer.dataProvider()
        global field2
        field2=provider2.fields()
        global fields2
        fields2=[]
        for i in range(field2.count()):
          fields2=fields2+[str(field2[i].name())]
        self.dlg3 = testDialogtoollc(self.iface.mainWindow())
        self.dlg3.ui.comboBox.addItems(fields)
        self.dlg3.ui.comboBox_2.addItems(fields)
        self.dlg3.ui.comboBox_3.addItems(["No","Yes"])
        self.dlg3.ui.comboBox_4.addItems(["No","Yes"])
        self.dlg3.ui.comboBox_5.addItems([""]+fields)
        QObject.connect(self.dlg3.ui.buttonBox, SIGNAL("accepted()"), self.calcul3flc)
        self.dlg3.show()

  def calcul2fdraw(self):
     if testmatplotview == 1 :
        table_noeud=self.dlg2.ui.comboBox.currentText()
        table_arc=self.dlg2.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
        global nLayer
        nLayer = allLayers[int(ind_noeud)]
        global provider2
        provider2 = nLayer.dataProvider()
        global field2
        field2=provider2.fields()
        global fields2
        fields2=[]
        for i in range(field2.count()):
          fields2=fields2+[str(field2[i].name())]
        self.dlg3 = testDialogdraw2(self.iface.mainWindow())
        self.dlg3.ui.comboBox.addItems(fields)
        self.dlg3.ui.comboBox_2.addItems(fields)
        self.dlg3.ui.comboBox_3.addItems(["No","Yes"])
        self.dlg3.ui.comboBox_4.addItems(["No","Yes"])
        self.dlg3.ui.comboBox_5.addItems([""]+fields)
        self.dlg3.ui.comboBox_6.addItems(["Fruchterman-Reingold force-directed algorithm","Spectral", "Circular", "Force Atlas"])  
        QObject.connect(self.dlg3.ui.buttonBox, SIGNAL("accepted()"), self.calcul3fdraw)
        self.dlg3.show()
     if testmatplotview == 0 :
        QMessageBox.information(None, " Message : ", "Your QGIS version is not compatible")

  def calcul2fpg(self):
        epsg=canvas.mapRenderer().destinationCrs().authid()
        table_arc=self.dlg2.ui.comboBox.currentText()
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        Layer = allLayers[int(ind_arc)]
        provider = Layer.dataProvider()
        tablex = []
        tabley = []
        ct = []
        tablegeom = []
        tablegeomnew = []
        tableid = []
        tablenum = []
        feat = QgsFeature()
        fit = provider.getFeatures()
        proi = 0
        while fit.nextFeature(feat): 
            geom = feat.geometry()
            geomwkt = str(geom.exportToWkt())
            lignegeom = []
            if str(geomwkt[0:10])== 'LineString' or str(geomwkt[0:10])== 'LINESTRING' or str(geomwkt[0:10])== 'Linestring' or str(geomwkt[0:10])== 'linestring':
                geomwkt2 = string.split(geomwkt,'(')
                geomwkt3 = string.split(geomwkt2[1],')')
                geomwkt4 = string.split(geomwkt3[0],',')
                for i in range(len(geomwkt4)):
                    geomwkt5 = string.split(geomwkt4[i],' ')
                    if i == 0 : 
                        x = float(geomwkt5[0])
                        y = float(geomwkt5[1])
                    if i != 0 : 
                        x = float(geomwkt5[1])
                        y = float(geomwkt5[2])
                    if i == 0 or i == len(geomwkt4)- 1 :
                        test = 0
                        for testx in enumerate(tablex):
                            if testx[1] == x :
                                if tabley[testx[0]] == y :
                                    test = 1
                                    a = testx[0]
                        if test == 0 :
                            tablex = tablex + [x]
                            tabley = tabley + [y]
                            ct = ct + [1]
                            if i == 0 :
                                id1 = len(tablex)
                            if i == len(geomwkt4)- 1 :
                                id2 = len(tabley)
                        if test == 1 :
                            ct [a] = ct[a] + 1
                            if i == 0 :
                                id1 = int(a) + 1
                            if i == len(geomwkt4)- 1 :
                                id2 = int(a) + 1
                    lignegeom = lignegeom + [[x,y]]
                tablegeom = tablegeom + [lignegeom[:]]
                tablegeomnew = tablegeomnew + [lignegeom[:]]
                tableid = tableid + [[id1, id2]]
                tablenum = tablenum + [proi]
            if str(geomwkt[0:15])== 'MultiLineString' or str(geomwkt[0:15])== 'MULTILINESTRING'  or str(geomwkt[0:15])== 'Multilinestring' or str(geomwkt[0:15])== 'multilinestring' :
                geomwkt2 = string.split(geomwkt,'(')
                for j in range(len(geomwkt2)-2): 
                  lignegeompro = []
                  geomwkt3 = string.split(geomwkt2[j+2],')')
                  geomwkt4 = string.split(geomwkt3[0],',')
                  for i in range(len(geomwkt4)):
                    geomwkt5 = string.split(geomwkt4[i],' ')
                    if i == 0 : 
                        x = float(geomwkt5[0])
                        y = float(geomwkt5[1])
                    if i != 0 : 
                        x = float(geomwkt5[1])
                        y = float(geomwkt5[2])
                    if i == 0 or i == len(geomwkt4)- 1 :
                        test = 0
                        for testx in enumerate(tablex):
                            if testx[1] == x :
                                if tabley[testx[0]] == y :
                                    test=1
                                    a=testx[0]
                        if test == 0 :
                            tablex = tablex + [x]
                            tabley = tabley + [y]
                            ct = ct + [1]
                            if i == 0 :
                                id1 = len(tablex)
                            if i == len(geomwkt4)- 1 :
                                id2 = len(tabley)
                        if test == 1 :
                            ct [a] = ct[a] + 1
                            if i == 0 :
                                id1 = int(a) + 1
                            if i == len(geomwkt4)- 1 :
                                id2 = int(a) + 1
                    lignegeompro = lignegeompro + [[x,y]]
                  tableid = tableid + [[id1, id2]]
                  tablenum = tablenum + [proi]
                  lignegeom = lignegeom + [lignegeompro[:]]
                tablegeom = tablegeom + lignegeom[:]
                tablegeomnew = tablegeomnew + lignegeom[:]
            proi = proi + 1
        for i in range(len(tablegeom)):
            compte = 0
            for j in range(len(tablegeom[i])-1): 
                line_feature = QgsFeature()
                line_feature.setGeometry( QgsGeometry.fromPolyline([ QgsPoint(tablegeom[i][j][0],tablegeom[i][j][1]),QgsPoint(tablegeom[i][j+1][0],tablegeom[i][j+1][1]) ]) )	 
                cands = Layer.getFeatures(QgsFeatureRequest().setFilterRect(line_feature.geometry().boundingBox()))
                stockpt = []
                for line_feature2 in cands:
                    if line_feature.geometry().intersects(line_feature2.geometry()):
                        intersection = line_feature.geometry().intersection(line_feature2.geometry()).exportToWkt() 
                        if str(intersection[0:5]) == 'Point' or str(intersection[0:5]) == 'POINT' or str(intersection[0:5]) == 'point':
                            geomwkt2 = string.split(intersection,'(')
                            geomwkt3 = string.split(geomwkt2[1],')')
                            geomwkt4 = string.split(geomwkt3[0],' ')
                            x = float(geomwkt4[0])
                            y = float(geomwkt4[1])
                            test = 0
                            for testx in enumerate(tablex):
                                if testx[1] == x :
                                    if tabley[testx[0]] == y :
                                        test=1
                                        a=testx[0]
                            if test == 0 :
                                tablex = tablex + [x]
                                tabley = tabley + [y]
                                ct = ct + [1]
                                id1 = len(tablex)
                            if test == 1 :
                                ct [a] = ct[a] + 1
                                id1 = int(a) + 1 
                            dist = abs(tablegeom[i][j][0] - x)
                            stockpt = stockpt + [[dist,x,y,id1]]
                        if str(intersection[0:10]) == 'MultiPoint' or str(intersection[0:10]) == 'MULTIPOINT' or str(intersection[0:10]) == 'Multipoint' or str(intersection[0:10]) == 'multipoint':
                            geomwkt2 = string.split(intersection,'(')
                            for k in range(len(geomwkt2)-2):
                                geomwkt3 = string.split(geomwkt2[k+2],')')
                                geomwkt4 = string.split(geomwkt3[0],' ')
                                x = float(geomwkt4[0])
                                y = float(geomwkt4[1])
                                test = 0
                                for testx in enumerate(tablex):
                                    if testx[1] == x :
                                        if tabley[testx[0]] == y :
                                            test=1
                                            a=testx[0]
                                if test == 0 :
                                    tablex = tablex + [x]
                                    tabley = tabley + [y]
                                    ct = ct + [1]
                                    id1 = len(tablex)
                                if test == 1 :
                                    ct [a] = ct[a] + 1
                                    id1 = int(a) + 1 
                                dist = abs(tablegeom[i][j][0] - x)
                                stockpt = stockpt + [[dist,x,y,id1]]
                stockptri = sorted(stockpt)
                jb = compte + 2
                if len(stockpt) > 0:
                    iddep=tableid[i][0]
                    idarr=tableid[i][1]
                    for k in range(len(stockpt)):
                        ligne1 = tablegeomnew[i][0:jb]
                        ligne1[jb-1] = [stockptri[k][1],stockptri[k][2]]
                        if len(ligne1) > 2 :
                            tablegeomnew[i][0:jb-1] = [[stockptri[k][1],stockptri[k][2]]]
                            tableid[i] = [stockptri[k][3],idarr]
                        if len(ligne1) == 2 :
                            tablegeomnew[i][0:1] = [[stockptri[k][1],stockptri[k][2]]]
                            tableid[i] = [stockptri[k][3],idarr]
                        jb = 2	
                        tablegeomnew = tablegeomnew + [ligne1]	
                        tableid = tableid + [[iddep,stockptri[k][3]]]
                        tablenum = tablenum + [tablenum[i]]
                        iddep = stockptri[k][3]
                    compte = 0
                compte = compte + 1
        v = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges", "memory")
        p = v.dataProvider()
        p.addAttributes( [QgsField("StartNode", QVariant.Int)] )
        p.addAttributes( [QgsField("EndNode", QVariant.Int)] )
        p.addAttributes( [QgsField("OldNum", QVariant.Int)] )
        v.commitChanges()
        for i in range(len(tablegeomnew)):
            test = 0
            if len(tablegeomnew[i]) == 2 :
                if tablegeomnew[i][0][0] == tablegeomnew[i][1][0] :
                    if tablegeomnew[i][0][1] == tablegeomnew[i][1][1] :
                        test = 1
            if test == 0 :
                v.startEditing()
                fet = QgsFeature()
                textgeom = "LINESTRING(" + str(tablegeomnew[i][0][0]) + " " + str(tablegeomnew[i][0][1])
                for j in range(len(tablegeomnew[i])-1):
                    textgeom = textgeom + "," + str(tablegeomnew[i][j+1][0]) + " " + str(tablegeomnew[i][j+1][1])
                textgeom = textgeom + ")"
                fet.setGeometry(  QgsGeometry.fromWkt( textgeom ) )
                fet.setAttributes( [ int(tableid[i][0]) , int(tableid[i][1]), int(tablenum[i]) ] )
                p.addFeatures( [ fet ] )
                v.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(v)
        v2 = QgsVectorLayer("Point?crs=epsg:"+str(epsg), "Nodes", "memory")
        p2 = v2.dataProvider()
        p2.addAttributes( [QgsField("ID", QVariant.Int)] )
        v2.commitChanges()
        for i in range(len(tablex)):
            v2.startEditing()
            fet = QgsFeature()
            textgeom = "POINT(" + str(tablex[i]) + " " + str(tabley[i]) + ")"
            fet.setGeometry(  QgsGeometry.fromWkt( textgeom ) )
            fet.setAttributes( [ int(i+1) ] )
            p2.addFeatures( [ fet ] )
            v2.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(v2)	
        QMessageBox.information(None, " Message : ", "End")

  def calcul2fpgb(self):
        table_noeud=self.dlg2.ui.comboBox.currentText()
        table_arc=self.dlg2.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global eLayer
        eLayer = allLayers[int(ind_arc)]
        global provider2
        provider2 = eLayer.dataProvider()
        global field
        field=provider2.fields()
        global fields
        fields=[]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
        global nLayer
        nLayer = allLayers[int(ind_noeud)]
        global provider
        provider = nLayer.dataProvider()
        global field2
        field2=provider.fields()
        global fields2
        fields2=[]
        for i in range(field2.count()):
          fields2=fields2+[str(field2[i].name())]
        self.dlg3 = testDialogtool2(self.iface.mainWindow())
        self.dlg3.ui.comboBox.addItems(fields)
        self.dlg3.ui.comboBox2.addItems(fields)
        QObject.connect(self.dlg3.ui.buttonBox, SIGNAL("accepted()"), self.calcul3fpgb)
        self.dlg3.show()

  def calcul2fid(self):
        table_noeud=self.dlg2.ui.comboBox.currentText()
        table_arc=self.dlg2.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
        global nLayer
        nLayer = allLayers[int(ind_noeud)]
        global provider2
        provider2 = nLayer.dataProvider()
        global field2
        field2=provider2.fields()
        global fields2
        fields2=[]
        for i in range(field2.count()):
          fields2=fields2+[str(field2[i].name())]
        self.dlg3 = testDialogtoolID(self.iface.mainWindow())
        self.dlg3.ui.comboBox.addItems(fields2)
        self.dlg3.ui.comboBox2.addItems(fields)
        self.dlg3.ui.comboBox3.addItems(fields)
        QObject.connect(self.dlg3.ui.buttonBox, SIGNAL("accepted()"), self.calcul3fid)
        self.dlg3.show()

  def calcul2fet(self):
        table_arc = self.dlg2.ui.comboBox.currentText()
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field = provider.fields()
        global fields
        fields = []
        for i in range(field.count()):
          fields = fields+[str(field[i].name())]
        fields2 = [""] + fields
        self.dlg3 = testDialogtoolET(self.iface.mainWindow())
        self.dlg3.ui.comboBox.addItems(fields2)
        self.dlg3.ui.comboBox2.addItems(fields2)
        self.dlg3.ui.comboBox3.addItems(fields)
        self.dlg3.ui.comboBox4.addItems(fields2)
        self.dlg3.ui.comboBoxb.addItems(fields2)
        self.dlg3.ui.comboBox2b.addItems(fields2)
        self.dlg3.ui.comboBox3b.addItems(fields)
        self.dlg3.ui.comboBox4b.addItems(fields2)
        QObject.connect(self.dlg3.ui.buttonBox, SIGNAL("accepted()"), self.calcul3fet)
        self.dlg3.show()

  def calcul2fdin(self):
        table_noeud=self.dlg2.ui.comboBox.currentText()
        table_arc=self.dlg2.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
        global nLayer
        nLayer = allLayers[int(ind_noeud)]
        global provider2
        provider2 = nLayer.dataProvider()
        global field2
        field2=provider2.fields()
        global fields2
        fields2=[]
        for i in range(field2.count()):
          fields2=fields2+[str(field2[i].name())]
        self.dlg3 = testDialogtoolID(self.iface.mainWindow())
        self.dlg3.ui.comboBox.addItems(fields2)
        self.dlg3.ui.comboBox2.addItems(fields)
        self.dlg3.ui.comboBox3.addItems(fields)
        QObject.connect(self.dlg3.ui.buttonBox, SIGNAL("accepted()"), self.calcul3fdin)
        self.dlg3.show()

  def calcul2fgs(self):
        table_noeud=self.dlg2.ui.comboBox.currentText()
        table_arc=self.dlg2.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
        global nLayer
        nLayer = allLayers[int(ind_noeud)]
        global provider2
        provider2 = nLayer.dataProvider()
        global field2
        field2=provider2.fields()
        global fields2
        fields2=[]
        for i in range(field2.count()):
          fields2=fields2+[str(field2[i].name())]
        self.dlg3 = testDialogtoolGS(self.iface.mainWindow())
        self.dlg3.ui.comboBox.addItems(fields)
        self.dlg3.ui.comboBox_2.addItems(fields)
        self.dlg3.ui.comboBox_3.addItems(["No","Yes"])
        self.dlg3.ui.comboBox_4.addItems(fields2)
        QObject.connect(self.dlg3.ui.buttonBox, SIGNAL("accepted()"), self.calcul3fgs)
        self.dlg3.show()

  def calcul2fgc(self):
        table_noeud=self.dlg2.ui.comboBox.currentText()
        table_arc=self.dlg2.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
        global nLayer
        nLayer = allLayers[int(ind_noeud)]
        global provider2
        provider2 = nLayer.dataProvider()
        global field2
        field2=provider2.fields()
        global fields2
        fields2=[]
        for i in range(field2.count()):
          fields2=fields2+[str(field2[i].name())]
        self.dlg3 = testDialogtoollc(self.iface.mainWindow())
        self.dlg3.ui.comboBox.addItems(fields)
        self.dlg3.ui.comboBox_2.addItems(fields)
        self.dlg3.ui.comboBox_3.addItems(["No","Yes"])
        self.dlg3.ui.comboBox_4.addItems(["No","Yes"])
        self.dlg3.ui.comboBox_5.addItems([""]+fields)
        QObject.connect(self.dlg3.ui.buttonBox, SIGNAL("accepted()"), self.calcul3fgc)
        self.dlg3.show()

  def calcul2ftoun(self):  
        table_noeud=self.dlg2.ui.comboBox.currentText()
        table_arc=self.dlg2.ui.comboBox_2.currentText()
        global ind_noeud
        for j in range(count):
          if str(table_noeud)==str(lay[j]) :
            ind_noeud=j
        global nLayer
        nLayer = allLayers[int(ind_noeud)]
        global provider2
        provider2 = nLayer.dataProvider()
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        global field
        field=provider.fields()
        global fields
        fields=[]
        fields2=[""]
        for i in range(field.count()):
          fields=fields+[str(field[i].name())]
          fields2=fields2+[str(field[i].name())]
        self.dlg4 = testDialog2(self.iface.mainWindow())
        self.dlg4.ui.comboBox.addItems(fields)
        self.dlg4.ui.comboBox_2.addItems(fields)
        self.dlg4.ui.comboBox_3.addItems(["No","Yes"])
        self.dlg4.ui.comboBox_4.addItems(["No","Yes"])
        self.dlg4.ui.comboBox_5.addItems(fields2)
        self.dlg4.ui.comboBox_6.addItems([])  
        self.dlg4.ui.comboBox_7.addItems([])
        QObject.connect(self.dlg4.ui.buttonBox, SIGNAL("accepted()"), self.calcul3ftoun)
        self.dlg4.show()

  def calcul2fcar(self):
        epsg=canvas.mapRenderer().destinationCrs().authid()
        table_noeud=self.dlg2.ui.comboBox.currentText()
        table_arc=self.dlg2.ui.comboBox_2.currentText()
        global ind_arc
        for j in range(count):
          if str(table_arc)==str(lay[j]) :
            ind_arc=j
        global aLayer
        aLayer = allLayers[int(ind_arc)]
        global provider
        provider = aLayer.dataProvider()
        num1, ok1 = QInputDialog.getText(None, "Parameter 1/2",  "Decimal number (0 close to start node 1 close to end node) :", QLineEdit.Normal, "0.5")
        if ok1 :
            num2, ok2 = QInputDialog.getText(None, "Parameter 2/2",  " Curve strength :", QLineEdit.Normal, "0.5")
            if ok2 :
                t, ok3 = QInputDialog.getItem(None,"Method","Choose a method", ["Simple", "Optimized"], editable = False)
                if ok3 :
                    field = provider.fields()
                    v = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges", "memory")
                    p = v.dataProvider()
                    v.startEditing()
                    for i in range(field.count()):
                        p.addAttributes( [field[i]] )
                    v.commitChanges()
                    if t == "Simple" :
                        feat = QgsFeature()
                        fit1 = provider.getFeatures()
                        while fit1.nextFeature(feat):
                            attrs = feat.attributes()
                            geom = feat.geometry().asPolyline()
                            deltax = float(geom[1][0]) - float(geom[0][0])
                            deltay = float(geom[1][1]) - float(geom[0][1])
                            dx1 = deltax * float(num1)
                            dy1 = deltay * float(num1)
                            dx2 = - deltay * float(num2)
                            dy2 = deltax * float(num2)
                            v.startEditing()
                            fet = QgsFeature()
                            fet.setGeometry(  QgsGeometry.fromPolyline( [QgsPoint(float(geom[0][0]),float(geom[0][1])), QgsPoint(float(geom[0][0]) + dx1 + dx2 , float(geom[0][1]) + dy1 + dy2), QgsPoint(float(geom[1][0]),float(geom[1][1]))] )) 
                            fet.setAttributes( attrs )
                            p.addFeatures( [ fet ] )
                            v.commitChanges()
                    if t == "Optimized" :
                        global ind_noeud
                        for j in range(count):
                            if str(table_noeud)==str(lay[j]) :
                                ind_noeud=j
                        global nLayer
                        nLayer = allLayers[int(ind_noeud)]
                        global provider2
                        provider2 = nLayer.dataProvider()
                        feat2 = QgsFeature()
                        fit2 = provider2.getFeatures()
                        x = 0
                        y = 0
                        n = 0
                        while fit2.nextFeature(feat2):
                            x = x + float(feat2.geometry().asPoint().x())
                            y = y + float(feat2.geometry().asPoint().y())
                            n = n +1
                        xmoy = x / float(n)
                        ymoy = y / float(n)
                        feat = QgsFeature()
                        fit1 = provider.getFeatures()
                        while fit1.nextFeature(feat):
                            attrs = feat.attributes()
                            geom = feat.geometry().asPolyline()
                            deltax = float(geom[1][0]) - float(geom[0][0])
                            deltay = float(geom[1][1]) - float(geom[0][1])
                            dx1 = deltax * float(num1)
                            dy1 = deltay * float(num1)
                            dx2a = - deltay * float(num2)
                            dy2a = deltax * float(num2)
                            dx2b = deltay * float(num2)
                            dy2b = - deltax * float(num2)
                            dist1 = (xmoy - (geom[0][0] + dx1 + dx2a)) * (xmoy - (geom[0][0] + dx1 + dx2a)) + (ymoy - (geom[0][1] + dy1 + dy2a)) * (ymoy - (geom[0][1] + dy1 + dy2a))
                            dist2 = (xmoy - (geom[0][0] + dx1 + dx2b)) * (xmoy - (geom[0][0] + dx1 + dx2b)) + (ymoy - (geom[0][1] + dy1 + dy2b)) * (ymoy - (geom[0][1] + dy1 + dy2a))
                            if dist1 > dist2 :
                                dx2 = dx2a 
                                dy2 = dy2a
                            else :
                                dx2 = dx2b 
                                dy2 = dy2b						
                            v.startEditing()
                            fet = QgsFeature()
                            fet.setGeometry(  QgsGeometry.fromPolyline( [QgsPoint(float(geom[0][0]),float(geom[0][1])), QgsPoint(float(geom[0][0]) + dx1 + dx2 , float(geom[0][1])+ dy1 + dy2), QgsPoint(float(geom[1][0]),float(geom[1][1]))] )) 
                            fet.setAttributes( attrs )
                            p.addFeatures( [ fet ] )
                            v.commitChanges()
                    QgsMapLayerRegistry.instance().addMapLayer(v)

  def calcul3f(self):
        arc_start=self.dlg3.ui.comboBox2.currentText()
        arc_end=self.dlg3.ui.comboBox2b.currentText()
        ID = self.dlg3.ui.comboBoxb.currentText()
        x = self.dlg3.ui.comboBox.currentText()
        y = self.dlg3.ui.comboBoxc.currentText()
        epsg = self.dlg3.ui.lineedit.text()
        Idind=provider2.fieldNameIndex(str(ID))
        xind=provider2.fieldNameIndex(str(x))
        yind=provider2.fieldNameIndex(str(y))
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        valID = []
        xval = []
        yval = []
        fit1 = provider2.getFeatures()
        feat = QgsFeature()
        v = QgsVectorLayer("Point?crs=epsg:"+str(epsg), "Nodes", "memory")
        p = v.dataProvider()
        for i in range(field2.count()):
            p.addAttributes( [field2[i]] )
        v.commitChanges()
        while fit1.nextFeature(feat):
            valID = valID + [feat.attributes()[Idind]]
            y1=feat.attributes()[yind]
            x1 = feat.attributes()[xind]
            yval = yval + [y1]
            xval = xval + [x1]
            att = feat.attributes()
            v.startEditing()
            fet = QgsFeature()
            fet.setGeometry(  QgsGeometry.fromPoint(QgsPoint(float(x1),float(y1))) )
            fet.setAttributes( att )
            p.addFeatures( [ fet ] )
            v.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(v)
        fit2 = provider.getFeatures()
        feat2 = QgsFeature()
        vl = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges", "memory")
        pr = vl.dataProvider()
        for i in range(field.count()):
            pr.addAttributes( [field[i]] )
        vl.commitChanges()
        tabsup = []
        while fit2.nextFeature(feat2):
            test = 0
            IDstart = feat2.attributes()[startind]
            IDend = feat2.attributes()[endind]
            try :
                num1 = valID.index(IDstart)
                num2 = valID.index(IDend)
            except :
                test = 1
                tabsup = tabsup + [[IDstart, IDend]]
            if test == 0 :
              if IDstart != IDend :
                X1 = xval[num1]
                Y1 = yval[num1]
                X2 = xval[num2]
                Y2 = yval[num2]
                att = feat2.attributes()
                vl.startEditing()
                fet = QgsFeature()
                fet.setGeometry( QgsGeometry.fromPolyline([QgsPoint(float(X1),float(Y1)),QgsPoint(float(X2),float(Y2))]) )
                fet.setAttributes( att )
                pr.addFeatures( [ fet ] )
                vl.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl)
        if len(tabsup) > 0 :
            QMessageBox.information(None, " Message : ", "Mismatch : <br>" + str(tabsup))
        QMessageBox.information(None, " Message : ", "End")

  def calcul3flc(self):
        epsg=canvas.mapRenderer().destinationCrs().authid()
        arc_start=self.dlg3.ui.comboBox.currentText()
        arc_end=self.dlg3.ui.comboBox_2.currentText()
        oriente=self.dlg3.ui.comboBox_3.currentText()
        poids=self.dlg3.ui.comboBox_4.currentText()
        ponderation=self.dlg3.ui.comboBox_5.currentText()
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        table = []
        geom = []
        if str(poids)=="No":
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          table=table+[(attrsstart,attrsend)]
          geom = geom + [feat.geometry().exportToWkt()]		  
         G=nx.Graph()
         if str(oriente)=="Yes" :
            QMessageBox.information(None, " Message : ", "Here graph is considered as undirected")
         G.add_edges_from(table)
        if str(poids)=="Yes":
         distind=provider.fieldNameIndex(str(ponderation))
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind,distind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          attrsdist=feat.attributes()[distind]
          table=table+[(attrsstart,attrsend,attrsdist)] 
          geom = geom + [feat.geometry()]	
         G=nx.Graph()
         if str(oriente)=="Yes" :
            QMessageBox.information(None, " Message : ", "Here graph is considered as undirected")
         G.add_weighted_edges_from(table)
        t=nx.number_of_nodes(G)
        res = nx.connected_components(G)
        cmax = 0
        imax = 0
        for i in range(len(res)):
            if len(res[i]) > cmax:
                cmax = len(res[i])
                imax = i
        trires = sorted(res[imax])
        v = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges", "memory")
        p = v.dataProvider()
        p.addAttributes( [QgsField("ID", QVariant.Int)] )
        p.addAttributes( [QgsField("ID2", QVariant.Int)] )
        p.addAttributes( [QgsField("StartNode", QVariant.Int)] )
        p.addAttributes( [QgsField("EndNode", QVariant.Int)] )
        p.addAttributes( [QgsField("StartNode2", QVariant.Int)] )
        p.addAttributes( [QgsField("EndNode2", QVariant.Int)] )
        v.commitChanges()
        idarcnew = 1
        for i in range(len(table)):
            test = 0
            try :
                id1 = int(trires.index(table[i][0])) + 1
            except :
                test = 1
            if test == 0 :
                try :
                    id2 = int(trires.index(table[i][1])) + 1
                except :
                    test = 1
            if test == 0 :
                v.startEditing()
                fet = QgsFeature()
                fet.setGeometry( QgsGeometry.fromWkt( geom[i] ) )
                fet.setAttributes( [ int(i+1), int(idarcnew), int(table[i][0]), int(table[i][1]), int(id1), int(id2) ] )
                p.addFeatures( [ fet ] )
                v.commitChanges() 
                idarcnew = idarcnew + 1
        QgsMapLayerRegistry.instance().addMapLayer(v)
        v2 = QgsVectorLayer("Point?crs=epsg:"+str(epsg), "Nodes", "memory")
        p2 = v2.dataProvider()
        p2.addAttributes( [QgsField("ID", QVariant.Int)] )
        p2.addAttributes( [QgsField("ID2", QVariant.Int)] )
        v2.commitChanges()
        feat2 = QgsFeature()
        fit2 = provider2.getFeatures()
        i = 1
        i2 = 0
        while fit2.nextFeature(feat2):
            test = 0
            try :
                trires.index(i)
            except :
                test = 1
            if test == 0 :
                i2 = i2 + 1
                v2.startEditing()
                fet = QgsFeature()
                fet.setGeometry( feat2.geometry() )
                fet.setAttributes( [ int(i), int(i2) ] )
                p2.addFeatures( [ fet ] )
                v2.commitChanges() 				
            i = i + 1
        QgsMapLayerRegistry.instance().addMapLayer(v2)			
        QMessageBox.information(None, " Message : ", "End")

  def calcul3fgc(self):
        epsg=canvas.mapRenderer().destinationCrs().authid()
        arc_start=self.dlg3.ui.comboBox.currentText()
        arc_end=self.dlg3.ui.comboBox_2.currentText()
        oriente=self.dlg3.ui.comboBox_3.currentText()
        poids=self.dlg3.ui.comboBox_4.currentText()
        ponderation=self.dlg3.ui.comboBox_5.currentText()
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        table = []
        table2 = []
        geom = []
        if str(poids)=="No":
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          table=table+[(attrsstart,attrsend)]
          geom = geom + [feat.geometry().exportToWkt()]		  
         if str(oriente)=="No" :
            QMessageBox.information(None, " Message : ", "Directed graph is required")
         if str(oriente)=="Yes" :
           G = nx.DiGraph()
           G.add_edges_from(table)
        if str(poids)=="Yes":
         distind=provider.fieldNameIndex(str(ponderation))
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind,distind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          attrsdist=feat.attributes()[distind]
          table=table+[(attrsstart,attrsend)]
          table2=table2+[(attrsstart,attrsend,attrsdist)] 
          geom = geom + [feat.geometry()]	
         if str(oriente)=="No" :
            QMessageBox.information(None, " Message : ", "Directed graph is required")
         if str(oriente)=="Yes" :
           G = nx.DiGraph()
           G.add_weighted_edges_from(table2)
        if str(oriente)=="Yes" :
            res = list(nx.simple_cycles(G))
            if res == [] :
                QMessageBox.information(None, " Message : ", "No cycle")
            if res != [] :
                geompt = []
                feat2 = QgsFeature()
                fit2 = provider2.getFeatures()
                while fit2.nextFeature(feat2):
                    geompt = geompt + [feat2.geometry().asPoint()]
                for i in range(len(res)):
                    trires = sorted(res[i])
                    v = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges"+str(i), "memory")
                    p = v.dataProvider()
                    p.addAttributes( [QgsField("ID", QVariant.Int)] )
                    p.addAttributes( [QgsField("ID2", QVariant.Int)] )
                    p.addAttributes( [QgsField("StartNode", QVariant.Int)] )
                    p.addAttributes( [QgsField("EndNode", QVariant.Int)] )
                    p.addAttributes( [QgsField("StartNode2", QVariant.Int)] )
                    p.addAttributes( [QgsField("EndNode2", QVariant.Int)] )
                    v.commitChanges()
                    idarcnew = 1
                    for j in range(len(table)):
                        test = 0
                        try :
                            id1 = int(trires.index(table[j][0])) + 1
                        except :
                            test = 1
                        if test == 0 :
                            try :
                                id2 = int(trires.index(table[j][1])) + 1
                            except :
                                test = 1
                        if test == 0 :
                            v.startEditing()
                            fet = QgsFeature()
                            fet.setGeometry( QgsGeometry.fromWkt( geom[j] ) )
                            fet.setAttributes( [ int(j+1), int(idarcnew), int(table[j][0]), int(table[j][1]), int(id1), int(id2) ] )
                            p.addFeatures( [ fet ] )
                            v.commitChanges() 
                            idarcnew = idarcnew + 1
                    QgsMapLayerRegistry.instance().addMapLayer(v)
                    v2 = QgsVectorLayer("Point?crs=epsg:"+str(epsg), "Nodes", "memory")
                    p2 = v2.dataProvider()
                    p2.addAttributes( [QgsField("ID", QVariant.Int)] )
                    p2.addAttributes( [QgsField("ID2", QVariant.Int)] )
                    v2.commitChanges()
                    feat2 = QgsFeature()
                    fit2 = provider2.getFeatures()
                    for j in range(len(trires)):
                        v2.startEditing()
                        fet = QgsFeature()
                        fet.setGeometry(  QgsGeometry.fromPoint(geompt[trires[j]-1]) )
                        fet.setAttributes( [ int(trires[j]), int(j + 1) ] )
                        p2.addFeatures( [ fet ] )
                        v2.commitChanges()
                    QgsMapLayerRegistry.instance().addMapLayer(v2)
        QMessageBox.information(None, " Message : ", "End")

  def calcul3fdraw(self):
        global Gdraw
        global positi
        global tabledraw
        arc_start=self.dlg3.ui.comboBox.currentText()
        arc_end=self.dlg3.ui.comboBox_2.currentText()
        oriente=self.dlg3.ui.comboBox_3.currentText()
        poids=self.dlg3.ui.comboBox_4.currentText()
        ponderation=self.dlg3.ui.comboBox_5.currentText()
        indicateur=self.dlg3.ui.comboBox_6.currentText()
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        table=[]
        tabledraw=[]
        if str(poids)=="No":
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          table=table+[(attrsstart,attrsend)] 
          tabledraw=tabledraw+[(attrsstart,attrsend)] 
         Gdraw=nx.Graph()
         if str(oriente)=="Yes" :
          Gdraw=nx.DiGraph()
         Gdraw.add_edges_from(table)
        if str(poids)=="Yes":
         distind=provider.fieldNameIndex(str(ponderation))
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind,distind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          attrsdist=feat.attributes()[distind]
          table=table+[(attrsstart,attrsend,attrsdist)] 
         Gdraw=nx.Graph()
         if str(oriente)=="Yes" :
          Gdraw=nx.DiGraph()
         Gdraw.add_weighted_edges_from(table)
        t=nx.number_of_nodes(Gdraw)
        self.dlg4 = testMatplot2(self.iface.mainWindow())
        ax = self.dlg4.ui.figure.add_subplot(111)
        if str(indicateur) == "Fruchterman-Reingold force-directed algorithm":
            positi = nx.spring_layout(Gdraw)
            ax.plot(nx.draw(Gdraw,pos = positi,node_size=200))
        if str(indicateur) == "Spectral":
            positi = nx.spectral_layout(Gdraw)
            ax.plot(nx.draw(Gdraw,pos = positi,node_size=200))
        if str(indicateur) == "Circular":
            positi = nx.circular_layout(Gdraw)
            ax.plot(nx.draw(Gdraw,pos = positi,node_size=200))
        if str(indicateur) == "Force Atlas":
            positi = fca.forceatlas2_layout(Gdraw, linlog=False, nohubs=False, iterations=100)
            ax.plot(nx.draw(Gdraw,pos = positi,node_size=200))
        self.dlg4.ui.canvas.draw()
        QObject.connect(self.dlg4.ui.bouton1, SIGNAL("clicked()"), self.changedraw)
        QObject.connect(self.dlg4.ui.bouton2, SIGNAL("clicked()"), self.changedrawcolor)
        self.dlg4.ui.comboBox.addItems(["Fruchterman-Reingold force-directed algorithm","Spectral", "Circular", "Force Atlas"])
        self.dlg4.show()

  def changedrawcolor(self):
        fields3 = [" "] + fields2
        fields4 = [" "] + fields
        fields5 = [" ","Default ID"] + fields2
        self.dlg5 = testDialogtooldraw(self.iface.mainWindow())
        self.dlg5.ui.lineedit.setStyleSheet("background-color: #ff0000")
        self.dlg5.ui.lineedit.setEnabled(False)
        self.dlg5.ui.combobox1b.addItems(["No","Yes"])
        self.dlg5.ui.combobox1c.addItems(fields3)
        self.dlg5.ui.combobox1d.addItems(["","Blue","Red","Green", "Orange", "Grey", "Purple"])
        self.dlg5.ui.lineedit2.setText("200")
        self.dlg5.ui.combobox2b.addItems(["No","Yes"])
        self.dlg5.ui.combobox2c.addItems(fields3)
        self.dlg5.ui.lineedit3.setStyleSheet("background-color: #000000")
        self.dlg5.ui.lineedit3.setEnabled(False)
        self.dlg5.ui.combobox3b.addItems(["No","Yes"])
        self.dlg5.ui.combobox3c.addItems(fields4)
        self.dlg5.ui.combobox3d.addItems(["","Blue","Red","Green", "Grey", "Purple", "RdYlBu", "RdYlGn"])
        self.dlg5.ui.lineedit4.setText("1")
        self.dlg5.ui.combobox4b.addItems(["No","Yes"])
        self.dlg5.ui.combobox4c.addItems(fields4)
        self.dlg5.ui.combobox5.addItems(["No","Yes"])
        self.dlg5.ui.combobox5b.addItems(fields5)
        self.dlg5.ui.lineedit5c.setText("12")
        QObject.connect(self.dlg5.ui.bouton1, SIGNAL("clicked()"), self.colorpicker1)
        QObject.connect(self.dlg5.ui.bouton3, SIGNAL("clicked()"), self.colorpicker2)
        QObject.connect(self.dlg5.ui.buttonBox, SIGNAL("accepted()"), self.editdraw)
        self.dlg5.show()

  def colorpicker1(self):
        color = QColorDialog.getColor()
        self.dlg5.ui.lineedit.setStyleSheet("QWidget { background-color: %s}" % color.name())

  def colorpicker2(self):
        color = QColorDialog.getColor()
        self.dlg5.ui.lineedit3.setStyleSheet("QWidget { background-color: %s}" % color.name())

  def changedraw(self) :
        global positi
        indicateur = self.dlg4.ui.comboBox.currentText()
        self.dlg4.ui.figure.clear()
        ax = self.dlg4.ui.figure.add_subplot(111)
        if str(indicateur) == "Fruchterman-Reingold force-directed algorithm":
            positi = nx.spring_layout(Gdraw)
            ax.plot(nx.draw(Gdraw,pos = positi,node_size= 200))
        if str(indicateur) == "Spectral":
            positi = nx.spectral_layout(Gdraw)
            ax.plot(nx.draw(Gdraw,pos = positi,node_size= 200))
        if str(indicateur) == "Circular":
            positi = nx.circular_layout(Gdraw)
            ax.plot(nx.draw(Gdraw,pos = positi,node_size= 200))
        if str(indicateur) == "Force Atlas":
            positi = fca.forceatlas2_layout(Gdraw, linlog=False, nohubs=False, iterations=100)
            ax.plot(nx.draw(Gdraw,pos = positi,node_size=200))
        self.dlg4.ui.canvas.draw()
        self.dlg4.show()

  def editdraw(self) :
        couleur = str(self.dlg5.ui.lineedit.styleSheet())
        couleur2 = string.split(couleur,": ")
        couleur3 = string.split(couleur2[1],"}")
        couleurnew = str(couleur3[0])
        couleura = str(self.dlg5.ui.lineedit3.styleSheet())
        couleura2 = string.split(couleura,": ")
        couleura3 = string.split(couleura2[1],"}")
        couleurnewa = str(couleura3[0])
        taille = float(self.dlg5.ui.lineedit2.text())
        taille_edge = float(self.dlg5.ui.lineedit4.text())
        taille_lab = float(self.dlg5.ui.lineedit5c.text())
        comaps = None
        comaps_edge = None
        wlab = None
        wlab2 = None
        test1 = str(self.dlg5.ui.combobox1b.currentText())
        if test1 == "Yes":
            champ = self.dlg5.ui.combobox1c.currentText()
            champind = provider2.fieldNameIndex(str(champ))
            feat = QgsFeature()
            tablech = []
            fit1 = provider2.getFeatures()
            while fit1.nextFeature(feat):
                attr = feat.attributes()[champind]
                tablech = tablech + [attr]
            taille3 = np.array(tablech)
            m = max(taille3)
            taille4 = 200 * taille3 / float(m)
            couleurnew = np.floor(taille4)
            test1b = str(self.dlg5.ui.combobox1d.currentText())
            if test1b == "Blue" :
                comaps = plt.cm.Blues
            if test1b == "Red" :
                comaps = plt.cm.Reds
            if test1b == "Green" :
                comaps = plt.cm.Greens
            if test1b == "Orange" :
                comaps = plt.cm.Oranges
            if test1b == "Grey" :
                comaps = plt.cm.Greys
            if test1b == "Purple" :
                comaps = plt.cm.Purples			
        test2 = str(self.dlg5.ui.combobox2b.currentText())
        if test2 == "Yes":
            taille2 = taille
            champ = self.dlg5.ui.combobox2c.currentText()
            champind = provider2.fieldNameIndex(str(champ))
            feat = QgsFeature()
            tablech = []
            fit1 = provider2.getFeatures()
            while fit1.nextFeature(feat):
                attr = feat.attributes()[champind]
                tablech = tablech + [attr]
            taille3 = np.array(tablech)
            m = max(taille3)
            taille4 = taille2 * taille3 / float(m)
            taille = np.floor(taille4)
        test3 = str(self.dlg5.ui.combobox3b.currentText())
        if test3 == "Yes":
            champ = self.dlg5.ui.combobox3c.currentText()
            champind = provider.fieldNameIndex(str(champ))
            feat = QgsFeature()
            tablech = []
            fit1 = provider.getFeatures()
            while fit1.nextFeature(feat):
                attr = feat.attributes()[champind]
                tablech = tablech + [attr]
            taille3 = np.array(tablech)
            m = max(taille3)
            taille4 = 200 * taille3 / float(m)
            taille_edgepro = np.floor(taille4)
            edg = Gdraw.edges()
            taille_edgepro2 = []
            for i in range(len(edg)):
                try : 
                    a = tabledraw.index((edg[i][0],edg[i][1]))  
                except :
                    a = tabledraw.index((edg[i][1],edg[i][0]))
                taille_edgepro2 = taille_edgepro2 + [taille_edgepro[a]]
            couleurnewa = np.array(taille_edgepro2)
            test1b = str(self.dlg5.ui.combobox3d.currentText())
            if test1b == "Blue" :
                comaps_edge = plt.cm.Blues
            if test1b == "Red" :
                comaps_edge = plt.cm.Reds
            if test1b == "Green" :
                comaps_edge = plt.cm.Greens
            if test1b == "Grey" :
                comaps_edge = plt.cm.Greys
            if test1b == "Purple" :
                comaps_edge = plt.cm.Purples
            if test1b == "RdYlBu" :
                comaps_edge = plt.cm.RdYlBu
            if test1b == "RdYlGn" :
                comaps_edge = plt.cm.RdYlGn
        test4 = str(self.dlg5.ui.combobox4b.currentText())
        if test4 == "Yes":
            taille2 = taille_edge
            champ = self.dlg5.ui.combobox4c.currentText()
            champind = provider.fieldNameIndex(str(champ))
            feat = QgsFeature()
            tablech = []
            fit1 = provider.getFeatures()
            while fit1.nextFeature(feat):
                attr = feat.attributes()[champind]
                tablech = tablech + [attr]
            taille3 = np.array(tablech)
            m = max(taille3)
            taille4 = taille2 * taille3 / float(m)
            taille_edgepro = np.floor(taille4)
            edg = Gdraw.edges()
            taille_edgepro2 = []
            for i in range(len(edg)):
                try : 
                    a = tabledraw.index((edg[i][0],edg[i][1]))  
                except :
                    a = tabledraw.index((edg[i][1],edg[i][0]))
                taille_edgepro2 = taille_edgepro2 + [taille_edgepro[a]]
            taille_edge = np.array(taille_edgepro2)
        test5 = str(self.dlg5.ui.combobox5.currentText())
        if test5 == "Yes":
            wlab = True
            champ = self.dlg5.ui.combobox5b.currentText()
            wlab2 = {}
            if champ != "Default ID" :
                champind = provider2.fieldNameIndex(str(champ))
                feat = QgsFeature()
                fit1 = provider2.getFeatures()
                j = 1
                while fit1.nextFeature(feat):
                    attr = feat.attributes()[champind]
                    wlab2[j]=str(attr)
                    j = j + 1
            if champ == "Default ID" :
                for j in range(len(Gdraw.nodes())) :
                    wlab2[j+1]=str(j+1)
        self.dlg4.ui.figure.clear()
        ax = self.dlg4.ui.figure.add_subplot(111)
        ax.plot(nx.draw(Gdraw,pos = positi,node_size = taille, node_color = couleurnew, cmap=comaps, edge_color = couleurnewa, width = taille_edge, edge_cmap = comaps_edge, with_labels = wlab, labels = wlab2, font_size = taille_lab ))
        self.dlg4.ui.canvas.draw()
        self.dlg4.show()
  
  def calcul3fpgb(self):
        epsg=canvas.mapRenderer().destinationCrs().authid()
        arc_start=self.dlg3.ui.comboBox.currentText()
        arc_end=self.dlg3.ui.comboBox2.currentText()
        if str(pg) == "Simplify Planar Graph" : 
            nb = 2
        if str(pg) == "Remove Leaves" : 
            nb = 1
        if str(pg) == "Remove Zero Degree Nodes" :
            nb = 0
        champ1=provider2.fieldNameIndex(str(arc_start))
        champ2=provider2.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        fit = provider.getFeatures()
        v = QgsVectorLayer("Point?crs=epsg:"+str(epsg), "Nodes", "memory")
        p = v.dataProvider()
        p.addAttributes( [QgsField("ID", QVariant.Int)] )
        p.addAttributes( [QgsField("ID2", QVariant.Int)] )
        v.commitChanges()
        i = 1
        i2 = 0
        valconfig=0
        tablept=[]
        if nb == 2:
            ptsup = []
        while fit.nextFeature(feat):
            cands = eLayer.getFeatures(QgsFeatureRequest().setFilterRect(feat.geometry().boundingBox()))
            c = 0
            for line_feature in cands:
                if feat.geometry().intersects(line_feature.geometry()):
                    c = c + 1
            if c != nb:
                i2 = i2 + 1
                v.startEditing()
                fet = QgsFeature()
                fet.setGeometry(  feat.geometry() )
                fet.setAttributes( [ int(i), int(i2) ] )
                p.addFeatures( [ fet ] )
                v.commitChanges()
                tablept = tablept + [i]
            if c==2 :
                if nb==2 :
                    ptsup = ptsup + [i]
            i = i + 1
        QgsMapLayerRegistry.instance().addMapLayer(v)
        feat = QgsFeature()
        fit = provider2.getFeatures()
        v2 = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges", "memory")
        p2 = v2.dataProvider()
        p2.addAttributes( [QgsField("StartNode", QVariant.Int)] )
        p2.addAttributes( [QgsField("EndNode", QVariant.Int)] )
        p2.addAttributes( [QgsField("StartNode2", QVariant.Int)] )
        p2.addAttributes( [QgsField("EndNode2", QVariant.Int)] )
        v2.commitChanges()
        i = 1
        i2 = 0
        tableconfig=[]
        while fit.nextFeature(feat):
            test = 0 
            start= int(feat.attributes()[champ1])
            for sid in enumerate(tablept):
                if sid[1] == start:
                    end = int(feat.attributes()[champ2])
                    for fid in enumerate(tablept) :
                        if fid[1] == end :
                            v2.startEditing()
                            fet = QgsFeature()
                            fet.setGeometry(  feat.geometry() )
                            fet.setAttributes( [ start, end, int(sid[0]+1) , int(fid[0]+1) ] )
                            p2.addFeatures( [ fet ] )
                            v2.commitChanges()
                            test = 1
            if test == 0 :
                tableconfig = tableconfig + [[str(feat.geometry().exportToWkt()),int(feat.attributes()[champ1]),int(feat.attributes()[champ2]),valconfig]]
                valconfig = valconfig + 1
        if nb == 2 :
            newrac = []
            for eltsup in (ptsup):
                geom2ligne=[]
                idarc=[]
                for i in range(len(tableconfig)):
                    if int(tableconfig[i][1]) == eltsup :
                        geom =tableconfig[i][0]
                        geom2 = string.split(geom,'(')
                        geom3 = string.split(geom2[1],')')
                        try :
                            idarc.index(tableconfig[i][3])
                            test = 1
                        except :
                            test = 0
                        if test == 0:
                            geom2ligne = geom2ligne + [[1, geom3[0], int(tableconfig[i][2]),tableconfig[i][3]]]
                            idarc = idarc + [tableconfig[i][3]]
                    if int(tableconfig[i][2]) == eltsup :
                        geom =tableconfig[i][0]
                        geom2 = string.split(geom,'(')
                        geom3 = string.split(geom2[1],')')
                        try :
                            idarc.index(tableconfig[i][3])
                            test = 1
                        except :
                            test = 0
                        if test == 0:
                            geom2ligne = geom2ligne + [[2, geom3[0], int(tableconfig[i][1]),tableconfig[i][3]]]
                            idarc = idarc + [tableconfig[i][3]]
                if geom2ligne[0][0] == 1:
                    if geom2ligne[1][0] == 2:
                        geomdef = 'LineString('+geom2ligne[1][1]+','+geom2ligne[0][1]+')'
                        id1 = geom2ligne[1][2]
                        id2 = geom2ligne[0][2]
                    if geom2ligne[1][0] == 1:
                        newgeom = ''
                        geom4 = string.split(geom2ligne[1][1],',')
                        for i in range(len(geom4)):
                            if i != 0 :
                                newgeom=newgeom+','+str(geom4[len(geom4)-i-1])
                            if i == 0 :
                                newgeom = str(geom4[len(geom4)-i-1])
                        geomdef = 'LineString('+newgeom+','+geom2ligne[0][1]+')'
                        id1 = geom2ligne[1][2]
                        id2 = geom2ligne[0][2]
                if geom2ligne[0][0] == 2:
                    if geom2ligne[1][0] == 1:
                        geomdef = 'LineString('+geom2ligne[0][1]+','+geom2ligne[1][1]+')'
                        id1 = geom2ligne[0][2]
                        id2 = geom2ligne[1][2]
                    if geom2ligne[1][0] == 2:
                        newgeom = ''
                        geom4 = string.split(geom2ligne[1][1],',')
                        for i in range(len(geom4)):
                            if i != 0 :
                                newgeom=newgeom+','+str(geom4[len(geom4)-i-1])
                            if i == 0 :
                                 newgeom = str(geom4[len(geom4)-i-1])
                        geomdef = 'LineString('+geom2ligne[0][1]+','+newgeom+')'
                        id1 = geom2ligne[0][2]
                        id2 = geom2ligne[1][2]
                tableconfig[idarc[0]][0] = geomdef[:]
                tableconfig[idarc[0]][1] = id1
                tableconfig[idarc[0]][2] = id2
                tableconfig[idarc[0]][3] = idarc[0]
                tableconfig[idarc[1]][0] = geomdef[:]
                tableconfig[idarc[1]][1] = id1
                tableconfig[idarc[1]][2] = id2
                tableconfig[idarc[1]][3] = idarc[0]
                try :
                    a1 = int(tablept.index(id1)) + 1
                    testdef = 0
                except :
                    testdef = 1
                if testdef == 0 :
                    try :
                        a2 = tablept.index(id2) + 1
                        testdef = 0
                    except:
                        testdef = 1
                if testdef == 0 :
                    v2.startEditing()
                    fet = QgsFeature()
                    fet.setGeometry(  QgsGeometry.fromWkt( geomdef[:] ) )
                    fet.setAttributes( [ id1, id2, int(a1) , int(a2) ] )
                    p2.addFeatures( [ fet ] )
                    v2.commitChanges()             
        QgsMapLayerRegistry.instance().addMapLayer(v2)
        QMessageBox.information(None, " Message : ", "End")

  def calcul3fid(self):
        arc_start=self.dlg3.ui.comboBox2.currentText()
        arc_end=self.dlg3.ui.comboBox3.currentText()
        ID = self.dlg3.ui.comboBox.currentText()
        Idind=provider2.fieldNameIndex(str(ID))
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        nbcol=int(provider2.fields().count())
        provider2.addAttributes( [QgsField("AnNet", QVariant.Int)] )
        nLayer.commitChanges()
        feat = QgsFeature()
        fit1 = provider2.getFeatures()
        olderID = []
        i=0
        nLayer.startEditing()
        while fit1.nextFeature(feat):
            olderID = olderID + [feat.attributes()[Idind]]
            nLayer.changeAttributeValue(i,nbcol, int(i+1))
            i = i + 1
        nLayer.commitChanges()
        nbcol=int(provider.fields().count())
        provider.addAttributes( [QgsField("AnNet", QVariant.Int)] )
        provider.addAttributes( [QgsField("StartNode", QVariant.Int)] )
        provider.addAttributes( [QgsField("EndNode", QVariant.Int)] )
        aLayer.commitChanges()
        feat2 = QgsFeature()
        fit2 = provider.getFeatures()
        i=0
        aLayer.startEditing()
        while fit2.nextFeature(feat2):
            dep = int(olderID.index(feat2.attributes()[startind]))+1
            fin = int(olderID.index(feat2.attributes()[endind]))+1
            aLayer.changeAttributeValue(i,nbcol, int(i+1))
            aLayer.changeAttributeValue(i,nbcol+1, dep)
            aLayer.changeAttributeValue(i,nbcol+2, fin)
            i = i + 1
        aLayer.commitChanges()
        QMessageBox.information(None, " Message : ", "End")

  def calcul3fdin(self):
        epsg=canvas.mapRenderer().destinationCrs().authid()
        arc_start=self.dlg3.ui.comboBox2.currentText()
        arc_end=self.dlg3.ui.comboBox3.currentText()
        ID = self.dlg3.ui.comboBox.currentText()
        Idind=provider2.fieldNameIndex(str(ID))
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        table=[]
        table_arc=[]
        geom_arc=[]
        fit1 = provider.getFeatures()
        while fit1.nextFeature(feat):
            attrsstart=feat.attributes()[startind]
            attrsend=feat.attributes()[endind]
            table=table+[(attrsstart,attrsend)]
            attrs=feat.attributes()
            table_arc=table_arc+[attrs]
            geom_arc=geom_arc+[feat.geometry().exportToWkt()]
        feat2 = QgsFeature()
        table2 = []
        table_noeud = []
        geom_noeud = []
        fit2 = provider2.getFeatures()
        while fit2.nextFeature(feat2):
            attrsid=feat2.attributes()[Idind]
            table2=table2+[attrsid]
            attrs = feat2.attributes()
            table_noeud = table_noeud + [attrs]
            geom_noeud = geom_noeud + [feat2.geometry().exportToWkt()]
        tablenew = []
        vl = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges", "memory")
        pr = vl.dataProvider()
        for j in range(field.count()):
            pr.addAttributes( [field[j]] )
        vl.startEditing()
        for i in range(len(table)):
            test = 0
            try :
                table2.index(table[i][0])
                table2.index(table[i][1])
            except :
                test = 1
            if test == 0 :
                tablenew = tablenew + [(table[i][0],table[i][1])]
                fet = QgsFeature()
                fet.setGeometry(  QgsGeometry.fromWkt( geom_arc[i] ) )
                fet.setAttributes( table_arc[i] )
                pr.addFeatures( [ fet ] )
        vl.commitChanges()
        G=nx.Graph()
        G.add_edges_from(tablenew)
        nod = G.nodes()
        vl2 = QgsVectorLayer("Point?crs=epsg:"+str(epsg), "Nodes", "memory")
        pr2 = vl2.dataProvider()
        for j in range(field2.count()):
            pr2.addAttributes( [field2[j]] )
        vl2.startEditing()
        for i in range(len(nod)):
            id = nod[i]
            num = table2.index(id)
            fet = QgsFeature()
            fet.setGeometry(  QgsGeometry.fromWkt( geom_noeud[num] ) )
            fet.setAttributes( table_noeud[num] )
            pr2.addFeatures( [ fet ] )
        vl2.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl)
        QgsMapLayerRegistry.instance().addMapLayer(vl2)
        QMessageBox.information(None, " Message : ", "End")

  def calcul3fgs(self):
        epsg=canvas.mapRenderer().destinationCrs().authid()
        arc_start=self.dlg3.ui.comboBox.currentText()
        arc_end=self.dlg3.ui.comboBox_2.currentText()
        oriente=self.dlg3.ui.comboBox_3.currentText()
        valpart=self.dlg3.ui.comboBox_4.currentText()
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        valpartind=provider2.fieldNameIndex(str(valpart))
        feat = QgsFeature()
        table=[]
        table_arc=[]
        geom_arc=[]
        fit1 = provider.getFeatures()
        while fit1.nextFeature(feat):
            attrsstart=feat.attributes()[startind]
            attrsend=feat.attributes()[endind]
            table=table+[(attrsstart,attrsend)]
            attrs=feat.attributes()
            table_arc=table_arc+[attrs]
            geom_arc=geom_arc+[feat.geometry().exportToWkt()]
        G=nx.Graph()
        G2=nx.Graph()
        if str(oriente)=="Yes" :
          G=nx.DiGraph()
          G2=nx.DiGraph()
        G.add_edges_from(table)
        G2.add_edges_from(table)
        feat2 = QgsFeature()
        valclass = []
        noeudpart = []
        table_noeud = []
        geom_noeud = []
        fit2 = provider2.getFeatures()
        i = 1
        while fit2.nextFeature(feat2):
            attr=feat2.attributes()[valpartind]
            try :
                valind = valclass.index(attr)
                noeudpart[valind] = noeudpart[valind] + [i]  
            except :
                noeudpart = noeudpart + [[i]]
                valclass = valclass + [attr]			
            i = i + 1
            attrs = feat2.attributes()
            table_noeud = table_noeud + [attrs]
            geom_noeud = geom_noeud + [feat2.geometry().exportToWkt()]
        for i in range(len(valclass)):
            nom = "Edges_SG_"+str(i+1)
            vl = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), nom, "memory")
            pr = vl.dataProvider()
            for j in range(field.count()):
                pr.addAttributes( [field[j]] )
            H = G.subgraph(noeudpart[i])
            harcs = H.edges()
            vl.startEditing()
            for j in range(len(harcs)):
                dep = harcs[j][0]
                arr = harcs[j][1]
                try : 
                    vid = table.index((dep,arr))	
                    fet = QgsFeature()
                    fet.setGeometry(  QgsGeometry.fromWkt( geom_arc[vid] ) )
                    fet.setAttributes( table_arc[vid] )
                    pr.addFeatures( [ fet ] )
                except :
                    vid = table.index((arr,dep))	
                    fet = QgsFeature()
                    fet.setGeometry(  QgsGeometry.fromWkt( geom_arc[vid] ) )
                    fet.setAttributes( table_arc[vid] )
                    pr.addFeatures( [ fet ] )
                try :
                    G2.remove_edge(dep,arr)
                except :
                    G2.remove_edge(arr,dep)
            vl.commitChanges()
            nom2 = "Nodes_SG_"+str(i+1)
            vl2 = QgsVectorLayer("Point?crs=epsg:"+str(epsg), nom2, "memory")
            pr2 = vl2.dataProvider()
            for j in range(field2.count()):
                pr2.addAttributes( [field2[j]] )
            vl2.startEditing()
            for j in range(len(noeudpart[i])):
                vid = noeudpart[i][j] - 1
                fet = QgsFeature()
                fet.setGeometry(  QgsGeometry.fromWkt( geom_noeud[vid] ) )
                fet.setAttributes( table_noeud[vid] )
                pr2.addFeatures( [ fet ] )
            vl2.commitChanges()    
            QgsMapLayerRegistry.instance().addMapLayer(vl)
            QgsMapLayerRegistry.instance().addMapLayer(vl2)
        edge_sup = G2.edges()
        node_sup = G2.nodes()
        deg = G2.degree()
        vl = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges_sup", "memory")
        pr = vl.dataProvider()
        for j in range(field.count()):
            pr.addAttributes( [field[j]] )
        vl.startEditing()
        for i in range(len(edge_sup)):
            dep = edge_sup[i][0]
            arr = edge_sup[i][1]
            try : 
                vid = table.index((dep,arr))	
                fet = QgsFeature()
                fet.setGeometry(  QgsGeometry.fromWkt( geom_arc[vid] ) )
                fet.setAttributes( table_arc[vid] )
                pr.addFeatures( [ fet ] )
            except :
                vid = table.index((arr,dep))	
                fet = QgsFeature()
                fet.setGeometry(  QgsGeometry.fromWkt( geom_arc[vid] ) )
                fet.setAttributes( table_arc[vid] )
                pr.addFeatures( [ fet ] )
        vl.commitChanges()
        vl2 = QgsVectorLayer("Point?crs=epsg:"+str(epsg), "Nodes_Edges_Sup", "memory")
        pr2 = vl2.dataProvider()
        for j in range(field2.count()):
            pr2.addAttributes( [field2[j]] )
        vl2.startEditing()
        for j in range(len(node_sup)):
            vid = node_sup[j] - 1
            if deg[node_sup[j]] > 0:
                fet = QgsFeature()
                fet.setGeometry(  QgsGeometry.fromWkt( geom_noeud[vid] ) )
                fet.setAttributes( table_noeud[vid] )
                pr2.addFeatures( [ fet ] )
        vl2.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl)
        QgsMapLayerRegistry.instance().addMapLayer(vl2)
        QMessageBox.information(None, " Message : ", "End")

  def calcul3ftoun(self):
        epsg=canvas.mapRenderer().destinationCrs().authid()
        arc_start=self.dlg4.ui.comboBox.currentText()
        arc_end=self.dlg4.ui.comboBox_2.currentText()
        oriente=self.dlg4.ui.comboBox_3.currentText()
        poids=self.dlg4.ui.comboBox_4.currentText()
        ponderation=self.dlg4.ui.comboBox_5.currentText()
        startind=provider.fieldNameIndex(str(arc_start))
        endind=provider.fieldNameIndex(str(arc_end))
        feat = QgsFeature()
        table = []
        geom = []
        if str(poids)=="No":
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          table=table+[(attrsstart,attrsend)] 
          geom = geom + [feat.geometry().exportToWkt()]
         G=nx.Graph()
         if str(oriente)=="Yes" :
          G=nx.DiGraph()
         G.add_edges_from(table)
        if str(poids)=="Yes":
         table2 = []
         distind=provider.fieldNameIndex(str(ponderation))
         fit1 = provider.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([startind,endind,distind]) )
         while fit1.nextFeature(feat):
          attrsstart=feat.attributes()[startind]
          attrsend=feat.attributes()[endind]
          attrsdist=feat.attributes()[distind]
          table=table+[(attrsstart,attrsend)] 
          table2=table2+[(attrsstart,attrsend,attrsdist)] 
          geom = geom + [feat.geometry().exportToWkt()]
         G=nx.Graph()
         if str(oriente)=="Yes" :
          G=nx.DiGraph()
         G.add_weighted_edges_from(table2)
        test = 0
        if str(oriente) == "No" :
            test = 1
            QMessageBox.information(None, " Message : ", "Graph needs to be directed")
        if str(oriente) == "Yes" :
            testzero,ok1 = QInputDialog.getItem(None,"Model","Delete unique edges ? : ", ["Yes","No"], editable = False)
            if ok1 :
                if testzero == "No" :
                    vln = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges_undirected", "memory")
                    pr = vln.dataProvider()
                    vln.startEditing()
                    pr.addAttributes( [QgsField("AnNet", QVariant.Int), QgsField("StartNode", QVariant.Int), QgsField("EndNode", QVariant.Int)] )
                    vln.commitChanges()
                    if str(poids) == "Yes" :
                        vln.startEditing()
                        pr.addAttributes( [QgsField("Weight", QVariant.Double)] )
                        vln.commitChanges()
                    UG = G.to_undirected()
                    edg = UG.edges()
                    for i in range(len(edg)):
                        if str(poids) == "Yes" :
                            try :
                                val1 = G[edg[i][0]][edg[i][1]]['weight']
                            except :
                                val1 = 0
                            try :
                                val2 = G[edg[i][1]][edg[i][0]]['weight']
                            except :
                                val2 = 0
                            val = val1 + val2
                            vid = [i+1, edg[i][0], edg[i][1], val]
                        if str(poids) == "No" :
                            vid = [i+1, edg[i][0], edg[i][0]]
                        try :
                            ind = table.index((edg[i][0],edg[i][1]))
                        except :
                            ind = table.index((edg[i][1],edg[i][0]))
                            vid[1] = edg[i][1]
                            vid[2] = edg[i][0]
                        geo = geom[ind]
                        fet = QgsFeature()
                        fet.setGeometry(  QgsGeometry.fromWkt( geo ) )
                        fet.setAttributes( vid )
                        pr.addFeatures( [ fet ] )
                    vln.commitChanges()
                    QgsMapLayerRegistry.instance().addMapLayer(vln)
                if testzero == "Yes" :
                    vln = QgsVectorLayer("LineString?crs=epsg:"+str(epsg), "Edges_undirected", "memory")
                    pr = vln.dataProvider()
                    vln.startEditing()
                    pr.addAttributes( [QgsField("AnNet", QVariant.Int), QgsField("StartNode", QVariant.Int), QgsField("EndNode", QVariant.Int)] )
                    if str(poids) == "Yes" :
                        vln.startEditing()
                        pr.addAttributes( [QgsField("Weight1", QVariant.Double)] )
                        pr.addAttributes( [QgsField("Weight2", QVariant.Double)] )
                        vln.commitChanges()
                    vln.commitChanges()
                    tablenew = table[:]
                    i = 1
                    vln.startEditing()
                    while len(tablenew) != 0 :
                        id1 = tablenew[0][0]
                        id2 = tablenew[0][1]
                        try :
                           ind2 = table.index((id2,id1))
                           tablenew.remove((id2,id1))
                           ind1 = table.index((id1,id2))
                           vid = [i,id1,id2]
                           if str(poids) == "Yes" :
                                vid = vid + [table2[ind1][2],table2[ind2][2]]
                           fet = QgsFeature()
                           fet.setGeometry( QgsGeometry.fromWkt( geom[ind1] ) )
                           fet.setAttributes( vid )
                           pr.addFeatures( [ fet ] )
                           i = i + 1
                        except :
                            "Do Nothing"
                        tablenew.remove((id1,id2))
                    vln.commitChanges()
                    QgsMapLayerRegistry.instance().addMapLayer(vln)
        QMessageBox.information(None, " Message : ", "End")

  def calcul3fet(self):
        street = self.dlg3.ui.comboBox.currentText()
        postalc = self.dlg3.ui.comboBox2.currentText()
        namel = self.dlg3.ui.comboBox3.currentText()
        countr = self.dlg3.ui.comboBox4.currentText()
        if str(street) != "":
            Idstreet = provider.fieldNameIndex(str(street))
        else :
            Idstreet = 99999999
        if str(postalc) != "":
            Idpostalc = provider.fieldNameIndex(str(postalc))
        else :
            Idpostalc = 99999999
        Idnamel = provider.fieldNameIndex(str(namel))
        if str(countr) != "":
            Idcountr = provider.fieldNameIndex(str(countr))
        else :
            Idcountr = 99999999
        streetb = self.dlg3.ui.comboBoxb.currentText()
        postalcb = self.dlg3.ui.comboBox2b.currentText()
        namelb = self.dlg3.ui.comboBox3b.currentText()
        countrb = self.dlg3.ui.comboBox4b.currentText()
        if str(streetb) != "":
            Idstreetb = provider.fieldNameIndex(str(streetb))
        else :
            Idstreetb = 99999999
        if str(postalcb) != "":
            Idpostalcb = provider.fieldNameIndex(str(postalcb))
        else :
            Idpostalcb = 99999999
        Idnamelb = provider.fieldNameIndex(str(namelb))
        if str(countrb) != "":
            Idcountrb = provider.fieldNameIndex(str(countrb))
        else :
            Idcountrb = 99999999
        attrs = []
        tabadrr = []
        tabligne = []
        feat = QgsFeature()
        fit1 = provider.getFeatures()
        i = 0
        while fit1.nextFeature(feat):
            attrs = attrs + [feat.attributes()]
            adrr = ""
            if Idstreet != 99999999 :
                adrr = adrr + str(feat.attributes()[Idstreet]) + ","
            adrr = adrr + str(feat.attributes()[Idnamel])
            if Idpostalc != 99999999 :
                adrr = adrr + "," + str(feat.attributes()[Idpostalc])
            if Idcountr != 99999999 :
                adrr = adrr + "," + str(feat.attributes()[Idcountr])
            try :
                id1 = tabadrr.index(adrr)
            except :
                tabadrr = tabadrr + [adrr]
                id1 = i
                i = i + 1
            adrr = ""
            if Idstreetb != 99999999 :
                adrr = adrr + str(feat.attributes()[Idstreetb]) + ","
            adrr = adrr + str(feat.attributes()[Idnamelb])
            if Idpostalcb != 99999999 :
                adrr = adrr + "," + str(feat.attributes()[Idpostalcb])
            if Idcountrb != 99999999 :
                adrr = adrr + "," + str(feat.attributes()[Idcountrb])
            try :
                id2 = tabadrr.index(adrr)
            except :
                tabadrr = tabadrr + [adrr]
                id2 = i
                i = i + 1
            tabligne = tabligne + [[id1,id2]]
        tabxy = []
        vln = QgsVectorLayer("Point?crs=epsg:4326", "Nodes", "memory")
        prn = vln.dataProvider()
        vln.startEditing()
        prn.addAttributes( [QgsField("AnNet", QVariant.Int), QgsField("Adress", QVariant.String)] )
        vln.commitChanges()
        for i in range(len(tabadrr)):
            req = "http://photon.komoot.de/api/?q="
            reqfin = str(req)+str(tabadrr[i])
            f2 = urllib.urlopen(reqfin)
            d2 = f2.read()
            lon = d2.split('coordinates":[')
            lon2 = lon[1].split(",")
            x = lon2[0]
            lat = lon2[1].split("]")
            y = lat[0]
            tabxy = tabxy + [[x,y]]
            fet = QgsFeature()
            fet.setGeometry( QgsGeometry.fromPoint(QgsPoint(float(x),float(y))) )
            fet.setAttributes( [ int(i + 1) , str(tabadrr[i]) ] )
            vln.startEditing()
            prn.addFeatures( [ fet ] )
            vln.commitChanges()
        vl = QgsVectorLayer("LineString?crs=epsg:4326", "Edges", "memory")
        pr = vl.dataProvider()
        vl.startEditing()
        for i in range(field.count()):
            pr.addAttributes( [field[i]] )
        pr.addAttributes( [QgsField("AnNet1", QVariant.Int), QgsField("AnNet2", QVariant.Int)] )
        vl.commitChanges()
        for i in range(len(attrs)):
            att = attrs[i] + [ int(tabligne[i][0] + 1),int(tabligne[i][1] + 1) ]
            fet = QgsFeature()
            fet.setGeometry( QgsGeometry.fromPolyline( [ QgsPoint(float(tabxy[int(tabligne[i][0])][0]), float(tabxy[int(tabligne[i][0])][1])) , QgsPoint(float(tabxy[int(tabligne[i][1])][0]),float(tabxy[int(tabligne[i][1])][1])) ] ))
            fet.setAttributes( att )
            vl.startEditing()
            pr.addFeatures( [ fet ] )
            vl.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vln)
        QgsMapLayerRegistry.instance().addMapLayer(vl)
        QMessageBox.information(None, " Message : ", "Thanks To Photon and OpenStreetMap")
