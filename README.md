# Network\_Analysis

This plugin provides an intuitive workflow (a user friendly tool) for network analysis within QGIS. It aims to fill the gap in GIS software for tools dedicated to the structural analysis of spatial networks. The extension is powered by the NetworkX library.

## Introduction

Find the appropriate version of the plugin below. Each folder corresponds to a specific release:

<ul>
<li><b>QGIS 4.x (and latest 3.x builds):</b> Use <a href="https://sergelhomme.fr/data/network_analysis_3_1.zip"  title="Analyse de graphe" >Network_Analysis_3_1</a></li>

<li><b>QGIS 3.x:</b> Use <a href="https://sergelhomme.fr/data/network_analysis_2_2.zip"  title="Analyse de graphe" >Network_Analysis_2_2</a>
</ul></li>

Other folders contain older versions for backward compatibility.

## Installation

Download the ZIP archive. In QGIS, go to the Plugins menu. Select Manage and Install Plugins... Click on the Install from ZIP tab. Browse and select the ZIP file. Click Install Plugin.

## Getting Started

To perform the calculations, you will need two spatial layers: a nodes layer and an edges (arcs) layer. Regardless of the algorithm selected, the initial dialog box will prompt you to select both the node and edge layers from your project.

<ul>
<li><b>Nodes layer:</b> Must include a unique identifier field. It is strongly recommended to use numeric IDs (from 1 to n). </li>

<li><b>Edges layer:</b> Must contain its own unique ID field. Additionally, this layer must include two specific fields referencing the IDs of the start and end nodes for each edge.</li>
</ul>

You can download a sample dataset here.

## Illustrations

![An illustration of two basic indicators](https://github.com/sergelhomme/Network_Analysis/blob/master/Images/basic_analysis2.png)

<p align="center"> An illustration of two basic indicators with Network_Analysis : Degree and Betweenness </p>

![Scale Free analysis](https://github.com/sergelhomme/Network_Analysis/blob/master/Images/statistics4.png)

<p align="center"> Scale Free analysis with Network_Analysis </p>

![Drawing Algo](https://github.com/sergelhomme/Network_Analysis/blob/master/Images/Drawing.png)

<p align="center"> Drawing Algo with Network_Analysis </p>

![Community Detection](https://github.com/sergelhomme/Network_Analysis/blob/master/Images/Community.png)

<p align="center"> Community detection (Louvain) with Network_Analysis </p>
