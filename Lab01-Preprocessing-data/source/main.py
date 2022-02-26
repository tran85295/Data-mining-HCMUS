import argparse   #for parsing arguments
import DataFrame  #util class for processing data

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Process some functions.')
   parser.add_argument("-m", "--method", help = 'Method to be used by some functions')
   parser.add_argument("-o", "--outfile", help = 'Output file name')
   parser.add_argument("-c", "--columns", help = 'List of input columns', nargs = '+')
   parser.add_argument("--threshold", default = '50', help = 'Percent, 50 by default')
   parser.add_argument("--formula", help = 'Formula to generate new column using existing columns')
   # Get arguments 
   args, unknown = parser.parse_known_args()

   # The first two arguments must represent function name and input file name
   function = unknown[0]
   inputfile = unknown[1]

   # Load file into dataframe using constructor
   df = DataFrame.DataFrame(inputfile)
   # Perform a specific function using the parsed arguments
   # e.g. df.list_missing(args)
   eval('df.'+function+'(args)')




