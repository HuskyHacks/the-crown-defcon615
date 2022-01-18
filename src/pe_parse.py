import pefile

import pefile
pe = pefile.PE("/home/husky/Desktop/the-crown-defcon615/samples/helloworld/helloworld.exe")

# print(pe.dump_info())

pe.print_info()


for entry in pe.OPTIONAL_HEADER.DATA_DIRECTORY:
    print(entry.name + "\n|\n|---- Size : " + str(entry.Size) + "\n|\n|---- VirutalAddress : " + hex(entry.VirtualAddress) +'\n')

print(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
print(pe.OPTIONAL_HEADER.ImageBase)
print(pe.FILE_HEADER.NumberOfSections)

for section in pe.sections:
  print(section.Name, hex(section.VirtualAddress),
    hex(section.Misc_VirtualSize), section.SizeOfRawData )

pe.parse_data_directories()

for entry in pe.DIRECTORY_ENTRY_IMPORT:
    for imp in entry.imports:
        imp_name = imp.name.decode("utf-8").strip()
        print(imp_name)


for entry in pe.DIRECTORY_ENTRY_IMPORT:
    dll_name = entry.dll.decode('utf-8')
    if dll_name == "KERNEL32.dll":
        print("[*] Kernel32.dll imports:")
        for func in entry.imports:
            print("\t%s at 0x%08x" % (func.name.decode('utf-8'), func.address))

