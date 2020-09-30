#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Nicole Dodd

Purpose of this script:
Build a Spanish dictionary using the Spanish Billion Words Corpus
Cristian Cardellino: Spanish Billion Words Corpus and Embeddings (March 2016)
https://crscardellino.github.io/SBWCE/

sys.argv[1] = path to .tar file
sys.argv[2] = name of dict to be exported into .txt file
'''

import sys, tarfile, io


## Step 1: Build dictionary from Spanish Billion Words Corpus #################

es_dict = []

tar = tarfile.open(sys.argv[1], 'r')
all_docs = tar.getmembers()
total = int(len(all_docs))
doc = 0

for member in tar.getmembers():
    f = tar.extractfile(member) # note: encoded in bytes
    if f is not None:
        content = f.read()
        decoded = content.decode(encoding='utf-8')
        toks = decoded.split()
        for tok in toks:
            if tok.lower() not in es_dict:
                es_dict.append(tok.lower())

        doc = doc + 1
        progress = (doc / total) * 100
        print(str(round(progress)) + '% complete')


## Step 2: Add Gutenberg-specific abbreviations to dict #######################
## (taken from SpanishReader.py script)

abbreviations = ['...', 'Arqueol.', '&c.', 'Mme.', 'Lib.', 'Lic.', 'Antrop.',
                'núm.', 'Dres.', 'Descrip.', '—tom.', 'rs.', 'lám.,' 'Sec.',
                'Liv.', 'Introd.', 'Excmo.', 'Caps.', 'Amer.', 'oct.', 'Antigs.',
                'Ses.', 'Moderns.', 'Moralíz.', 'Esp.', 'Lam.', 'act.', 'Europ.',
                'Geog.', 'CC.', 'Eneid.', 'Nat.', 'M.', 'Crón.', 'Ntra.', 'men.',
                'Láms.', 'Orth.', 'Gam.', 'tam.', 'Arg.', 'Op.', 'caps.', 'Agust.',
                'fol.', 'Sr.', 'Tam.', 'Janr.', 'MS.', 'Bol.', 'Mr.', 'S.A.S.',
                'Núms.', 'Civiliz.', 'Figs.', 'DR.', 'Orígs.', 'Vocabuls.', 'cits.',
                'L.E.', 'Dicc.', 'paj.', 'Amér.', 'Lám.', 'ESQ.', 'op.', 'Argent.',
                'NE.', 'Sres.', 'Esp.', 'Lam.', 'Exmo.', 'Espagn.', 'pag.', 'Conq.',
                'Cont.', 'Sr.', 'SR.', 'SO.', 'Ind.', 'ded.', 'cuads.', 'Oct.',
                'Psch.', 'Ed.', 'Sta.', 'Fot.', 'sec.', 'Part.', 'JUV.', 'Arqueolog.',
                'Sto.', 'pp.', 'Antig.', 'vol.Cod.', 'Srta.', 'Col.', 'lib.',
                'Congr.', 'lin.', 'Colec.', 'Instit.', 'Cong.', 'Cient.', 'Mlle.',
                'Rev.', 'LLOR.', 'nat.', 'gr.', 'ROB.', 'Ge.', 'Ord.', 'lec.',
                'FR.', 'Fr.', 'ILMO.', 'Colecc.', 'Pág.', 'Tuc.', 'Prov.', 'EXCMO.',
                'Págs.', 'p.m.', 'sc.', 'capits.', 'Pl.', 'PP.', 'lug.', 'Sra.',
                'a.m.', 'Antich.', 'Gen.', 'Apénd.', 'Cap.', 'Bs.', 'pags.', 'MSS.',
                'cap.', 'Vds.', 'nos.', 'tom.', 'Lug.', 'Dr.', 'págs.', 'id.',
                'pág.', 'verb.', 'Or.', 'sigtes.', 'SEB.', 'Hist.', 'Vd.', 'ci.',
                'vol.', 'cit.', 'etc.', 'Cía.', 'Id.', 'Nos.', 'Ibid.', 'LLO.',
                'Ud.', 'Fig.', 'Geográf.', 'Internat.', 'Sant.', 'ps.', 'part.',
                'Luxemburg.']

prepositions = ['á', 'ó']

for abbrev in abbreviations:
    es_dict.append(abbrev)

for prep in prepositions:
    es_dict.append(prep)


## Step 3: Write dict to file #################################################

with io.open(sys.argv[2], 'w', encoding = 'utf-8') as f:
    f.write('\n'.join(es_dict))

print(len(es_dict))
