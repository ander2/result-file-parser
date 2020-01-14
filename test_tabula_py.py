import tabula

# convert PDF into CSV file
tabula.convert_into("2020111_194026_200111_Arraun denborrak.pdf", "2020111_194026_200111_Arraun denborrak.csv", lattice=True, output_format="csv", pages='all')
