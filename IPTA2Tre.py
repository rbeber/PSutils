#!/usr/bin/env python3
#/***************************************************************************\
#|  Name                : IPTA2Tre                                           |
#|  Description         : Fix IPTA outputs to be digested by Qgis            |   
#|  Date                : April 15, 2021                                     |
#|  copyright           : (C) 2021 by Raniero Beber (IRPI-CNR, Italy)        |
#|  email               : raniero.beber@gmail.com                            |
#\***************************************************************************/
import os,sys
import warnings, time, argparse, pathlib
import pandas as pd
import geopandas as gpd
import re

if __name__ == '__main__':
    start_time = time.process_time()

    #warnings.filterwarnings('ignore', '', dbf.FieldNameWarning)
    
    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)


    parser = MyParser(description='Fix IPTA outputs to be digested by Qgis')
    parser.add_argument('-i','--in_table', type=pathlib.Path, 
                      required=True, help='IPTA *.txt file containing the data table')
    parser.add_argument('-m','--in_meta', type=pathlib.Path, 
                      required=True, help='IPTA *.txt file with metadata (dates)')
    parser.add_argument('-e','--in_EPSG', type=int, 
                      required=True, help='EPSG integer of long lat coordinates in table')
    parser.add_argument('-o','--out_shp', type=pathlib.Path,
                      required=True, help='where to save the *.shp file generated, if ext not specified a folder is created',default='-')
    args = parser.parse_args()
    #print(args)
    #args.in_table.close()
    #args.in_meta.close()
    
    IPTA_table=args.in_table    
    IPTA_meta=args.in_meta
    IPTA_EPSG = args.in_EPSG
    SHP_out=args.out_shp

    #iitialize variables for metafile
    col_names_init=['ID',
           'x_pixel',
           'y_pixel',
           'lon_deg',
           'lat_deg',
           'height',
           'def_rate',
           'sd_res_ph',
           'height_unc',
           'rate_unc']

    #From metafile of file
    #```
    #    1  point number
    #    2  x pixel in the reference image
    #    3  y pixel in the reference image
    #    4  longitude (deg.)
    #    5  latitude (deg.)
    #    6  height (m)
    #    7  deformation rate (mm/y)q
    #    8  standard deviation of the residual phase (rad)
    #    9  estimated height uncertainty (m)
    #    10  estimated deformation rate uncertainty (mm/y)
    #```
    #the followigns comes afterwards
    #```
    #    11  displacement (mm)  date: 2014 10 27     60515.246  JD:    16370.70041  days: -1752.00034
    #``` 
    
    #
    #just warning the user
    if input("This script will create a  *.shp file from IPTA, it will take ~ few minutes \nDo You Want To Continue? [y/N]") != "y":
        exit()
    
    path_shp_IPTA=os.path.expanduser(IPTA_table)
    path_meta_IPTA=os.path.expanduser(IPTA_meta)   
    
    IPTA_meta= pd.read_csv(path_meta_IPTA, skiprows=10, skipfooter=3,engine='python', header=None) 
    
    col_names= []
    
    for ele in IPTA_meta.iterrows():
        text = ele[1][0]
        #print(text)
        match = re.findall(r"date: (.{10})", text)[0] #return a list of finds of the '10+1 space caracters after date:'
        #print(match)
        midm = re.sub(r"(?:^|(?<=[^0-9]))([0-9]{1})(?=$|[^0-9])", "0\\1", match, 0)
        #print(midm)
        #print(re.sub(r"\s+", "", midm))
        col_names.append('D'+re.sub(r"\s+", "", midm)) 
    
    #
    col_names_tot=col_names_init+col_names 
    
    IPTA_df= pd.read_csv(path_shp_IPTA, header=None, names=col_names_tot)

    #IPTA_EPSG = string()
    #an other way
    gdf = gpd.GeoDataFrame(IPTA_df.copy())
    gdf.set_geometry(
        gpd.points_from_xy(gdf['lon_deg'], gdf['lat_deg']),
        inplace=True, crs='EPSG:'+str(IPTA_EPSG))
    #gdf.drop(['Lat', 'Long'], axis=1, inplace=True)  # optional
    # Determine the output path for the Shapefile
    #outfp = "IPTA\IPTA_df_geo.shp"

    # Write the data into that Shapefile
    gdf.to_file(SHP_out)
    print("--- %.2f seconds ---" % (time.process_time() - start_time))