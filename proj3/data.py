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
    "year": "YEAR OF STOP (CCYY)",
    "pct": "PRECINCT OF STOP (FROM 1 TO 123)",
    "ser_num": "UF250 SERIAL NUMBER",
    "datestop": "DATE OF STOP (MM-DD-YYYY)",
    "timestop": "TIME OF STOP (HH:MM)",
    "recstat": "RECORD STATUS",
    "inout": "WAS STOP INSIDE OR OUTSIDE ?",
    "trhsloc": "WAS LOCATION HOUSING OR TRANSIT AUTHORITY ?",
    "perobs": "PERIOD OF OBSERVATION (MMM)",
    "crimsusp": "CRIME SUSPECTED",
    "perstop": "PERIOD OF STOP (MMM)",
    "typeofid": "STOPPED PERSON'S IDENTIFICATION TYPE",
    "explnstp": "DID OFFICER EXPLAIN REASON FOR STOP ?",
    "othpers": "WERE OTHER PERSONS STOPPED, QUESTIONED OR FRISKED ?",
    "arstmade": "WAS AN ARREST MADE ?",
    "arstoffn": "OFFENSE SUSPECT ARRESTED FOR",
    "sumissue": "WAS A SUMMONS ISSUED ?",
    "sumoffen": "OFFENSE SUSPECT WAS SUMMONSED FOR",
    "compyear": "COMPLAINT YEAR (IF COMPLAINT REPORT PREPARED)",
    "comppct": "COMPLAINT PRECINCT (IF COMPLAINT REPORT PREPARED)",
    "offunif": "WAS OFFICER IN UNIFORM ?",
    "officrid": "ID CARD PROVIDED BY OFFICER (IF NOT IN UNIFORM)",
    "frisked": "WAS SUSPECT FRISKED ?",
    "searched": "WAS SUSPECT SEARCHED ?",
    "contrabn": "WAS CONTRABAND FOUND ON SUSPECT ?",
    "adtlrept": "WERE ADDITIONAL REPORTS PREPARED ?",
    "pistol": "WAS A PISTOL FOUND ON SUSPECT ?",
    "riflshot": "WAS A RIFLE FOUND ON SUSPECT ?",
    "asltweap": "WAS AN ASSAULT WEAPON FOUND ON SUSPECT ?",
    "knifcuti": "WAS A KNIFE OR CUTTING INSTRUMENT FOUND ON SUSPECT ?",
    "machgun": "WAS A MACHINE GUN FOUND ON SUSPECT ?",
    "othrweap": "WAS ANOTHER TYPE OF WEAPON FOUND ON SUSPECT",
    "pf_hands": "PHYSICAL FORCE USED BY OFFICER - HANDS",
    "pf_wall": "PHYSICAL FORCE USED BY OFFICER - SUSPECT ON GROUND",
    "pf_grnd": "PHYSICAL FORCE USED BY OFFICER - SUSPECT AGAINST WALL",
    "pf_drwep": "PHYSICAL FORCE USED BY OFFICER - WEAPON DRAWN",
    "pf_ptwep": "PHYSICAL FORCE USED BY OFFICER - WEAPON POINTED",
    "pf_baton": "PHYSICAL FORCE USED BY OFFICER - BATON",
    "pf_hcuff": "PHYSICAL FORCE USED BY OFFICER - HANDCUFFS",
    "pf_pepsp": "PHYSICAL FORCE USED BY OFFICER - PEPPER SPRAY",
    "pf_other": "PHYSICAL FORCE USED BY OFFICER - OTHER",
    "radio": "RADIO RUN",
    "ac_rept": "ADDITIONAL CIRCUMSTANCES - REPORT BY VICTIM/WITNESS/OFFICER",
    "ac_inves": "ADDITIONAL CIRCUMSTANCES - ONGOING INVESTIGATION",
    "rf_vcrim": "REASON FOR FRISK - VIOLENT CRIME SUSPECTED",
    "rf_othsw": "REASON FOR FRISK - OTHER SUSPICION OF WEAPONS",
    "ac_proxm": "ADDITIONAL CIRCUMSTANCES - PROXIMITY TO SCENE OF OFFENSE",
    "rf_attir": "REASON FOR FRISK - INAPPROPRIATE ATTIRE FOR SEASON",
    "cs_objcs": "REASON FOR STOP - CARRYING SUSPICIOUS OBJECT",
    "cs_descr": "REASON FOR STOP - FITS A RELEVANT DESCRIPTION",
    "cs_casng": "REASON FOR STOP - CASING A VICTIM OR LOCATION",
    "cs_lkout": "REASON FOR STOP - SUSPECT ACTING AS A LOOKOUT",
    "rf_vcact": "REASON FOR FRISK-  ACTIONS OF ENGAGING IN A VIOLENT CRIME",
    "cs_cloth": "REASON FOR STOP - WEARING CLOTHES COMMONLY USED IN A CRIME",
    "cs_drgtr": "REASON FOR STOP - ACTIONS INDICATIVE OF A DRUG TRANSACTION",
    "ac_evasv": "ADDITIONAL CIRCUMSTANCES - EVASIVE RESPONSE TO QUESTIONING",
    "ac_assoc": "ADDITIONAL CIRCUMSTANCES - ASSOCIATING WITH KNOWN CRIMINALS",
    "cs_furtv": "REASON FOR STOP - FURTIVE MOVEMENTS",
    "rf_rfcmp": "REASON FOR FRISK - REFUSE TO COMPLY W OFFICER'S DIRECTIONS",
    "ac_cgdir": "ADDITIONAL CIRCUMSTANCES - CHANGE DIRECTION AT SIGHT OF OFFICER",
    "rf_verbl": "REASON FOR FRISK - VERBAL THREATS BY SUSPECT",
    "cs_vcrim": "REASON FOR STOP - ACTIONS OF ENGAGING IN A VIOLENT CRIME",
    "cs_bulge": "REASON FOR STOP - SUSPICIOUS BULGE",
    "cs_other": "REASON FOR STOP - OTHER",
    "ac_incid": "ADDITIONAL CIRCUMSTANCES - AREA HAS HIGH CRIME INCIDENCE",
    "ac_time": "ADDITIONAL CIRCUMSTANCES - TIME OF DAY FITS CRIME INCIDENCE",
    "rf_knowl": "REASON FOR FRISK - KNOWLEDGE OF SUSPECT'S PRIOR CRIM BEHAV",
    "ac_stsnd": "ADDITIONAL CIRCUMSTANCES - SIGHTS OR SOUNDS OF CRIMINAL ACTIVITY",
    "ac_other": "ADDITIONAL CIRCUMSTANCES - OTHER",
    "sb_hdobj": "BASIS OF SEARCH - HARD OBJECT",
    "sb_outln": "BASIS OF SEARCH - OUTLINE OF WEAPON",
    "sb_admis": "BASIS OF SEARCH - ADMISSION BY SUSPECT",
    "sb_other": "BASIS OF SEARCH - OTHER",
    "repcmd": "REPORTING OFFICER'S COMMAND (1 TO 999)",
    "revcmd": "REVIEWING OFFICER'S COMMAND (1 TO 999)",
    "rf_furt": "REASON FOR FRISK - FURTIVE MOVEMENTS",
    "rf_bulg": "REASON FOR FRISK - SUSPICIOUS BULGE",
    "offverb": "VERBAL STATEMENT PROVIDED BY OFFICER (IF NOT IN UNIFORM)",
    "offshld": "SHIELD PROVIDED BY OFFICER (IF NOT IN UNIFORM)",
    "sex": "SUSPECT'S SEX",
    "race": "SUSPECT'S RACE",
    "dob": "SUSPECT'S DATE OF BIRTH (CCYY-MM-DD)",
    "age": "SUSPECT'S AGE",
    "ht_feet": "SUSPECT'S HEIGHT (FEET)",
    "ht_inch": "SUSPECT'S HEIGHT (INCHES)",
    "weight": "SUSPECT'S WEIGHT",
    "haircolr": "SUSPECT'S HAIRCOLOR",
    "eyecolor": "SUSPECT'S EYE COLOR",
    "build": "SUSPECT'S BUILD",
    "othfeatr": "SUSPECT'S OTHER FEATURES (SCARS, TATOOS ETC.)",
    "addrtyp": "PERSON STOP HOME ADDRESS TYPE",
    "rescode": "LOCATION OF STOP RESIDENT CODE",
    "premtype": "LOCATION OF STOP PREMISE TYPE",
    "premname": "LOCATION OF STOP PREMISE NAME",
    "addrnum": "LOCATION OF STOP ADDRESS NUMBER",
    "stname": "LOCATION OF STOP STREET NAME",
    "stinter": "LOCATION OF STOP INTERSECTION",
    "crossst": "LOCATION OF STOP CROSS STREET",
    "aptnum": "LOCATION OF STOP APT NUMBER",
    "city": "LOCATION OF STOP CITY",
    "state": "LOCATION OF STOP STATE",
    "zip": "LOCATION OF STOP ZIP CODE",
    "addrpct": "LOCATION OF STOP ADDRESS PRECINCT",
    "sector": "LOCATION OF STOP SECTOR",
    "beat": "LOCATION OF STOP BEAT",
    "post": "LOCATION OF STOP POST",
    "xcoord": "LOCATION OF STOP X COORD",
    "ycoord": "LOCATION OF STOP Y COORD",
    "dettypCM": "DETAILS TYPES CODE",
    "lineCM": "COUNT >1 ADDITIONAL DETAILS",
    "detailCM": "CRIME CODE DESCRIPTION",
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

