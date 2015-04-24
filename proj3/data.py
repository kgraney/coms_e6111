from collections import defaultdict
import copy
import csv
import gzip
import logging

logger = logging.getLogger(__name__)

def WriteIntegratedDataset(filename, lst):
    with gzip.open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        for row in lst:
            writer.writerow(row)

def ReadIntegratedDataset(filename):
    lst = []
    with gzip.open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            lst.append(row)
    return lst

expanded_names =  {
    "year": "Year Of Stop (Ccyy)",
    "pct": "Precinct Of Stop (From 1 To 123)",
    "ser_num": "Uf250 Serial Number",
    "datestop": "Date Of Stop (Mm-Dd-Yyyy)",
    "timestop": "Time Of Stop (Hh:Mm)",
    "recstat": "Record Status",
    "inout": "Was Stop Inside Or Outside ?",
    "trhsloc": "Was Location Housing Or Transit Authority ?",
    "perobs": "Period Of Observation (Mmm)",
    "crimsusp": "Crime Suspected",
    "perstop": "Period Of Stop (Mmm)",
    "typeofid": "Stopped Person'S Identification Type",
    "explnstp": "Officer Explained Reason For Stop",
    "othpers": "Other Persons Stopped, Questioned Or Frisked",
    "arstmade": "Arrest Made",
    "arstoffn": "Offense Suspect Arrested For",
    "sumissue": "Summons Issued",
    "sumoffen": "Offense Suspect Was Summonsed For",
    "compyear": "Complaint Year (If Complaint Report Prepared)",
    "comppct": "Complaint Precinct (If Complaint Report Prepared)",
    "offunif": "Officer In Uniform",
    "officrid": "Id Card Provided By Officer (If Not In Uniform)",
    "frisked": "Suspect Frisked",
    "searched": "Suspect Searched",
    "contrabn": "Contraband Found On Suspect",
    "adtlrept": "Additional Reports Prepared",
    "pistol": "Pistol Found On Suspect",
    "riflshot": "Rifle Found On Suspect",
    "asltweap": "Assault Weapon Found On Suspect",
    "knifcuti": "Knife Or Cutting Instrument Found On Suspect",
    "machgun": "Machine Gun Found On Suspect",
    "othrweap": "Other Weapon Found On Suspect",
    "pf_hands": "Physical Force Used By Officer - Hands",
    "pf_wall": "Physical Force Used By Officer - Suspect On Ground",
    "pf_grnd": "Physical Force Used By Officer - Suspect Against Wall",
    "pf_drwep": "Physical Force Used By Officer - Weapon Drawn",
    "pf_ptwep": "Physical Force Used By Officer - Weapon Pointed",
    "pf_baton": "Physical Force Used By Officer - Baton",
    "pf_hcuff": "Physical Force Used By Officer - Handcuffs",
    "pf_pepsp": "Physical Force Used By Officer - Pepper Spray",
    "pf_other": "Physical Force Used By Officer - Other",
    "radio": "Radio Run",
    "ac_rept": "Additional Circumstances - Report By Victim/Witness/Officer",
    "ac_inves": "Additional Circumstances - Ongoing Investigation",
    "rf_vcrim": "Reason For Frisk - Violent Crime Suspected",
    "rf_othsw": "Reason For Frisk - Other Suspicion Of Weapons",
    "ac_proxm": "Additional Circumstances - Proximity To Scene Of Offense",
    "rf_attir": "Reason For Frisk - Inappropriate Attire For Season",
    "cs_objcs": "Reason For Stop - Carrying Suspicious Object",
    "cs_descr": "Reason For Stop - Fits A Relevant Description",
    "cs_casng": "Reason For Stop - Casing A Victim Or Location",
    "cs_lkout": "Reason For Stop - Suspect Acting As A Lookout",
    "rf_vcact": "Reason For Frisk-  Actions Of Engaging In A Violent Crime",
    "cs_cloth": "Reason For Stop - Wearing Clothes Commonly Used In A Crime",
    "cs_drgtr": "Reason For Stop - Actions Indicative Of A Drug Transaction",
    "ac_evasv": "Additional Circumstances - Evasive Response To Questioning",
    "ac_assoc": "Additional Circumstances - Associating With Known Criminals",
    "cs_furtv": "Reason For Stop - Furtive Movements",
    "rf_rfcmp": "Reason For Frisk - Refuse To Comply W Officer'S Directions",
    "ac_cgdir": "Additional Circumstances - Change Direction At Sight Of Officer",
    "rf_verbl": "Reason For Frisk - Verbal Threats By Suspect",
    "cs_vcrim": "Reason For Stop - Actions Of Engaging In A Violent Crime",
    "cs_bulge": "Reason For Stop - Suspicious Bulge",
    "cs_other": "Reason For Stop - Other",
    "ac_incid": "Additional Circumstances - Area Has High Crime Incidence",
    "ac_time": "Additional Circumstances - Time Of Day Fits Crime Incidence",
    "rf_knowl": "Reason For Frisk - Knowledge Of Suspect'S Prior Crim Behav",
    "ac_stsnd": "Additional Circumstances - Sights Or Sounds Of Criminal Activity",
    "ac_other": "Additional Circumstances - Other",
    "sb_hdobj": "Basis Of Search - Hard Object",
    "sb_outln": "Basis Of Search - Outline Of Weapon",
    "sb_admis": "Basis Of Search - Admission By Suspect",
    "sb_other": "Basis Of Search - Other",
    "repcmd": "Reporting Officer'S Command (1 To 999)",
    "revcmd": "Reviewing Officer'S Command (1 To 999)",
    "rf_furt": "Reason For Frisk - Furtive Movements",
    "rf_bulg": "Reason For Frisk - Suspicious Bulge",
    "offverb": "Verbal Statement Provided By Officer (If Not In Uniform)",
    "offshld": "Shield Provided By Officer (If Not In Uniform)",
    "sex": "Suspect'S Sex",
    "race": "Suspect'S Race",
    "dob": "Suspect'S Date Of Birth (Ccyy-Mm-Dd)",
    "age": "Suspect'S Age",
    "ht_feet": "Suspect'S Height (Feet)",
    "ht_inch": "Suspect'S Height (Inches)",
    "weight": "Suspect'S Weight",
    "haircolr": "Suspect'S Haircolor",
    "eyecolor": "Suspect'S Eye Color",
    "build": "Suspect'S Build",
    "othfeatr": "Suspect'S Other Features (Scars, Tatoos Etc.)",
    "addrtyp": "Person Stop Home Address Type",
    "rescode": "Location Of Stop Resident Code",
    "premtype": "Location Of Stop Premise Type",
    "premname": "Location Of Stop Premise Name",
    "addrnum": "Location Of Stop Address Number",
    "stname": "Location Of Stop Street Name",
    "stinter": "Location Of Stop Intersection",
    "crossst": "Location Of Stop Cross Street",
    "aptnum": "Location Of Stop Apt Number",
    "city": "Location Of Stop City",
    "state": "Location Of Stop State",
    "zip": "Location Of Stop Zip Code",
    "addrpct": "Location Of Stop Address Precinct",
    "sector": "Location Of Stop Sector",
    "beat": "Location Of Stop Beat",
    "post": "Location Of Stop Post",
    "xcoord": "Location Of Stop X Coord",
    "ycoord": "Location Of Stop Y Coord",
    "dettypcm": "Details Types Code",
    "linecm": "Count >1 Additional Details",
    "detailcm": "Crime Code Description",
}

def ExpandName(name):
    try:
        return expanded_names[name].strip()
    except (KeyError):
        return name.strip()

def ParseFile(filename):
    integrated_dataset = []
    row_labels = None
    logger.info('Reading file %s', filename)
    with gzip.open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            transaction = []
            if row_labels is None: 
                row_labels = row
            else:
                for i, value in enumerate(row):
                    if i == 12:  # Reason for statement being taken
                        continue
                    if value == 'Y':
                        transaction.append(row_labels[i])
                    if i == 9:   # Suspected crime
                        transaction.append(value)
                    if i == 6:
                        if value == 'O': transaction.append('Outside')
                        if value == 'I': transaction.append('Inside')
                    if i == 10:
                        if value == 'H': transaction.append('Housing Authority')
                        if value == 'T': transaction.append('Transit')
                    #if i == 79:  # Gender
                    #    transaction.append(value)
                    #elif value == 'N':
                    #    transaction.append('not_' + row_labels[i])
                integrated_dataset.append([ExpandName(x) for x in transaction])
    logger.info('Finished constructing integrated dataset from %s', filename)
    return integrated_dataset


class Dataset(object):
    def __init__(self, integrated_dataset):
        self.data = integrated_dataset
        self.support = defaultdict(set)

        for trans_id, trans_lst in enumerate(self.data):
            for item in trans_lst:
                self.support[item].add(trans_id)

    def GetSupport(self, itemset):
        support_set = copy.copy(self.support[itemset[0]])
        for item in itemset[1:]:
            support_set &= self.support[item]
        return len(support_set)/float(len(self.data))

