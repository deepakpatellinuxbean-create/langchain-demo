from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path="DocumentLoaders/csv_file.csv")

# csv files ko load krta hai and list of docs return krta hai har ek row individual ek document object ban jati hai
docs = loader.load()

print(docs) 