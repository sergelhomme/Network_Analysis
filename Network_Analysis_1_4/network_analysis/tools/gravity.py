import networkx as nx
import numpy as np

def calculmod(p,gdep,gap,a,b,ori):
    tot = 0
    subg = 0
    for i in range(len(p)):
        if len(p[i]) > 1 :
            subg = gdep.subgraph(p[i])
            if str(ori) == "Yes" :
                UG=subg.to_undirected()
                contest = nx.is_connected(UG)
            if str(ori) == "No" :
                contest = nx.is_connected(subg)
            if contest == True :
                edg = subg.edges()
                tot1 = 0
                tot2 = 0
                for j in range(len(edg)):
                    try :
                        tot1 = tot1 + gdep[edg[j][0]][edg[j][1]]['weight']
                    except :
                        tot1 = tot1 + gdep[edg[j][0]][edg[j][1]]['weight']
                    try :
                        tot2 = tot2 + gap[edg[j][0]][edg[j][1]]['weight']
                    except :
                        tot2 = tot2 + gap[edg[j][0]][edg[j][1]]['weight']
                ecart = (tot1 / float(a)) - (tot2 / float(b))
                tot = tot + ecart
    return tot

def com_spa(Gr,Gapprox,orie,isol): 
    noeuds = Gr.nodes()
    sum1 = sum(nx.degree(Gr,weight='weight').values())/float(2)
    sum2 = sum(nx.degree(Gapprox,weight='weight').values())/float(2)
    part = []
    for i in range(len(noeuds)) :
        part = part + [[noeuds[i]]]
    mod = 0
    test = 0
    while test == 0 :
        print(len(part))
        test = 1
        partnew = part[:]
        j = 0
        while j < ( len(partnew) - 1 ) :
            print(j)
            maxmod = mod
            for k in range(len(part) - j - 1) : 
                partnew = part[:]
                part1 = part[j]
                part2 = part[k+j+1]
                parttest = part1 + part2
                partnew[j] = parttest
                del partnew[k+j+1]
                val = calculmod(partnew,Gr,Gapprox,sum1,sum2,orie)
                if val > maxmod  :
                    test = 0
                    maxmod = val
                    maxpart = partnew[:]
                    sousg = parttest
                    ligne = k+j+1
            if maxmod > mod :
                mod = maxmod
                part = maxpart[:]
            j = j +1
    if isol == "Yes" :
        npart = [0] * len(Gr.nodes())
        for i in range(len(part)):
            for j in range(len(part[i])):
                npart[part[i][j]-1] = i
        for i in range(len(part)):
            if len(part[i]) == 1 :
                nei = Gr.neighbors(int(part[i][0]))
                if len(nei) == 1 :
                    com = npart[nei[0]-1]
                    part[com] = part[com] + [part[i][0]]
                if len(nei) == 0 :
                    UG = Gr.to_undirected()
                    nei2 = UG.neighbors(int(part[i][0]))
                    if len(nei2) == 1 :
                        com = npart[nei2[0]-1]
                        part[com] = part[com] + [part[i][0]]
                if len(nei) > 1 :
                    print(part[i])
        n2 = len(part)		   
        for i in range(len(part)):
            if len(part[n2-i-1]) == 1 :
                nei = Gr.neighbors(int(part[n2-i-1][0]))
                if len(nei) == 1 :
                    del part[n2-i-1]
                if len(nei) == 0 :
                    UG = Gr.to_undirected()
                    nei2 = UG.neighbors(int(part[n2-i-1][0]))
                    if len(nei2) == 1 :
                        del part[n2-i-1]
        if str(orie) == "Yes":
            GUN = Gr.to_undirected()
        for i in range(len(part)):
            if len(part[i]) == 1 :
                edg = Gr.edges(int(part[i][0]))
                if str(orie) == "Yes":
                    edg = GUN.edges(int(part[i][0]))		
                valmax = 0
                for j in range(len(edg)):
                    try :
                        val1 = Gr[edg[j][0]][edg[j][1]]['weight']
                    except :
                        val1 = Gr[edg[j][1]][edg[j][0]]['weight']
                    try :
                        val2 = Gapprox[edg[j][0]][edg[j][1]]['weight']
                    except :
                        val2 = Gapprox[edg[j][1]][edg[j][0]]['weight']
                    if valmax <= (val1-val2):
                        if int(part[i][0]) != int(edg[j][0]):
                            ind = edg[j][0]
                        if int(part[i][0]) != int(edg[j][1]):
                            ind = edg[j][1]
                        valmax = val1-val2
                com = npart[ind-1]
                part[com] = part[com] + [part[i][0]]
        n2 = len(part)		   
        for i in range(len(part)):
            if len(part[n2-i-1]) == 1 :
                nei = Gr.neighbors(int(part[n2-i-1][0]))
                del part[n2-i-1]
        mod = calculmod(part,Gr,Gapprox,sum1,sum2,orie)
    return part,mod

def gravitaire_oriente_uncomplete(Gr,T,D):
    kin = Gr.in_degree(weight='weight')
    kout = Gr.out_degree(weight='weight')
    flux2 = []
    sumflux = 0
    for i in range(len(T)):
        flux2 = flux2 + [T[i][2]/float(kin[T[i][1]] * kout[T[i][0]])]
        sumflux = sumflux + T[i][2]
    aflux2 = np.array(flux2)
    adist = np.array(D)
    reg = np.polyfit(np.log10(adist),np.log10(aflux2), 1)
    c = np.corrcoef(np.log10(adist),np.log10(aflux2))
    fluxapprox = []
    for i in range(len(T)):
        fluxapprox = fluxapprox + [pow(10, reg[1]) * kin[T[i][1]] * kout[T[i][0]] * pow(D[i], reg[0])]  
    fluxapproxdef = fluxapprox / sum(fluxapprox) * sumflux
    return fluxapproxdef, c, reg[0]

def gravitaire_oriente(Gr,T,T2,D,D2):
    kin = Gr.in_degree(weight='weight')
    kout = Gr.out_degree(weight='weight')
    flux2 = []
    sumflux = 0
    for i in range(len(T2)):
        flux2 = flux2 + [T2[i][2]/float(kin[T2[i][1]] * kout[T2[i][0]])]
        sumflux = sumflux + T2[i][2]
    aflux2 = np.array(flux2)
    adist = np.array(D2)
    reg = np.polyfit(np.log10(adist),np.log10(aflux2), 1)
    c = np.corrcoef(np.log10(adist),np.log10(aflux2))
    fluxapprox = []
    for i in range(len(T)):
        fluxapprox = fluxapprox + [pow(10, reg[1]) * kin[T[i][1]] * kout[T[i][0]] * pow(D[i], reg[0])]  
    fluxapproxdef = fluxapprox / sum(fluxapprox) * sumflux
    return fluxapproxdef, c, reg[0]

def gravitaire_oriente_uncomplete2(Gr,T,D,nit):
    kin = Gr.in_degree(weight='weight')
    kout = Gr.out_degree(weight='weight')
    flux2 = []
    for i in range(len(T)):
        flux2 = flux2 + [T[i][2]/float(kin[T[i][1]] * kout[T[i][0]])]
    aflux2 = np.array(flux2)
    adist = np.array(D)
    reg = np.polyfit(np.log10(adist),np.log10(aflux2), 1)
    c = np.corrcoef(np.log10(adist),np.log10(aflux2))
    fluxapprox = []
    tablefluxapprox = []
    for i in range(len(T)):
        vale = pow(10, reg[1]) * kin[T[i][1]] * kout[T[i][0]] * pow(D[i], reg[0]) 
        fluxapprox = fluxapprox + [vale]
        tablefluxapprox = tablefluxapprox + [[T[i][0], T[i][1], vale]] 
    for i in range(nit):
        Gfluxapprox = nx.DiGraph()
        Gfluxapprox.add_weighted_edges_from(tablefluxapprox)
        koutfluxapprox = Gfluxapprox.out_degree(weight='weight')
        for j in range(len(fluxapprox)):
            vale = fluxapprox[j] * kout[T[j][0]] / float(koutfluxapprox[T[j][0]])
            fluxapprox[j] = vale
            tablefluxapprox[j][2] = vale
        Gfluxapprox = nx.DiGraph()
        Gfluxapprox.add_weighted_edges_from(tablefluxapprox)
        koutfluxapprox2 = Gfluxapprox.out_degree(weight='weight')
        kinfluxapprox = Gfluxapprox.in_degree(weight='weight')
        for j in range(len(fluxapprox)):
            vale = fluxapprox[j] * kin[T[j][1]] / float(kinfluxapprox[T[j][1]])
            fluxapprox[j] = vale
            tablefluxapprox[j][2] = vale
        Gfluxapprox = nx.DiGraph()
        Gfluxapprox.add_weighted_edges_from(tablefluxapprox)
        kinfluxapprox2 = Gfluxapprox.in_degree(weight='weight')
    return fluxapprox, c, reg[0]

def gravitaire_oriente2(Gr,T,T2,D,D2,nit):
    kin = Gr.in_degree(weight='weight')
    kout = Gr.out_degree(weight='weight')
    flux2 = []
    for i in range(len(T2)):
        flux2 = flux2 + [T2[i][2]/float(kin[T2[i][1]] * kout[T2[i][0]])]
    aflux2 = np.array(flux2)
    adist = np.array(D2)
    reg = np.polyfit(np.log10(adist),np.log10(aflux2), 1)
    c = np.corrcoef(np.log10(adist),np.log10(aflux2))
    fluxapprox = []
    tablefluxapprox = []
    for i in range(len(T)):
        vale = pow(10, reg[1]) * kin[T[i][1]] * kout[T[i][0]] * pow(D[i], reg[0]) 
        fluxapprox = fluxapprox + [vale]
        tablefluxapprox = tablefluxapprox + [[T[i][0], T[i][1], vale]] 
    for i in range(nit):
        Gfluxapprox = nx.DiGraph()
        Gfluxapprox.add_weighted_edges_from(tablefluxapprox)
        koutfluxapprox = Gfluxapprox.out_degree(weight='weight')
        for j in range(len(fluxapprox)):
            vale = fluxapprox[j] * kout[T[j][0]] / float(koutfluxapprox[T[j][0]])
            fluxapprox[j] = vale
            tablefluxapprox[j][2] = vale
        Gfluxapprox = nx.DiGraph()
        Gfluxapprox.add_weighted_edges_from(tablefluxapprox)
        koutfluxapprox2 = Gfluxapprox.out_degree(weight='weight')
        kinfluxapprox = Gfluxapprox.in_degree(weight='weight')
        for j in range(len(fluxapprox)):
            vale = fluxapprox[j] * kin[T[j][1]] / float(kinfluxapprox[T[j][1]])
            fluxapprox[j] = vale
            tablefluxapprox[j][2] = vale
        Gfluxapprox = nx.DiGraph()
        Gfluxapprox.add_weighted_edges_from(tablefluxapprox)
        kinfluxapprox2 = Gfluxapprox.in_degree(weight='weight')
    return fluxapprox, c, reg[0]

def gravitaire_uncomplete(Gr,T,D):
    k = Gr.degree(weight='weight')
    flux2 = []
    sumflux = 0
    for i in range(len(T)):
        flux2 = flux2 + [T[i][2]/float(k[T[i][1]] * k[T[i][0]])]
        sumflux = sumflux + T[i][2]
    aflux2 = np.array(flux2)
    adist = np.array(D)
    reg = np.polyfit(np.log10(adist),np.log10(aflux2), 1)
    c = np.corrcoef(np.log10(adist),np.log10(aflux2))
    fluxapprox = []
    for i in range(len(T)):
        fluxapprox = fluxapprox + [pow(10, reg[1]) * k[T[i][1]] * k[T[i][0]] * pow(D[i], reg[0])]  
    fluxapproxdef = fluxapprox / sum(fluxapprox) * sumflux
    return fluxapproxdef, c, reg[0]

def gravitaire(Gr,T,T2,D,D2):
    k = Gr.degree(weight='weight')
    flux2 = []
    sumflux = 0
    for i in range(len(T2)):
        flux2 = flux2 + [T2[i][2]/float(k[T2[i][1]] * k[T2[i][0]])]
        sumflux = sumflux + T2[i][2]
    aflux2 = np.array(flux2)
    adist = np.array(D2)
    reg = np.polyfit(np.log10(adist),np.log10(aflux2), 1)
    c = np.corrcoef(np.log10(adist),np.log10(aflux2))
    fluxapprox = []
    for i in range(len(T)):
        fluxapprox = fluxapprox + [pow(10, reg[1]) * k[T[i][1]] * k[T[i][0]] * pow(D[i], reg[0])]  
    fluxapproxdef = fluxapprox / sum(fluxapprox) * sumflux
    return fluxapproxdef, c, reg[0]

def gravitaire_uncomplete2(Gr,T,D,nit):
    k = Gr.degree(weight='weight')
    flux2 = []
    for i in range(len(T)):
        flux2 = flux2 + [T[i][2]/float(k[T[i][1]] * k[T[i][0]])]
    aflux2 = np.array(flux2)
    adist = np.array(D)
    reg = np.polyfit(np.log10(adist),np.log10(aflux2), 1)
    c = np.corrcoef(np.log10(adist),np.log10(aflux2))
    fluxapprox = []
    tablefluxapprox = []
    for i in range(len(T)):
        vale = pow(10, reg[1]) * k[T[i][1]] * k[T[i][0]] * pow(D[i], reg[0])
        fluxapprox = fluxapprox + [vale]  
        tablefluxapprox = tablefluxapprox + [[T[i][0], T[i][1], vale]] 
    for i in range(nit):
        Gfluxapprox = nx.Graph()
        Gfluxapprox.add_weighted_edges_from(tablefluxapprox)
        kfluxapprox = Gfluxapprox.degree(weight='weight')
        for j in range(len(fluxapprox)):
            val = fluxapprox[j] * k[T[j][0]] / float(kfluxapprox[T[j][0]])
            fluxapprox[j] = val
            tablefluxapprox[j][2] = val
        Gfluxapprox = nx.Graph()
        Gfluxapprox.add_weighted_edges_from(tablefluxapprox)
        kfluxapprox2 = Gfluxapprox.degree(weight='weight')
    return fluxapprox, c, reg[0]

def gravitaire2(Gr,T,T2,D,D2,nit):
    k = Gr.degree(weight='weight')
    flux2 = []
    for i in range(len(T2)):
        flux2 = flux2 + [T2[i][2]/float(k[T2[i][1]] * k[T2[i][0]])]
    aflux2 = np.array(flux2)
    adist = np.array(D2)
    reg = np.polyfit(np.log10(adist),np.log10(aflux2), 1)
    c = np.corrcoef(np.log10(adist),np.log10(aflux2))
    fluxapprox = []
    tablefluxapprox = []
    for i in range(len(T)):
        vale = pow(10, reg[1]) * k[T[i][1]] * k[T[i][0]] * pow(D[i], reg[0])
        fluxapprox = fluxapprox + [vale]  
        tablefluxapprox = tablefluxapprox + [[T[i][0], T[i][1], vale]] 
    for i in range(nit):
        Gfluxapprox = nx.Graph()
        Gfluxapprox.add_weighted_edges_from(tablefluxapprox)
        kfluxapprox = Gfluxapprox.degree(weight='weight')
        for j in range(len(fluxapprox)):
            val = fluxapprox[j] * k[T[j][0]] / float(kfluxapprox[T[j][0]])
            fluxapprox[j] = val
            tablefluxapprox[j][2] = val
        Gfluxapprox = nx.Graph()
        Gfluxapprox.add_weighted_edges_from(tablefluxapprox)
        kfluxapprox2 = Gfluxapprox.degree(weight='weight')
    return fluxapprox, c, reg[0]



