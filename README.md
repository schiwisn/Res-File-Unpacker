# Res-File-Unpacker
Extracts files contained in certain resource files (.res)

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
