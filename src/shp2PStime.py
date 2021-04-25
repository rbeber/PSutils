#!/usr/bin/env python3
#/***************************************************************************\
#|  Name                : shp2PStime                                         |
#|  Description         : Create *.csv INPUT for PSTime exe                  |   
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


    parser = MyParser(description='Create *.csv INPUT for PSTime exe')
    parser.add_argument('-i','--in_shp', type=pathlib.Path, 
                      required=True, help='SHP file in input to be converted')
    parser.add_argument('-t','--in_TYPE', type=str, 
                      required=True, help='type of source of the shp file, choose amongst: IPTA, CPTA, TRE')
    parser.add_argument('-o','--out_csv', type=pathlib.Path,
                      required=True, help='where to save the *.csv file generated',default='-')
    args = parser.parse_args()
    #print(args)
    #args.in_table.close()
    #args.in_meta.close()
    
    SHP_file=args.in_shp    
    data_type = args.in_TYPE
    output_csv=args.out_csv
    #
    #just warning the user
    if input("This script will create a  *.csv file from a *.shp file in INPUT, it will take ~ few minutes \nDo You Want To Continue? [y/N]") != "y":
        exit()
    
    path_shp=os.path.expanduser(SHP_file)
        
    #diff type of file in inputs
    Ncol_drop = {'IPTA': 9, 'CPTA': 5, 'TRE': 12} #here to fix TRE since in this way left ID not CODE

    #import *.shp file
    df_shp = gpd.read_file(path_shp)
    
    # from geopandas to pandas, drop geometry
    df = pd.DataFrame(df_shp.drop(columns='geometry'))

    cols_drop = list(range(1,Ncol_drop[data_type]+1))
    df.drop(df.columns[cols_drop],axis=1,inplace=True)
    # `inplace=True` is used to make the changes in the dataframe itself without doing the column dropping on a copy of the data frame. If you need to keep your original intact, use: df_after_dropping = df.drop(df.columns[cols],axis=1)
    # 
    # write data to csv
    df.to_csv(output_csv, index=False)       
    print("--- %.2f seconds ---" % (time.process_time() - start_time))