#***************************************************#
#                                                   #
#      Anubis -> MAEC XML Converter Script          #
#                                                   #
# Copyright (c) 2014 - The MITRE Corporation        #
#                                                   #
#***************************************************#

#BY USING THE ANUBIS TO MAEC SCRIPT, YOU SIGNIFY YOUR ACCEPTANCE OF THE TERMS AND 
#CONDITIONS OF USE.  IF YOU DO NOT AGREE TO THESE TERMS, DO NOT USE THE ANUBIS
#TO MAEC SCRIPT.

#For more information, please refer to the terms.txt file.

#Anubis Converter Script
#Copyright 2014, MITRE Corp
#Andrew Sillers & Ivan Kirillov, MITRE
#v0.95 - BETA
#Updated 02/24/2014 for MAEC v4.1 and CybOX v2.1

import anubis_parser as anparser
from maec.package.package import Package
import sys
import os
import traceback

#Create a MAEC output file from an Anubis input file
def create_maec(inputfile, outputfile, verbose_error_mode, stat_mode):
    stat_actions = 0

    if os.path.isfile(inputfile):    

        #Create the main parser object
        parser = anparser.parser()
        
        try:
            open_file = parser.open_file(inputfile)
            
            if not open_file:
                print('\nError: Error in parsing input file. Please check to ensure that it is valid XML and conforms to the Anbuis output schema.')
                return
            
            #Parse the file to get the actions and processes
            parser.parse_document()

            #Create the MAEC package
            package = Package(parser.generator.generate_package_id())
            
            #Add the analysis
            for subject in parser.maec_subjects:
                package.add_malware_subject(subject)
                
            ##Add all applicable actions to the bundle
            for key, value in parser.actions.items():
                for action in value:
                    stat_actions += 1
                
            ##Finally, Export the results
            package.to_xml_file(outputfile)
            
            if stat_mode:
                print '\n---- Statistics ----'
                print str(stat_actions) + ' actions converted'
                #print str(converter.stat_behaviors) + ' behaviors extracted'
        except Exception, err:
           #print('\nError: %s\n' % str(err))
           
           if verbose_error_mode or True:
                traceback.print_exc()
    else:
        print('\nError: Input file not found or inaccessible.')
        return

#Print the usage text    
def usage():
    print USAGE_TEXT
    sys.exit(1)
    
USAGE_TEXT = """
Anubis XML Output --> MAEC XML Converter Utility
v0.95 BETA // Supports MAEC v4.1 and CybOX v2.1

Usage: python anubis_to_maec.py <special arguments> -i <input anubis xml output> -o <output maec xml file>
       OR -d <directory name>

Special arguments are as follows (all are optional):
-v : verbose error mode (prints tracebacks of any errors during execution).

"""    

def main():
    verbose_error_mode = 0
    stat_mode = 0
    infilename = ''
    outfilename = ''
    directoryname = ''
    
    #Get the command-line arguments
    args = sys.argv[1:]
    
    if len(args) < 2:
        usage()
        sys.exit(1)
        
    for i in range(0,len(args)):
        if args[i] == '-v':
            verbose_error_mode = 1
        elif args[i] == '-i':
            infilename = args[i+1]
        elif args[i] == '-o':
            outfilename = args[i+1]
        elif args[i] == '-d':
            directoryname = args[i+1]
        elif args[i] == '-s':
            stat_mode = 1
    
    if directoryname != '':
        for filename in os.listdir(directoryname):
            if '.xml' not in filename:
                pass
            else:
                print filename
                outfilename = filename.rstrip('.xml') + '_anubis_maec.xml'
                create_maec(os.path.join(directoryname, filename), outfilename, verbose_error_mode, stat_mode)
    #Basic input file checking
    elif infilename != '' and outfilename != '':
        create_maec(infilename, outfilename, verbose_error_mode, stat_mode)
    print 'Done'

if __name__ == "__main__":
    main()    
