import sys, os

''' 
python get_ColSynonyms.py NameUsage.tsv Collembola collembola_unique_n_occurence.txt 
output: collembola_unique_n_occurence_ColSynonyms.tsv
'''

TaxBackbone=sys.argv[1]
HigherTaxName=sys.argv[2] #Collembola
TaxoBold=sys.argv[3]

D={'kingdom': 0, 'phylum': 1, 'class': 2, 'order': 3, 'family': 4, 'subfamily': 5, 'tribe': 6,'genus': 7, 'species': 8}

def if_empty(st):
    if st=='':
        return 'NA'
    else:
        return st

def insert_ScientificNamebyRank (L, taxRank, ScientificName, D): #L is a list containing 
    RankIndex=D[taxRank]
    L[RankIndex]=ScientificName
    return L
    

def get_accepted_synonyms(CoL_TaxBackbone, HigherTaxName, D):
    #D={'kingdom': 0, 'phylum': 1, 'class': 2, 'order': 3, 'family': 4, 'subfamily': 5, 'tribe': 6,'genus': 7, 'species': 8}
    D_AcceptedSpID_Taxonomy={}
    D_synonymID_SynonymName={}
    D_SciNameID_SynonymID={}
    D_SciName_ColID={}
    f=open(CoL_TaxBackbone, 'r')
    Headers=f.readline()
    #info we need:
    L_Headers = Headers.strip().split('\t')
    #colID = L_Headers[0]
    colID = L_Headers.index('col:ID')
    SynonymID_Index = L_Headers.index('col:parentID')
    SciName_Index = L_Headers.index('col:scientificName')
    rank_Index = L_Headers.index('col:rank')
    status_Index = L_Headers.index('col:status')
    species_Index = L_Headers.index('col:species')
    genus_Index = L_Headers.index('col:genus')
    family_Index = L_Headers.index('col:family')
    subfamily_Index = L_Headers.index('col:subfamily')
    tribe_Index = L_Headers.index('col:tribe')
    order_Index = L_Headers.index('col:order')
    class_Index = L_Headers.index('col:class')
    phylum_Index = L_Headers.index('col:phylum')
    kingdom_Index = L_Headers.index('col:kingdom')
    for line in f:
        l=line.strip().split('\t')
        if l[status_Index] == 'accepted':
            if l[class_Index]==HigherTaxName:
                if l[rank_Index] in D:
                    Taxo_Temp = [if_empty(l[kingdom_Index]), if_empty(l[phylum_Index]), if_empty(l[class_Index]), if_empty(l[order_Index]), if_empty(l[family_Index]), if_empty(l[subfamily_Index]), if_empty(l[tribe_Index]), if_empty(l[genus_Index]), if_empty(l[species_Index])]
                    Taxo = insert_ScientificNamebyRank (Taxo_Temp, l[rank_Index], l[SciName_Index], D)
                    D_AcceptedSpID_Taxonomy[l[SciName_Index]]=Taxo
                    D_SciName_ColID[l[SciName_Index]]=if_empty(l[colID])
        if l[status_Index] == 'synonym':
            D_synonymID_SynonymName.setdefault(if_empty(l[colID]),[]).append(if_empty(l[SciName_Index]))
            D_SciNameID_SynonymID.setdefault(l[SynonymID_Index], []).append(l[colID])
    f.close()
    return D_AcceptedSpID_Taxonomy, D_synonymID_SynonymName, D_SciNameID_SynonymID, D_SciName_ColID


ColRes=get_accepted_synonyms(TaxBackbone, HigherTaxName, D)
AcceptedSpID_Taxonomy=ColRes[0]
synonymID_SynonymName=ColRes[1]
SciNameID_SynonymID=ColRes[2]
SciName_ColID=ColRes[3]

def get_TaxoBOLD(f_BOLDTaxonomy):
    t=range(9)
    f=open(f_BOLDTaxonomy, 'r')
    f.readline()
    D_SpName_Taxonomy={}
    for line in f:
        l=line.strip().split('\t')
        Sp=l[8]
        t_temp=[]
        for i in t:
            t_temp.append(l[i])
        D_SpName_Taxonomy[Sp]=t_temp
    f.close()
    return D_SpName_Taxonomy

Bold_Sp_Taxo=get_TaxoBOLD(TaxoBold)
print(len(Bold_Sp_Taxo))

def get_diff_subTaxonomy(boldT, ColT):
    for i, n in enumerate(boldT):
        if n!=ColT[i] and (n=='NA' or ColT[i] == 'NA'):
            return True

def get_BoldTaxo_ColSynonyms(Bold_Sp_Taxo, SciName_ColID, SciNameID_SynonymID, AcceptedSpID_Taxonomy):
    D_BoldTaxonomy_ColSynonyms={}
    f_temp_out=open('Conflicting_BOLD_COL_Taxonomies.tsv', 'w')
    f_temp_out.write('BOLD_Taxonomy\tCOL_Taxonomy\n')
    n=0
    m=0
    for i in Bold_Sp_Taxo:
        if i in SciName_ColID:
            n+=1
            BoldTaxonomy=Bold_Sp_Taxo[i]
            ColTaxonomy=AcceptedSpID_Taxonomy[i]
            #print(BoldTaxonomy, ColTaxonomy)
            if BoldTaxonomy == ColTaxonomy:
                ID=SciName_ColID[i]
                if ID in SciNameID_SynonymID:
                    synonyms_temp=[]
                    #print(ID, SciNameID_SynonymID[ID])
                    for j in SciNameID_SynonymID[ID]:
                        synonyms_temp.append(synonymID_SynonymName[j])
                    #print(synonyms_temp)
                    D_BoldTaxonomy_ColSynonyms[';'.join(BoldTaxonomy)]=';'.join(list(set(sum(synonyms_temp,[]))))
                else:
                    D_BoldTaxonomy_ColSynonyms[';'.join(BoldTaxonomy)]=''
            else:
                if get_diff_subTaxonomy(BoldTaxonomy, ColTaxonomy) == True:
                    ID=SciName_ColID[i]
                    if ID in SciNameID_SynonymID:
                        synonyms_temp=[]
                        for j in SciNameID_SynonymID[ID]:
                            synonyms_temp.append(synonymID_SynonymName[j])
                        #print(synonyms_temp)
                        D_BoldTaxonomy_ColSynonyms[';'.join(BoldTaxonomy)]=';'.join(list(set(sum(synonyms_temp,[]))))
                    else:
                        D_BoldTaxonomy_ColSynonyms[';'.join(BoldTaxonomy)]=''
                else:
                    D_BoldTaxonomy_ColSynonyms[';'.join(BoldTaxonomy)]=''
                    f_temp_out.write(';'.join(BoldTaxonomy)+'\t'+';'.join(ColTaxonomy)+'\n')
                    print (BoldTaxonomy, ColTaxonomy)
        else:
            D_BoldTaxonomy_ColSynonyms[';'.join(Bold_Sp_Taxo[i])]=''
    f_temp_out.close()
    print(n, m)
    print (len(D_BoldTaxonomy_ColSynonyms))
    return D_BoldTaxonomy_ColSynonyms


BoldWithColSyn = get_BoldTaxo_ColSynonyms(Bold_Sp_Taxo, SciName_ColID, SciNameID_SynonymID, AcceptedSpID_Taxonomy)

def write_BoldTaxo_ColSynonyms(f_BOLDTaxonomy, BoldWithColSyn, D):
    f_out = open(f_BOLDTaxonomy.split('.')[0]+'_ColSynonyms.tsv', 'w')
    TaxPath=';'.join(D.keys())
    f_out.write('BOLD_Taxonomy|'+TaxPath+ '\tCatalogueOfLife_Synonyms\n')
    for t in BoldWithColSyn:
        f_out.write(t + '\t' + BoldWithColSyn[t] + '\n')
    f_out.close()

WriteBoldWithColSyn = write_BoldTaxo_ColSynonyms(TaxoBold, BoldWithColSyn, D)
    
