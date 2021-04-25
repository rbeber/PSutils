#!/usr/bin/env python3
#/***************************************************************************\
#|  Name                : PStime2shp                                         |
#|  Description         : Create *.shp to visualize OUTPUT of PSTime exe     |   
#|  Date                : April 23, 2021                                     |
#|  copyright           : (C) 2021 by Raniero Beber (IRPI-CNR, Italy)        |
#|  email               : raniero.beber@gmail.com                            |
#\***************************************************************************/
import os,sys
import warnings, time, argparse, pathlib
import pandas as pd
import geopandas as gpd

if __name__ == '__main__':
    start_time = time.process_time()

    #warnings.filterwarnings('ignore', '', dbf.FieldNameWarning)
    
    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)


    parser = MyParser(description='Create *.shp OUTPUT from PSTime exe')
    parser.add_argument('-i','--in_csv', type=pathlib.Path, 
                      required=True, help='CSV file in input to be converted')
    parser.add_argument('-s','--in_shp', type=pathlib.Path, 
                      required=True, help='SHP file in input to be used for georeff')
    parser.add_argument('-t','--in_TYPE', type=str, 
                      required=True, help='type of source of the shp file, choose amongst: IPTA, CPTA, TRE')
    parser.add_argument('-o','--out_shp', type=pathlib.Path,
                      required=True, help='where to save the *.shp file generated, if ext not specified a folder is created',default='-')
    args = parser.parse_args()
    #print(args)
    #args.in_table.close()
    #args.in_meta.close()
    
    in_csv=args.in_csv
    SHP_file=args.in_shp    
    data_type = args.in_TYPE
    output_shp=args.out_shp
    #
    #just warning the user
    if input("This script will create a  *.shp file of the Berti, 2013 PStime OUTPUT, it will take ~ few minutes \nDo You Want To Continue? [y/N]") != "y":
        exit()
    
    Ncol_drop = {'IPTA': 9, 'CPTA': 5, 'TRE': 12} #here to fix TRE since in this way left ID not CODE

    path_shp=os.path.expanduser(SHP_file)
    path_csv=os.path.expanduser(in_csv)


    df = pd.read_csv(path_csv)
    #since the OUTPUT from PSTime have Code instead of ID
    df.rename(columns={'Code':'ID'}, inplace=True)
    
    df_shp = gpd.read_file(path_shp)
    geom_col = df_shp.pop('geometry')
    inv_cols_drop = list(range(Ncol_drop[data_type]+1, len(df_shp.columns)))
    df_shp.drop(df_shp.columns[inv_cols_drop],axis=1,inplace=True)
    df_shp = df_shp.merge(df, on='ID')
    df_shp['geometry']= geom_col
    gdf = gpd.GeoDataFrame(df_shp.copy())

    #save to shp
    gdf.to_file(output_shp)      
    print("--- %.2f seconds ---" % (time.process_time() - start_time))