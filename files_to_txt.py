import datetime
import os

def times_to_txt(times, recs):


    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Specify the directory where you want to save the file
    directory = 'output_files'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a filename with the timestamp
    filename = os.path.join(directory, 'output_{}.txt'.format(timestamp))

    # Write to the file
    try:
        with open(filename, 'w') as f:
            for r in times:
                f.write(str(r) + ':')
                for i in times[r]:
                     f.write(str(i) + ',')
            
            f.write('\n\n')

            for j in recs:
                f.write( str(j) + ':' + str(recs[j]) )
    

            
                     
            

    except Exception as e:
        print("An error occurred:", e)

    print("File saved as:", filename)