# !/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Filename: dm3reader.py

################################################################################
## Python script for parsing GATAN DM3 (DigitalMicrograph) files
## and extracting various metadata
## --
## warning: *tested on single-image files only*
## --
## based on the DM3_Reader plug-in (v 1.3.4) for ImageJ by Greg Jefferis <jefferis@stanford.edu>
## http://rsb.info.nih.gov/ij/plugins/DM3_Reader.html
## --
## Python adaptation: Pierre-Ivan Raynal <raynal@med.univ-tours.fr>
## http://microscopies.med.univ-tours.fr/
################################################################################


"""
modified by Todd Nicholson, University of Illinois, Coordinated Sciences Lab.

"""
import sys, struct, os
import json
import chardet
import tempfile
import collections

version = '0.72'

## constants for encoded data types ##

SHORT = 2
LONG = 3
USHORT = 4
ULONG = 5
FLOAT = 6
DOUBLE = 7
BOOLEAN = 8
CHAR = 9
OCTET = 10
STRUCT = 15
STRING = 18
ARRAY = 20

## END constants ##


debugLevel = 0  # 0=none, 1-3=basic, 4-5=simple, 6-10 verbose

# chosenImage = 1
#
# IMGLIST = "root.ImageList."
# OBJLIST = "root.DocumentObjectList."


### initialize variables ###
f = ''
# track currently read group
MAXDEPTH = 64
curGroupLevel = -1
curGroupAtLevelX = [0 for x in range(MAXDEPTH)]
curGroupNameAtLevelX = ["" for x in range(MAXDEPTH)]
# track current tag
curTagAtLevelX = ["" for x in range(MAXDEPTH)]
curTagName = ""
storedTags = []
tagHash = {}


### END init. variables ###


### sub-routines ###

## reading n bytes functions
def readLong(file):
    '''Read 4 bytes as integer in file'''
    read_bytes = file.read(4)
    return struct.unpack('>l', read_bytes)[0]


def readShort(file):
    '''Read 2 bytes as integer in file'''
    read_bytes = file.read(2)
    return struct.unpack('>h', read_bytes)[0]


def readByte(file):
    '''Read 1 byte as integer in file'''
    read_bytes = file.read(1)
    return struct.unpack('>b', read_bytes)[0]


def readChar(file):
    '''Read 1 byte as char in file'''
    read_bytes = file.read(1)
    return struct.unpack('c', read_bytes)[0]


def readString(file, len=1):
    '''Read len bytes as a string in file'''
    read_bytes = file.read(len)
    str_fmt = '>' + str(len) + 's'
    return struct.unpack(str_fmt, read_bytes)[0]


def readLEShort(file):
    '''Read 2 bytes as *little endian* integer in file'''
    read_bytes = file.read(2)
    return struct.unpack('<h', read_bytes)[0]


def readLELong(file):
    '''Read 4 bytes as *little endian* integer in file'''
    read_bytes = file.read(4)
    return struct.unpack('<l', read_bytes)[0]


def readLEUShort(file):
    '''Read 2 bytes as *little endian* unsigned integer in file'''
    read_bytes = file.read(2)
    return struct.unpack('<H', read_bytes)[0]


def readLEULong(file):
    '''Read 4 bytes as *little endian* unsigned integer in file'''
    read_bytes = file.read(4)
    return struct.unpack('<L', read_bytes)[0]


def readLEFloat(file):
    '''Read 4 bytes as *little endian* float in file'''
    read_bytes = file.read(4)
    return struct.unpack('<f', read_bytes)[0]


def readLEDouble(file):
    '''Read 8 bytes as *little endian* double in file'''
    read_bytes = file.read(8)
    return struct.unpack('<d', read_bytes)[0]


## utility functions
def makeGroupString():
    global curGroupLevel, curGroupAtLevelX

    tString = curGroupAtLevelX[0]
    for i in range(1, curGroupLevel + 1):
        tString += "." + curGroupAtLevelX[i]
    return tString


def makeGroupNameString():
    global curGroupLevel, curGroupNameAtLevelX

    tString = curGroupNameAtLevelX[0]
    for i in range(1, curGroupLevel + 1):
        tString += "." + str(curGroupNameAtLevelX[i])

    return tString


def readTagGroup():
    global curGroupLevel, curGroupAtLevelX, curTagAtLevelX

    # go down a level
    curGroupLevel += 1
    # increment group counter
    curGroupAtLevelX[curGroupLevel] += 1
    # set number of current tag to -1 --- readTagEntry() pre-increments => first gets 0
    curTagAtLevelX[curGroupLevel] = -1

    if (debugLevel > 5):
        print "rTG: Current Group Level:", curGroupLevel

    # is the group sorted?
    sorted = readByte(f)
    if (sorted == 1):
        isSorted = True
    else:
        isSorted = False

    # is the group open?
    open = readByte(f)
    if (open == 1):
        isOpen = True
    else:
        isOpen = False

    # number of Tags
    nTags = readLong(f)

    if (debugLevel > 5):
        print "rTG: Iterating over the", nTags, "tag entries in this group"

    # read Tags
    for i in range(nTags):
        readTagEntry()

    # go back up one level as reading group is finished
    curGroupLevel += -1

    return 1


def readTagEntry():
    global curGroupLevel, curGroupAtLevelX, curTagAtLevelX, curTagName

    # is data or a new group?
    data = readByte(f)
    if (data == 21):
        isData = True
    else:
        isData = False

    curTagAtLevelX[curGroupLevel] += 1

    # get tag label if exists
    lenTagLabel = readShort(f)

    if (lenTagLabel != 0):
        tagLabel = readString(f, lenTagLabel)
    else:
        tagLabel = str(curTagAtLevelX[curGroupLevel])

    if (debugLevel > 5):
        print str(curGroupLevel) + "|" + makeGroupString() + ": Tag label = " + tagLabel
    elif (debugLevel > 0):
        print str(curGroupLevel) + ": Tag label = " + tagLabel

    if isData:
        # give it a name
        curTagName = makeGroupNameString() + "." + tagLabel
        # read it
        readTagType()
    else:
        # it is a tag group
        curGroupNameAtLevelX[curGroupLevel + 1] = tagLabel
        readTagGroup()  # increments curGroupLevel

    return 1


def readTagType():
    delim = readString(f, 4)
    if (delim != "%%%%"):
        print hex(f.tell()) + ": Tag Type delimiter not %%%%"
        sys.exit()

    nInTag = readLong(f)

    readAnyData()

    return 1


def encodedTypeSize(eT):
    # returns the size in bytes of the data type

    width = -1;  # returns -1 for unrecognised types

    if eT == 0:
        width = 0
    elif ((eT == BOOLEAN) or (eT == CHAR) or (eT == OCTET)):
        width = 1
    elif ((eT == SHORT) or (eT == USHORT)):
        width = 2
    elif ((eT == LONG) or (eT == ULONG) or (eT == FLOAT)):
        width = 4
    elif (eT == DOUBLE):
        width = 8

    return width


def readAnyData():
    ## higher level function dispatching to handling data types to other functions

    # get Type category (short, long, array...)
    encodedType = readLong(f)
    # calc size of encodedType
    etSize = encodedTypeSize(encodedType)

    if (debugLevel > 5):
        print "rAnD, " + hex(f.tell()) + ": Tag Type = " + str(encodedType) + ", Tag Size = " + str(etSize)

    if (etSize > 0):
        storeTag(curTagName, readNativeData(encodedType, etSize))
    elif (encodedType == STRING):
        stringSize = readLong(f)
        readStringData(stringSize)
    elif (encodedType == STRUCT):
        # does not store tags yet
        structTypes = readStructTypes()
        readStructData(structTypes)
    elif (encodedType == ARRAY):
        # does not store tags yet
        # indicates size of skipped data blocks
        arrayTypes = readArrayTypes()
        readArrayData(arrayTypes)
    else:
        print "rAnD, " + hex(f.tell()) + ": Can't understand encoded type"
        sys.exit()

    return 1


def readNativeData(encodedType, etSize):
    # reads ordinary data types

    if (encodedType == SHORT):
        val = readLEShort(f)
    elif (encodedType == LONG):
        val = readLELong(f)
    elif (encodedType == USHORT):
        val = readLEUShort(f)
    elif (encodedType == ULONG):
        val = readLEULong(f)
    elif (encodedType == FLOAT):
        val = readLEFloat(f)
    elif (encodedType == DOUBLE):
        val = readLEDouble(f)
    elif (encodedType == BOOLEAN):
        bool = readByte(f)
        if bool == 0:
            val = False
        else:
            val = True
    elif (encodedType == CHAR):
        val = readChar(f)
    elif (encodedType == OCTET):
        val = readChar(f)  # difference with char???
    else:
        print "rND, " + hex(f.tell()) + ": Unknown data type " + str(encodedType)
        sys.exit()

    if (debugLevel > 3):
        print "rND, " + hex(f.tell()) + ": " + str(val)
    elif (debugLevel > 0):
        print val

    return val


def readStringData(stringSize):
    # reads string data
    if (stringSize <= 0):
        rString = ""
    else:
        if (debugLevel > 3):
            print "rSD @ " + str(f.tell()) + "/" + hex(f.tell()) + " :",

        ## !!! *Unicode* string... convert to latin-1 string
        rString = readString(f, stringSize)
        rString = unicode(rString, "utf_16_le").encode("latin1", "replace")

        if (debugLevel > 3):
            print rString + "   <" + repr(rString) + ">"

    if (debugLevel > 0):
        print "StringVal:", rString

    storeTag(curTagName, rString)

    return rString


def readArrayTypes():
    # determines the data types in an array data type
    arrayType = readLong(f)

    itemTypes = []
    if (arrayType == STRUCT):
        itemTypes = readStructTypes()
    elif (arrayType == ARRAY):
        itemTypes = readArrayTypes()
    else:
        itemTypes.append(arrayType)

    return itemTypes


def readArrayData(arrayTypes):
    # reads array data

    arraySize = readLong(f)

    if (debugLevel > 3):
        print "rArD, " + hex(f.tell()) + ": Reading array of size = " + str(arraySize)

    itemSize = 0
    encodedType = 0

    for i in range(len(arrayTypes)):
        encodedType = int(arrayTypes[i])
        etSize = encodedTypeSize(encodedType)
        itemSize += etSize
        if (debugLevel > 5):
            print "rArD: Tag Type = " + str(encodedType) + ", Tag Size = " + str(etSize)
        ##! readNativeData( encodedType, etSize ) !##

    if (debugLevel > 5):
        print "rArD: Array Item Size = " + str(itemSize)

    bufSize = arraySize * itemSize

    if ((not curTagName.endswith("ImageData.Data"))
        and (len(arrayTypes) == 1)
        and (encodedType == USHORT)
        and (arraySize < 256)):
        # treat as string
        val = readStringData(bufSize)
    else:
        # treat as binary data
        # - store data size and offset as tags
        storeTag(curTagName + ".Size", bufSize)
        storeTag(curTagName + ".Offset", f.tell())
        # - skip data w/o reading
        f.seek(f.tell() + bufSize)

    return 1


def readStructTypes():
    # analyses data types in a struct

    if (debugLevel > 3):
        print "Reading Struct Types at Pos = " + hex(f.tell())

    structNameLength = readLong(f)
    nFields = readLong(f)

    if (debugLevel > 5):
        print "nFields = ", nFields

    if (nFields > 100):
        print hex(f.tell()), "Too many fields"
        sys.exit()

    fieldTypes = []
    nameLength = 0
    for i in range(nFields):
        nameLength = readLong(f)
        if (debugLevel > 9):
            print i + "th namelength = " + nameLength
        fieldType = readLong(f)
        fieldTypes.append(fieldType)

    return fieldTypes


def readStructData(structTypes):
    # reads struct data based on type info in structType
    for i in range(len(structTypes)):
        encodedType = structTypes[i]
        etSize = encodedTypeSize(encodedType)

        if (debugLevel > 5):
            print "Tag Type = " + str(encodedType) + ", Tag Size = " + str(etSize)

        # get data
        readNativeData(encodedType, etSize)

    return 1


def storeTag(tagName, tagValue):
    global storedTags, tagHash

    storedTags.append(str(tagName) + " = " + str(tagValue))
    tagHash[str(tagName)] = str(tagValue)


### END sub-routines ###



### parse DM3 file ###
def parseDM3(filename, dump=False):
    '''Function parses DM3 file and returns dict with extracted Tags.
    Dumps Tags in a txt file if 'dump' set to 'True'.'''

    global f

    try:
        print "Accessing file... "
        f = open(filename, 'rb')
        isDM3 = True
        isDM4 = True
        ## read header (first 3 4-byte int)
        # get version
        fileVersion = readLong(f)
        if (fileVersion != 3):
            isDM3 = False
        if (fileVersion != 4):
            isDM4 = False
        # get indicated file size
        FileSize = readLong(f)
        # get byte-ordering
        lE = readLong(f)
        if (lE == 1):
            littleEndian = True
        else:
            littleEndian = False
            isDM3 = False
        # check file header, raise Exception if not DM3
        if ((not (isDM3 and littleEndian)) and (not (isDM4 ))):
            raise NameError("Is_Not_a_DM3_File")

        if (debugLevel > 5):
            print "Header info.:"
            print "File version:", version
            print "lE:", lE
            print "File size:", FileSize

        print '%s appears to be a DM3 or DM4 file' % filename,

        # set name of root group (contains all data)...
        curGroupNameAtLevelX[0] = "root"
        # ... then read it
        global storedTags, tagHash
        storedTags = []
        tagHash = {}
        readTagGroup()

        f.close()

        print "--", len(storedTags), "Tags read"

        # dump Tags in txt file if requested
        if dump:
            dump_file = filename + ".dump.txt"
            try:
                log = open(dump_file, 'w')
            except:
                print "Error -- could not access output file."
                sys.exit()
            for tag in storedTags:
                log.write(tag + "\n")
            log.close

        # return Tag list
        return tagHash

    except IOError:
        print "Error -- cannot access data file. Termfinating."
        sys.exit()
    except NameError:
        print '%s does not appear to be a DM3 file.' % filename
        return 0
    except:
        print '\n Could not parse %s as a DM3 file' % filename
        return 0


def getDM3FileInfo(dm3_file, makePGMtn=False, tn_file='dm3tn_temp.pgm'):
    '''Extracts useful experiment info from DM3 file and
    exports thumbnail to a PGM file if 'makePGMtn' set to 'True'.'''

    # define useful information
    info_keys = {
        'descrip': 'root.ImageList.1.Description',
        'acq_date': 'root.ImageList.1.ImageTags.DataBar.Acquisition Date',
        'acq_time': 'root.ImageList.1.ImageTags.DataBar.Acquisition Time',
        'name': 'root.ImageList.1.ImageTags.Microscope Info.Name',
        'micro': 'root.ImageList.1.ImageTags.Microscope Info.Microscope',
        'hv': 'root.ImageList.1.ImageTags.Microscope Info.Voltage',
        'mag': 'root.ImageList.1.ImageTags.Microscope Info.Indicated Magnification',
        'mode': 'root.ImageList.1.ImageTags.Microscope Info.Operation Mode',
        'operator': 'root.ImageList.1.ImageTags.Microscope Info.Operator',
        'specimen': 'root.ImageList.1.ImageTags.Microscope Info.Specimen',
        #		'image_notes': 'root.DocumentObjectList.10.Text' # = Image Notes
    }

    # parse DM3 file
    tags = parseDM3(dm3_file, dump=False)

    # if OK, extract Tags [and thumbnail]
    if tags:
        if makePGMtn:
            # get thumbnail
            tn_size = int(tags['root.ImageList.0.ImageData.Data.Size'])
            tn_offset = int(tags['root.ImageList.0.ImageData.Data.Offset'])
            tn_width = int(tags['root.ImageList.0.ImageData.Dimensions.0'])
            tn_height = int(tags['root.ImageList.0.ImageData.Dimensions.1'])

            if (debugLevel > 0):
                print "tn data in", dm3_file, "starts at", hex(tn_offset)
                print "tn dimension:", tn_width, "x", tn_height

            if ((tn_width * tn_height * 4) != tn_size):
                print "Error: cannot extract thumbnail from", dm3_file
                sys.exit()

            # access DM3 file
            try:
                dm3 = open(dm3_file, 'rb')
            except:
                print "Error accessing DM3 file"
                sys.exit()

            # open PGM file
            try:
                pgm_file = open(tn_file, 'w')
            except:
                print 'Error creating PGM output file!'
                sys.exit()

            # build plain PGM file header
            pgm_file.write("P2 " + str(tn_width) + " " + str(tn_height) + " 255\n")

            # read tn image data
            dm3.seek(tn_offset)
            for i in range(tn_height):
                for ii in range(tn_width):
                    data_bytes = dm3.read(4)
                    pgm_data = struct.unpack('<L', data_bytes)[0]
                    pgm_data = int(pgm_data / 65536)
                    pgm_file.write(str(pgm_data) + ' ')
                pgm_file.write("\n")

            pgm_file.close()
            dm3.close()

        # store experiment information
        infoHash = {}
        for key, tag in info_keys.items():
            if tags.has_key(tag):
                infoHash[key] = tags[tag]

        return infoHash
    # else, return false value
    else:
        return 0


def make_pgm_tempfile(dm3_file):
    dm3 = None
    tags = parseDM3(dm3_file)
    (fd, tn_file) = tempfile.mkstemp(suffix=".pgm")
    os.close(fd)
    tn_size = int(tags['root.ImageList.0.ImageData.Data.Size'])
    tn_offset = int(tags['root.ImageList.0.ImageData.Data.Offset'])
    tn_width = int(tags['root.ImageList.0.ImageData.Dimensions.0'])
    tn_height = int(tags['root.ImageList.0.ImageData.Dimensions.1'])

    if (debugLevel > 0):
        print "tn data in", dm3_file, "starts at", hex(tn_offset)
        print "tn dimension:", tn_width, "x", tn_height

    if ((tn_width * tn_height * 4) != tn_size):
        print "Error: cannot extract thumbnail from", dm3_file
        sys.exit()

    # access DM3 file
    try:
        dm3 = open(dm3_file, 'rb')
    except:
        print "Error accessing DM3 file"
        sys.exit()

    # open PGM file
    try:
        pgm_file = open(tn_file, 'w')
    except:
        print 'Error creating PGM output file!'
        sys.exit()

    # build plain PGM file header
    pgm_file.write("P2 " + str(tn_width) + " " + str(tn_height) + " 255\n")

    # read tn image data
    dm3.seek(tn_offset)
    for i in range(tn_height):
        for ii in range(tn_width):
            data_bytes = dm3.read(4)
            pgm_data = struct.unpack('<L', data_bytes)[0]
            pgm_data = int(pgm_data / 65536)
            pgm_file.write(str(pgm_data) + ' ')
        pgm_file.write("\n")

    pgm_file.close()
    dm3.close()
    return tn_file


def make_pgm(dm3_file, tn_file='dm3tn_temp.pgm', **tags):
    tn_size = int(tags['root_ImageList_0_ImageData_Data_Size'])
    tn_offset = int(tags['root_ImageList_0_ImageData_Data_Offset'])
    tn_width = int(tags['root_ImageList_0_ImageData_Dimensions_0'])
    tn_height = int(tags['root_ImageList_0_ImageData_Dimensions_1'])

    if (debugLevel > 0):
        print "tn data in", dm3_file, "starts at", hex(tn_offset)
        print "tn dimension:", tn_width, "x", tn_height

    if ((tn_width * tn_height * 4) != tn_size):
        print "Error: cannot extract thumbnail from", dm3_file
        sys.exit()

    # access DM3 file
    try:
        dm3 = open(dm3_file, 'rb')
    except:
        print "Error accessing DM3 file"
        sys.exit()

    # open PGM file
    try:
        pgm_file = open(tn_file, 'w')
    except:
        print 'Error creating PGM output file!'
        sys.exit()

    # build plain PGM file header
    pgm_file.write("P2 " + str(tn_width) + " " + str(tn_height) + " 255\n")

    # read tn image data
    dm3.seek(tn_offset)
    for i in range(tn_height):
        for ii in range(tn_width):
            data_bytes = dm3.read(4)
            pgm_data = struct.unpack('<L', data_bytes)[0]
            pgm_data = int(pgm_data / 65536)
            pgm_file.write(str(pgm_data) + ' ')
        pgm_file.write("\n")

    pgm_file.close()
    dm3.close()
    return pgm_file

#below are methods added by Todd Nicholson, CSL, 2015 - 2016

def convert_encoding(data, new_encoding="UTF-8"):
    if data is None or data == "":
        return "EMPTY"
    current_encoding = chardet.detect(data)['encoding']
    if type(current_encoding) is None:
        print("is none")
    if new_encoding.upper() != current_encoding.upper():
        data = data.decode(current_encoding).encode("UTF-8")

    return data


def replace_periods_in_metadata(**tags):
    metadata = dict()
    keys = tags.keys()
    for old_key in keys:
        encoding = chardet.detect(old_key)['encoding']
        newKey = convert_encoding(old_key, new_encoding="UTF-8")
        newKey = newKey.replace('.', '_')

        old_value = tags[old_key]
        newValue = convert_encoding(old_value, new_encoding="UTF-8")
        metadata[newKey] = newValue
    return metadata


def fix_metadata_tags(**tags):
    metadata = dict()
    keys = tags.keys()
    for old_key in keys:
        encoding = chardet.detect(old_key)['encoding']
        newKey = convert_encoding(old_key, new_encoding="UTF-8")
        newKey = newKey.replace('.', ' ')
        newKey = newKey.replace('root ', '')
        newKey = newKey.replace('ImageList 0', '')
        newKey = newKey.replace('ImageList 1', '')
        newKey = newKey.replace('ImageTags', '')
        newKey = newKey.replace('ImageData', '')
        newKey = newKey.replace('DocumentObjectList 0', '')
        newKey = newKey.replace('DocumentObjectList 1', '')
        # need to handle encoding

        old_value = tags[old_key]
        newValue = convert_encoding(old_value, new_encoding="UTF-8")
        metadata[newKey] = newValue
    return metadata

def keyMatch(currentString, key):
    key_list = key.split(' ')
    contains_all = True
    for each in key_list:
        if each not in currentString:
            contains_all = False

    return contains_all

#tags should be fixed - no periods, underscores, and trimmed
def get_metadata_shortlist(**tags):
    #need more research on the top 10 fields and what counts

    """
    Beam Voltage
    Beam Current
    Spot Size
    Alpha
    Magnification/camera length
    Condenser Aperture
    Objective Aperture
    Dark/bright filed
    Exposure
    Binning
    Specimen

    """

    new_shorlist_keys = ['beam','voltage','current','spot','alpha','magnification','camera length','condenser',
                         'aperture','objective','dark','bright','exposure','binning','specimin']

    shortlist_keys = ['actual magnification', 'emission current', 'illumination mode', 'imaging mode',
                      'magnification interpolated', 'microscope info microscope', 'operation mode',
                      'indicated magnification','voltage']
    keys = tags.keys()
    short_metadata = dict()
    for key in keys:
        lower_key = key.lower()
        for each in shortlist_keys:
            if each in lower_key:
                #new_key = convert_encoding(key,new_encoding="UTF-8")
                old_value = tags[key]
                new_value = convert_encoding(old_value,new_encoding="UTF-8")
                short_metadata[key] = new_value
    return short_metadata

def sortMetadataByRelevance(**tags):
    top_demand_keys = ['beam','voltage','current','spot','alpha','magnification','camera length','condenser',
                         'aperture','objective','dark','bright','exposure','binning','specimin']
    top_tags = dict()
    keys = tags.keys()
    for key in keys:
        lowercase_key = key.lower()
        for each in top_demand_keys:
            if each in lowercase_key:
                old_value = tags[key]
                new_value = convert_encoding(old_value,new_encoding="UTF-8")
                top_tags[key] = new_value
    new_tags = collections.OrderedDict()
    top_keys = top_tags.keys()
    if (bool(top_tags) == True):
        for key in top_keys:
            new_tags[key] = top_tags[key]
    for key in keys:
        if key not in top_keys:
            new_tags[key] = tags[key]
    return new_tags

def extract_dm3_metadata(filename, dump=False):
    tags = parseDM3(filename)
    tags = fix_metadata_tags(**tags)
    tags = sortMetadataByRelevance(**tags)
    return tags


### END dm3reader.py
