import pprint
import requests
import csv
import pdb

# FOR DEBUGGING
pp = pprint.PrettyPrinter(indent=4)

# INITIALIZE CSV FILE, FIELDS ARRAY, ROWS ARRAY
fileWrite = "genes.csv"

# FILE TO READ, MUST BE IN SAME DIRECTORY AS THIS FILE
fileRead = "CSVtest.csv"

# INITIALIZE FIELDS FOR CSV THAT WILL BE WRITTEN TO
writeFields = ['Term / Ensemble Gene ID', 'ID', 'Nomenclature Symbol']

# INITIALIZE EMPTY ARRAY FOR ROWS THAT WILL BE WRITTEN, WILL BE ARRAY OF SUB-ARRAYS
writeRows = []

# ROWS THAT ARE READ FROM INPUT CSV FILE
readRows = []

# OPEN INPUT CSV AND READ FIELDS INTO ARRAY
with open(fileRead, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    # fields = csvreader.next()

    # extracting each data row one by one
    for row in csvreader:
        readRows.append(row)

    # get total number of rows
    print("Total no. of rows: %d"%(csvreader.line_num))

# FROM INPUT CSV, QUERY ON EACH TERM THAT IS NOW IN readRows
for term in readRows[:30]:
    term = term[0]

    # QUERY TO GET ID FROM PROVIDED TERM, ex. term - ENSG00000099869
    gene_id_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?retmode=json&db=gene&term=" + term

    # QUERY NIH API
    r = requests.get(gene_id_url)
    rj = r.json()

    # IF TERM IS NOT FOUND, APPEND 'Not Found', GO TO NEXT TERM
    if rj['esearchresult']['count'] == '0':
        writeRows.append([
            term,
            "ID Not Found",
            "Nomenclature Not Found"
        ])
        continue

    # GET GENE_ID FROM RESULT, ex ID - 51214
    gene_id = rj['esearchresult']['idlist'][0]

    # QUERY FOR MORE INFO ABOUT GENE USING ID
    gene_info_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?retmode=json&db=gene&id=" + gene_id

    # QUERY NIH API
    r2 = requests.get(gene_info_url)
    gene = r2.json()['result']

    # PRINT OUTPUT TO STDOUT
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(gene)

    # WRITE SELECTED INFO TO writeRows
    # THIS CAN BE EXPANDED JUST BE SURE TO ADD ANOTHER VALUE TO writeFields
    writeRows.append([
        term,
        gene_id,
        gene[gene_id]['nomenclaturesymbol']
    ])

# WRITE writeFields TO OUTPUT CSV FILE
with open(fileWrite, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(writeFields)

    # writing the data rows
    csvwriter.writerows(writeRows)
