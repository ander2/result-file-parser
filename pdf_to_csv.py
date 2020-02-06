import tabula
import sys

if __name__ == "__main__":
    filename = sys.argv[1]
    if filename.strip() == '':
        printf('Please insert a filename')
    else:
        # convert PDF into CSV file
        output = filename.replace('.pdf', '.csv')
        tabula.convert_into(filename, output, lattice=True, output_format="csv", pages='all')
