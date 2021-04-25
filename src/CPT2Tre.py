#!/usr/bin/python3
#/***************************************************************************\
#|  Name                : CPT2Tre                                            |
#|  Description         : Fix the CPT output to be digested by Qgis          |   
#|  Date                : April 15, 2021                                     |
#|  copyright           : (C) 2021 by Raniero Beber (IRPI-CNR, Italy)        |
#|  email               : raniero.beber@gmail.com                            |
#\***************************************************************************/
import os,sys
import warnings, time, argparse, pathlib
import geopandas as gpd

if __name__ == '__main__':
	class MyParser(argparse.ArgumentParser):
	    def error(self, message):
	        sys.stderr.write('error: %s\n' % message)
	        self.print_help()
	        sys.exit(2)
	
	parser = MyParser(description='Fix the CPT output to be digested by Qgis')
	parser.add_argument('-i','--in_shp', type=pathlib.Path, 
	                      required=True, help='CPTA *.shp file to be fixed')
	parser.add_argument('-o','--out_shp', type=pathlib.Path,
	                      required=True, help='where to save the *.shp file generated, if ext not specified a folder is created',default='-')
	#parser.add_argument('--usage', help='use on *.DBF of a *.shp')
	#parser.add_argument('foo', nargs='+', help='missed *.DBF file')
	args = parser.parse_args()
	
	start_time = time.process_time()
	
	CPTA_table=args.in_shp
	SHP_out=args.out_shp
	
	path_shp_CPTA=os.path.expanduser(CPTA_table)
	path_shp_CPTA_out=os.path.expanduser(SHP_out)
	
	
	#just warning the user
	if input("This script will create a new SHP file from the INPUT, it will take ~ few minutes \nDo You Want To Continue? [y/N]") != "y":
	    exit()
	
	
	
	
	df_shp = gpd.read_file(path_shp_CPTA)
	#adding D in fornt of headears that are ony decimal
	df_shp.rename(columns=lambda x: 'D{0}'.format(x) if x.isdecimal() else x, inplace=True)
	
	df_shp.to_file(path_shp_CPTA_out)
	print("--- %.2f seconds ---" % (time.process_time() - start_time))