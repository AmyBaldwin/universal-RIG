#!/usr/bin/env python3

import csv
import urllib.request
import codecs
import gzip 
import requests
import shutil
import time, datetime, os
import sys

#### SETTING UP PARAMETERS ####

## GENERA ##
genera = sys.argv[1]
genus_filters = genera.split(",")
print("The Genera will be: ", genus_filters)

## QUANTITY ##
max = int(sys.argv[2]) - 1
print("The number of species downloaded for each Genera will be: ", sys.argv[2])

## FILE EXTENSION ##
ending = sys.argv[3]
print("The file extension will be: ", ending)

#### PARAMETERS END ####


#### Configure options here ####

# RefSeq assembly summary URL
refseq_summary_url = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt"

# Remove species names containing these strings
string = ' sp.'
genus_filters_negative = [x + string for x in genus_filters]

other_negative_filters = ["phage", "virus"]
genus_filters_negative.extend(other_negative_filters)

#### Configure options end ####


#### Make output directory ####

today = datetime.date.today()  

todaystr = today.isoformat()   

os.mkdir(ending + "_" + todaystr)

os.chdir(ending + "_" + todaystr)

#### Make output directory end ####


def get_speciesname_from_string(name):
    '''
    Tidy up genus/species names to remove strain designations
    in the incorrect field

    Returns string containing Genus species OR 
    Genus species subsp. subspecies
    '''

    if "subsp." in name:
        clean_name = " ".join(name.split()[0:4])
    else:
        clean_name = " ".join(name.split()[0:2])

    return clean_name


# Stream RefSeq assembly summary and create a list of each line
print("Downloading RefSeq Summary")

ftpstream = urllib.request.urlopen(refseq_summary_url)
csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'), delimiter='\t')


# Create dict of {header: line_property}. Gets around first line being unrealated to the table 
csvkeys = []
csvlines = []
for line in csvfile:
    if "# assembly_accession" in line[0]:
        line[0] = line[0].replace('# ', '')
        csvkeys = list(line)
    elif "#" not in line[0]:
        csvlines.append(line)

dictlist = []
for line in csvlines:
    linedict = dict(zip( csvkeys, line))
    dictlist.append(linedict)


# Filter dict from csv to contain just selected genera and remove lines with unwanted
# strings in species name

filtered_dicts_genus = []
negative_filtered_accessions = []

for line in dictlist:
    if line['organism_name'].lower().startswith(tuple( [ x.lower() for x in genus_filters ]) ):
        line['organism_name'] = get_speciesname_from_string(line['organism_name'])
        filtered_dicts_genus.append(line)
        for neg_filter in [ x.lower() for x in genus_filters_negative ]:
            if neg_filter in line['organism_name'].lower():
                negative_filtered_accessions.append(line['assembly_accession'])

negative_filtered_dicts = []

for line in filtered_dicts_genus:
    if line['assembly_accession'] not in negative_filtered_accessions:
        negative_filtered_dicts.append(line)


# Dereplicate the filtered dict to keep just the highest spec representative from each species
# Reference genome, representative genome, Complete genome, Scaffold then Contig assemblies
# Keep track of species encountered at each stage

##### Section 1: reference

filtered_dicts = []
added_species = []

for line in negative_filtered_dicts:
    if "reference genome" in line['refseq_category'] and added_species.count(line['species_taxid']) <= max:
        filtered_dicts.append(line)
        added_species.append(line['species_taxid'])

# remove the entry(s) from the original dictionary

negative_filtered_dicts = [x for x in negative_filtered_dicts if not ('reference genome' == x.get('refseq_category'))]


##### Section 2: representative

for line in negative_filtered_dicts:
    if "representative genome" in line['refseq_category'] and added_species.count(line['species_taxid']) <= max:
        filtered_dicts.append(line)
        added_species.append(line['species_taxid'])

# remove the entry(s) from the original dictionary

negative_filtered_dicts = [x for x in negative_filtered_dicts if not ('representative genome' == x.get('refseq_category'))]


##### Section 3: Complete Genome AND type

for line in negative_filtered_dicts:
    if "assembly from type material" in line['relation_to_type_material'] and "Complete Genome" in line['assembly_level'] and added_species.count(line['species_taxid']) <= max:
       filtered_dicts.append(line)
       added_species.append(line['species_taxid'])

# remove the entry(s) from the original dictionary

negative_filtered_dicts = [x for x in negative_filtered_dicts if not ('assembly from type material' == x.get('relation_to_type_material') and 'Complete Genome' == x.get('assembly_level'))]


##### Section 4: Complete Genome

for line in negative_filtered_dicts:
    if "Complete Genome" in line['assembly_level'] and added_species.count(line['species_taxid']) <= max:
        filtered_dicts.append(line)
        added_species.append(line['species_taxid'])

# remove the entry(s) from the original dictionary

negative_filtered_dicts = [x for x in negative_filtered_dicts if not ('Complete Genome' == x.get('assembly_level'))]


##### Section 5: Scaffold AND TYPE

for line in negative_filtered_dicts:
    if "assembly from type material" in line['relation_to_type_material'] and "Scaffold" in line['assembly_level'] and added_species.count(line['species_taxid']) <= max:
        filtered_dicts.append(line)
        added_species.append(line['species_taxid'])
 
# remove the entry(s) from the original dictionary

negative_filtered_dicts = [x for x in negative_filtered_dicts if not ('assembly from type material' == x.get('relation_to_type_material') and 'Scaffold' == x.get('assembly_level'))]


##### Section 6: Scaffold

for line in negative_filtered_dicts:
    if "Scaffold" in line['assembly_level'] and added_species.count(line['species_taxid']) <= 0:
        filtered_dicts.append(line)
        added_species.append(line['species_taxid'])

# remove the entry(s) from the original dictionary

negative_filtered_dicts = [x for x in negative_filtered_dicts if not ('Scaffold' == x.get('assembly_level'))]


##### Section 7: Contig AND type

for line in negative_filtered_dicts:
    if "assembly from type material" in line['relation_to_type_material'] and "Contig" in line['assembly_level'] and added_species.count(line['species_taxid']) <= max:
        filtered_dicts.append(line)
        added_species.append(line['species_taxid'])

# remove the entry(s) from the original dictionary

negative_filtered_dicts = [x for x in negative_filtered_dicts if not ('assembly from type material' == x.get('relation_to_type_material') and 'Contig' == x.get('assembly_level'))]


##### Section 8: Contig

for line in negative_filtered_dicts:
    if "Contig" in line['assembly_level'] and added_species.count(line['species_taxid']) <= max:
        filtered_dicts.append(line)
        added_species.append(line['species_taxid'])

# remove the entry(s) from the original dictionary

negative_filtered_dicts = [x for x in negative_filtered_dicts if not ('Contig' == x.get('assembly_level'))]

print("Filtered RefSeq summary")


# Create dict of output filename and RefSeq assembly URL
download_urls = []
for line in filtered_dicts:
    url_dict = {}
    if len(line.get('infraspecific_name')) != 0:
        clean_name = str(line['organism_name'] + " " + line['infraspecific_name'].split("=")[1]).replace(" ", "_").replace(":","-").replace("/","-")
    else:
        clean_name = str(line['organism_name'] + " " + line['asm_name']).replace(" ", "_").replace(":","-").replace("/","-")
    url = str(line['ftp_path'] + "/" + line['assembly_accession'] + "_" + line['asm_name'] + "_genomic.fna.gz").replace(" ", "_")
    url_dict['name'] = clean_name
    url_dict['url'] = url
    download_urls.append(url_dict)


# Download gzip-encoded genomes, decompress on the fly and write to filename
download_urls_sorted = sorted(download_urls, key = lambda i: i['name']) 

print("Downloading " + str(len(download_urls_sorted)) + " genome assemblies...")

for line in download_urls_sorted:
    https_url = line['url'].replace("ftp://", "https://")
    print("Downloading " + line['name'] + " from " + https_url)
    if https_url.startswith("https"):
        try:
            r = requests.get(https_url, stream=True)
            path = str(line['name'] + "." + ending )
            with open(path, 'wb') as f:
                r.raw.decode_content = True  # just in case transport encoding was applied
                gzip_file = gzip.GzipFile(fileobj=r.raw)
                shutil.copyfileobj(gzip_file, f)
        except Exception:
            pass
                      
print("Reference library complete")

### THE END ###


