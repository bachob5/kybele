import sys

'''
Execution:
cd /home/user/NCBI_Taxonomy/ftp/Update_240226
python get_NCBISynonyms.py /home/user/KYBELE/collembola_unique_n_occurence.txt
'''


'''
pwd /home/user/NCBI_Taxonomy/ftp/Update_240226
wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz
tar -xzf new_taxdump.tar.gz
'''

RankedLineages_NCBI = 'rankedlineage.dmp'
Nodes_NCBI = 'nodes.dmp'
NCBI_taxonomy_Path = '/KYBELE/NCBI_Taxonomy/ftp/Update_240226/'

TaxoBold=sys.argv[1]

Euk='Eukaryota'

def get_TaxoBOLD(f_BOLDTaxonomy):
    t=range(9)
    f=open(f_BOLDTaxonomy, 'r')
    f.readline()
    D_SpName_Taxonomy={}
    for line in f:
        l=line.strip().split('\t')
        Sp=l[8].strip()
        t_temp=[]
        for i in t:
            t_temp.append(l[i])
        D_SpName_Taxonomy[Sp]=t_temp
    f.close()
    return D_SpName_Taxonomy

Bold_Sp_Taxo=get_TaxoBOLD(TaxoBold)


def taxonomyLevelsNum():
    D_TaxonomyLevelsNum={}
    TaxR='phylum,class,order,family,genus,species'
    TaxRanks=TaxR.split(',')
    for i,n in enumerate(TaxRanks):
        D_TaxonomyLevelsNum[n]=i
    return D_TaxonomyLevelsNum

taxonomyLevelsNum=taxonomyLevelsNum()


def get_SpeciesNodes(f_Nodes_NCBI):
    D_TaxId_True={}
    D_OtherRanks_TaxIds={}
    D_TaxidsAll_True={}
    D_OtherRanks_TaxIds_1={}
    D_TaxidsAll_True_1={}
    R1=['phylum', 'class', 'order', 'family', 'subfamily', 'tribe', 'genus']
    R=['phylum', 'class', 'order', 'family', 'genus']
    f=open(f_Nodes_NCBI, 'r')
    for line in f:
        l=line.split('\t')
        TxId=l[0].strip()
        Sp=l[4].strip()
        if Sp=='species':
            D_TaxId_True[TxId]=True
            D_TaxidsAll_True[TxId]=True
            D_TaxidsAll_True_1[TxId]=True
        elif Sp in R:
            D_OtherRanks_TaxIds[TxId]=Sp
            D_TaxidsAll_True[TxId]=True
        if Sp in R1:
            D_OtherRanks_TaxIds_1[TxId]=Sp
            D_TaxidsAll_True_1[TxId]=True
        else:
            continue
    f.close()
    return D_TaxId_True, D_OtherRanks_TaxIds, D_TaxidsAll_True, D_OtherRanks_TaxIds_1, D_TaxidsAll_True_1

S=get_SpeciesNodes(Nodes_NCBI)
SpeciesNodes=S[0]
OtherRanks=S[1]
MainRanks_Taxids=S[2] 
NeededOtherRanks=S[3]
NeededRanks_Taxids=S[4] 

def getTaxID_SynNames(NCBITaxonomyPath):
    Dict_TaxID_ScientificNames={}
    Dict_ScientificNames_TaxID={}
    Dict_Synonyms_TaxID={}
    f_TaxNames=open(NCBITaxonomyPath+'names.dmp','r')
    for line in f_TaxNames:
        l=line.split('\t')
        tax_id=l[0].strip()
        name_txt=l[2].strip()
        className=l[6]
        if className =='scientific name':
            Dict_TaxID_ScientificNames[tax_id]=name_txt
            Dict_ScientificNames_TaxID.setdefault(name_txt,[]).append(tax_id)
        elif className=='synonym':
            Dict_Synonyms_TaxID.setdefault(tax_id,[]).append(name_txt)
        elif className=='equivalent name':
            Dict_Synonyms_TaxID.setdefault(tax_id,[]).append(name_txt)
    f_TaxNames.close()
    return Dict_ScientificNames_TaxID, Dict_Synonyms_TaxID, Dict_TaxID_ScientificNames

tx_n_Id=getTaxID_SynNames(NCBI_taxonomy_Path)
SciName_TaxId=tx_n_Id[0]
Synonyms_TaxId=tx_n_Id[1]
TaxID_ScientificNames=tx_n_Id[2]


def get_Taxid_lineage():
    TaxidLineageFile=NCBI_taxonomy_Path+'taxidlineage.dmp'
    D_Taxid_lineage={}
    f_taxidlin=open(TaxidLineageFile,'r')
    for line in f_taxidlin:
        l=line.split('\t|\n')[0].split('\t|\t')
        TaxId=l[0].strip()
        lineage_Txid=l[1].strip()
        D_Taxid_lineage[TaxId]=lineage_Txid+' '+TaxId
    f_taxidlin.close()
    return D_Taxid_lineage

Taxid_Lineages=get_Taxid_lineage()


def get_Taxid_Taxonomy(f_rankedLineages, SpeciesNodes, OtherRanks):
    D_TAXON_Taxid_Taxonomy={}
    #L_TaxID_Kingdom=[]
    f=open(f_rankedLineages, 'r')
    for line in f:
        l=line.split('|')
        Taxid=l[0].strip()
        TAXON=l[1].strip()
        SuperKing=l[9].strip()
        #King=l[8].strip()
        Phylum=l[7].strip()
        Class=l[6].strip()
        Order=l[5].strip()
        Family=l[4].strip()
        Genus=l[3].strip()
        Species=l[2].strip() 
        if SuperKing==Euk:
            if Taxid in SpeciesNodes:
                D_TAXON_Taxid_Taxonomy.setdefault(TAXON,[]).append([Taxid, Phylum, Class, Order, Family, Genus, TAXON])
            else:
                #D={}
                if Taxid in OtherRanks:
                    Rank=OtherRanks[Taxid]
                    Pos=taxonomyLevelsNum[Rank]
                    L_Tax=[Phylum, Class, Order, Family, Genus, Species]
                    L_Tax.pop(Pos)
                    L_Tax.insert(Pos, TAXON)                        
                    D_TAXON_Taxid_Taxonomy.setdefault(TAXON,[]).append([Taxid]+L_Tax)
    f.close()
    return D_TAXON_Taxid_Taxonomy
        

TT=get_Taxid_Taxonomy(RankedLineages_NCBI, SpeciesNodes, OtherRanks)
Taxon_Txid_Taxonomy=TT



def get_rankedTaxids(SpeciesNodes, OtherRanks, Taxid_Lineages, taxonomyLevelsNum):
    D_Taxid_RankedLineages={}
    for tid in Taxid_Lineages:
        D={}
        allTaxids=Taxid_Lineages[tid].split()
        for txid in allTaxids:
            if txid.strip() in SpeciesNodes:
                D[taxonomyLevelsNum['species']]=txid.strip()
            elif txid.strip() in OtherRanks:
                rank=OtherRanks[txid.strip()]
                N=taxonomyLevelsNum[rank]
                D[N]=txid.strip()
            else:
                continue
        for r in taxonomyLevelsNum:
            N=taxonomyLevelsNum[r]
            if N not in D:
                D[N]='NA'
        D1=list(D.items())
        D1.sort()
        L=[]
        for n in D1:
            L.append(n[1])
        D_Taxid_RankedLineages[tid]=L
    return D_Taxid_RankedLineages

Taxid_RankedLineages=get_rankedTaxids(SpeciesNodes, OtherRanks, Taxid_Lineages, taxonomyLevelsNum)


def harmonizeSynonyms(Taxon_Txid_Taxonomy, Synonyms_TaxId):
    D_HarmonizedSyn={}
    temp_Txn_Txid_Taxo={}
    for t in Taxon_Txid_Taxonomy:
        val=Taxon_Txid_Taxonomy[t]
        if len(val)==1:
            temp_Txn_Txid_Taxo[val[0][0]]=val
        else:
            for v in val:
                temp_Txn_Txid_Taxo[v[0]]=[v]
    for SynTaxId in Synonyms_TaxId:
        try:
            syn=temp_Txn_Txid_Taxo[SynTaxId]
            for s in Synonyms_TaxId[SynTaxId]:
                D_HarmonizedSyn.setdefault(s,[]).append(syn[0])
        except KeyError:
            continue
    return D_HarmonizedSyn

HarmonizedSyn=harmonizeSynonyms(Taxon_Txid_Taxonomy, Synonyms_TaxId)


def get_TaxId_fullNamesLineage():
    D_Taxid_lineageNames={}
    D_Taxon_TaxIDfullineage={}
    Taxid_FullNamesLineage=NCBI_taxonomy_Path+'fullnamelineage.dmp'
    f_fl=open(Taxid_FullNamesLineage, 'r')
    for line in f_fl:
        l=line.split('\t|\n')[0].split('\t|\t')
        Taxid_Organism=l[0].strip()
        sciName_org=l[1].strip()
        TaxIds_lineage=l[2].strip()
        if Euk in TaxIds_lineage:
            D_Taxid_lineageNames[Taxid_Organism]=TaxIds_lineage+sciName_org
            D_Taxon_TaxIDfullineage.setdefault(sciName_org,[]).append([Taxid_Organism, TaxIds_lineage])
    f_fl.close()
    return D_Taxid_lineageNames, D_Taxon_TaxIDfullineage

fullLineage=get_TaxId_fullNamesLineage()
Taxid_lineageNames=fullLineage[0]
Taxon_TaxIDfullineage=fullLineage[1]

print (list(Taxid_lineageNames.items())[100:110])
print (list(Taxon_TaxIDfullineage.items())[100:110])

'''
here we should create the taxonomy according to a specific pattern. In our case including subfamily and tribe:
- start with sp name
- get the full taxid list
- search the taxid for its rank
- if the rank is present in the list get its name
- if the rank not present insert NA
- search the sp name of bold if present in the above and assert their taxonomy (start from phylum)
- search for the sp taxid the synonym in harmonized synonyms
- get all in one dict
'''

def get_diff_subTaxonomy(boldT, ncbiT):
    for i, n in enumerate(boldT):
        if n!=ncbiT[i]:
            if n=='NA' or ncbiT[i] == 'NA':
                return True


def personalize_TaxPath(Bold_Sp_Taxo, Taxon_TaxIDfullineage, NeededOtherRanks, NeededRanks_Taxids, Taxid_Lineages, SpeciesNodes, Synonyms_TaxId):
    D_Taxon_NeededRanks={}
    D_Taxon_ConflictingNCBItaxonomy={}
    L_Taxon_NotFound=[]
    TaxR='phylum,class,order,family,subfamily,tribe,genus,species'
    l_TaxR=TaxR.split(',')
    D_rank_Pos={}
    for i,n in enumerate(l_TaxR):
        D_rank_Pos[n]=i
    for tx in Bold_Sp_Taxo:
        if tx in Taxon_TaxIDfullineage:
            D_Index_Taxon={}
            L_Taxonomy=[]
            D_Sp_tid_temp={}
            tx_tid_lineage=Taxon_TaxIDfullineage[tx]
            if len(tx_tid_lineage)==1:
                tid_lineage=tx_tid_lineage[0]
                tid=tid_lineage[0]
                lineage=tid_lineage[1].split(';')
                allTids=Taxid_Lineages[tid].split()
                for j,t in enumerate(allTids):
                    if t in NeededOtherRanks:
                        Index=D_rank_Pos[NeededOtherRanks[t]]
                        D_Index_Taxon[Index]=lineage[j].strip()
                        if tid in SpeciesNodes:
                            D_Index_Taxon[D_rank_Pos['species']]=tx
                            D_Sp_tid_temp[tx]=tid
            else:
                print(tx, len(Taxon_TaxIDfullineage[tx]), Taxon_TaxIDfullineage[tx])
            for r in D_rank_Pos:
                pos=D_rank_Pos[r]
                if pos not in D_Index_Taxon:
                    D_Index_Taxon[pos]='NA'
            extractedTaxo=sorted(D_Index_Taxon.items())
            for ex in extractedTaxo:
                L_Taxonomy.append(ex[1])#.strip())
            if get_diff_subTaxonomy(Bold_Sp_Taxo[tx][1:], L_Taxonomy) == True or Bold_Sp_Taxo[tx][1:] == L_Taxonomy:
                ncbiSynonyms_Tid=D_Sp_tid_temp[L_Taxonomy[-1]]
                if ncbiSynonyms_Tid in Synonyms_TaxId:
                    D_Taxon_NeededRanks[';'.join(Bold_Sp_Taxo[tx])]= [Synonyms_TaxId[ncbiSynonyms_Tid], ['\t'], Taxid_RankedLineages[ncbiSynonyms_Tid]]
                else:
                    D_Taxon_NeededRanks[';'.join(Bold_Sp_Taxo[tx])]= [[''],['\t'], Taxid_RankedLineages[ncbiSynonyms_Tid]] #+ [ncbiSynonyms_Tid]+['\t']
            else:
                D_Taxon_ConflictingNCBItaxonomy[';'.join(Bold_Sp_Taxo[tx])]= L_Taxonomy
        else:
            L_Taxon_NotFound.append(';'.join(Bold_Sp_Taxo[tx]))
    f_out=open(TaxoBold.split('.')[0]+'_ncbiSynonyms.tsv', 'w')
    f_out.write('BOLD_Taxonomy|kingdom;'+';'.join(l_TaxR)+ '\tNCBI_Synonyms\tRankedTaxIDs|phylum;class;order;family;genus;species\n')
    for h in D_Taxon_NeededRanks:
        f_out.write(h + '\t') #+ ';'.join(D_Taxon_NeededRanks[h]) + '\n')
        for v in D_Taxon_NeededRanks[h]:
            f_out.write(';'.join(v))
        f_out.write('\n')
    f_out.close()
    f_out_conflict=open(TaxoBold.split('.')[0]+'_ncbi_ConflictingTaxonomies.tsv', 'w')
    f_out_conflict.write('BOLD_Taxonomy|kingdom;'+';'.join(l_TaxR)+ '\tNCBI_Taxonomy|'+';'.join(l_TaxR) +'\n')
    for taxConf in D_Taxon_ConflictingNCBItaxonomy:
        f_out_conflict.write(taxConf+'\t'+';'.join(D_Taxon_ConflictingNCBItaxonomy[taxConf])+'\n')
    f_out_conflict.close()
    f_out_TaxonNotFound=open(TaxoBold.split('.')[0]+'_ncbi_TaxaNotFound.tsv', 'w')
    f_out_TaxonNotFound.write('BOLD_Taxonomy|kingdom;'+';'.join(l_TaxR)+'\n')
    f_out_TaxonNotFound.write('\n'.join(L_Taxon_NotFound))
    f_out_TaxonNotFound.close()
    
    

r=personalize_TaxPath(Bold_Sp_Taxo, Taxon_TaxIDfullineage, NeededOtherRanks, NeededRanks_Taxids, Taxid_Lineages, SpeciesNodes, Synonyms_TaxId)


'Bold_Sp_Taxo, Taxon_TaxIDfullineage, NeededOtherRanks, NeededRanks_Taxids, Taxid_Lineages, SpeciesNodes, Synonyms_TaxId'
SpeciesNodes=S[0]
OtherRanks=S[1] #get taxid for main ranks (in R) from here
MainRanks_Taxids=S[2] 
NeededOtherRanks=S[3] #get taxid for the requested ranks (in R1) from here
NeededRanks_Taxids=S[4] 





