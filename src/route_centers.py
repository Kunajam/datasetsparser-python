
'''
KunaJam - A new dimension in traffic management 

@author     Mutinda Boniface <http://bmutinda.com>
@link       http://kunajam.com
@copyright  2015
'''

class RouteCentersFileAnalyzer:
    def __init__( self, _filename ):
        self.filename = _filename
        self.data_keys_tmp = []
        self.data_sets_tmp = []
        self.data_keys = []
        self.data_sets = []
        self.data = []

    def analyse( self ):
        print( 'Reading file contents' )

        if not self.filename:
            raise Exception("filename was not supplied..")

        lines = tuple( open( self.filename, "r") )
        # Lets get our data keys/titles/labels 
        self.data_keys_tmp = lines[0]
        # Lets ommit the first tuple and pick the rest as it contains our data keys
        data_unformatted = lines[1::1]
        for this_line in data_unformatted:
            # remove \r\n characters 
            self.data_sets_tmp.append( this_line.rstrip() )

        self.formatAll()

    def formatAll( self ):

        print 'Formating extracted data'

        # Now lets extract all what we need and leave the rest 
        '''
         The data received from the API is in this format (after removing the keys which are on line 1 of the file )
         -----------------------------------------------------------------------------------------------------------------------
            stop_id,stop_code,stop_name,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station
            0005AMB,,Ambassadeur,-1.285963,36.826048,,,1,
         -----------------------------------------------------------------------------------------------------------------------
         We only need data : stop_name, stop_lat and stop_lon
        '''

        # Lets start with keys 
        self.data_keys = self.data_keys_tmp.split( ",")[2:5]
        for entry in self.data_sets_tmp:
            entry_data = entry.split( ",")[2:5]
            self.data_sets.append( tuple( entry_data) )

        # Now we re-arrange the keys and specific data to form a complete data set
        '''
         At the end this is what we expect 
         data = {
            [stop_name: name_here, stop_lat:latitude_here, stop_lon:longitude_here  ],
            [ ...... ],
         }
        '''
        data = []
        for value in self.data_sets:
            this_center = {}
            this_center[self.data_keys[0]] = value[0]
            this_center[self.data_keys[1]] = value[1]
            this_center[self.data_keys[2]] = value[2]
            data.append( this_center )

        self.data = data
        return self.data

    def writeToFile( self, filename='centers_json' ):
        print 'writing to file %s.json' %(filename)

        output = open( "datasets/"+filename+".json", "w+")
        import json
        output.write( str( json.dumps(self.getData()) ) )
        output.close()

    def getData( self ):
        return self.data

def main():
    filename = "datasets/bus_stops.txt"
    file_obj = RouteCentersFileAnalyzer( filename )
    data = file_obj.analyse( )
    file_obj.writeToFile( )
    
if __name__=='__main__':
    main()