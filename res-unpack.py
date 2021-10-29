"""
RES-File Unpacker
by Sebastian Schiwietz

Extracts files contained in resource files (.res)

FILE FORMAT:
Byte order is Little Endian.

4 Bytes   Number of files contained
8 Bytes   ? (Probably some sort of signature and/or unused parts)

List of:
4 Bytes   Index of filename
4 Bytes   Length of filename

List of:
x Bytes   Filename
4 Bytes   Index of file
4 Bytes   Length of file
"""

def save_file(filename, filedata):
    try:
        newfile = open(filename, 'wb')
        newfile.write(filedata)
        newfile.close()
    except:
        print("Error writing file.")


file_nr = 0         # Number of files
data = bytearray()  # File data

print("RES File Extractor")
res = input("Filename: ")
try:
    f = open(res, 'rb') # read binary
    data = bytearray(f.read())
except:
    print("Error loading/reading file.")
else:
    print("Reading file successful.")

# Check for "signature byte"
if data[6] == 0x53:
    print("Signature found.")

    # Get the number of contained files
    # First two bytes [0:2] are sufficient, reading 4 bytes leads to issues in one case
    file_nr = int.from_bytes(data[0:2], byteorder='little', signed=False)
    print(str(file_nr) + " files.")

    # Finding and extracting all the files
    start = 12 # 4+8 bytes in the header

    for i in range(file_nr):
        # Get filename
        print("")
        index = int.from_bytes(data[start:start+4], byteorder='little', signed=False)
        #length = int.from_bytes(data[start+4:start+8], byteorder='little', signed=False)
        length = int.from_bytes(data[start+4:start+6], byteorder='little', signed=False)
        # Some trash(?) in the 2 higher bytes leads to extremely large filename sizes
        # with bigger integers (32 or higher). Therefore only use the first 2 bytes.
        print(str(hex(index)) + " " + str(length))
        try:
            fname = data[index:index+length].decode()
        except:
            fname = str(i) + ".fix"
        print(fname)

        # Get index and length of actual file
        tmp = index + length # Index of data after (variable size) filename
        find = int.from_bytes(data[tmp:tmp+4], byteorder='little', signed=False)
        print("At " + str(hex(find)))
        flen = int.from_bytes(data[tmp+4:tmp+8], byteorder='little', signed=False)
        print(str(flen) + " bytes.")

        save_file(fname, data[find:find+flen])
        start += 8
    
else:
    print("No signature found.")

print("Done.")
