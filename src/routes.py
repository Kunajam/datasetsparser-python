
'''
KunaJam - A new dimension in traffic management 

@author     Mutinda Boniface <http://bmutinda.com>
@link       http://kunajam.com
@copyright  2015
'''

class RoutesFileAnalyzer:
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
         route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color
         10200010811,UON,108,Gachie,UN-NewMuthaiga-Gachie-Gichagi,3,,,
         -----------------------------------------------------------------------------------------------------------------------
         We only need data from route_short_name  upto route_desc
        '''

        # Lets start with keys 
        self.data_keys = self.data_keys_tmp.split( ",")[2:5]
        self.data_keys.append("routes")
        for entry in self.data_sets_tmp:
            entry_data = entry.split( ",")[2:5]
            self.data_sets.append( tuple( entry_data) )

        # Analyse the long route description by splitting up the locations as another turple 
        '''
         -----------------------------------------------------------------------------------------------------------------------
         Gachie,UN-NewMuthaiga-Gachie-Gichagi - Should contain routes as follows 
            Gachie - UN, UN - NewMuthaiga, NewMuthaiga- Gachie, Gachie - Gichagi
         ----------------------------------------------------------------------------------------------------------------------

         At the end this is what we expect 
         data = {
            [ short_name: 108, long_name:Gachie, description: UN-NewMuthaiga-Gachie-Gichagi, routes: [Gachie - UN, UN - NewMuthaiga, NewMuthaiga- Gachie, Gachie - Gichagi] ],
            [ ...... ],
         }
        '''
        data = []
        for value in self.data_sets:
            this_route = {}
            this_route[self.data_keys[0]] = value[0]
            this_route[self.data_keys[1]] = value[1]
            this_route[self.data_keys[2]] = value[2]
            this_route[self.data_keys[3]] = self.splitRouteDescription( value[2] )
            data.append( this_route )

        self.data = data 
        return self.data

    def splitRouteDescription( self, description ):
        routes = []
        route_names  = description.split( "-")
        for i in range( len(route_names)-1 ):
            routes.append( route_names[i]+"-"+route_names[i+1] )
        return routes

    def writeToFile( self, filename='routes_json' ):
        print 'writing to file %s.json' %(filename)

        output = open( "datasets/"+filename+".json", "w+")
        import json
        output.write( str( json.dumps(self.getData()) ) )
        output.close()

    def getData( self ):
        return self.data

def main():
    filename = "datasets/routes.txt"
    file_obj = RoutesFileAnalyzer( filename )
    data = file_obj.analyse( )
    file_obj.writeToFile( )
    
if __name__=='__main__':
    main()