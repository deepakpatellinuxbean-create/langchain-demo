# yadi hume pure folder hi load karwana ho jiske andar multiple files hai to us case me DirectoryLoader use kia jata hai
# below e.g. me hum ek directory load kr rhe hai jiske andar multiple pdf files hai

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path="DocumentLoaders/pdf_files_directory",
    glob="*.pdf", #isme batana padta hai ki konsi files hum load krna chahta hai via passing a pattern current pattern says ki tum saari pdf file load kro jo ki pdf_files_directory ke andar hai we do have other patterns as well for e.g. "**/*.txt": Find every .txt file, including files inside all subfolders., "*.pdf": Find .pdf files only in the current/root directory, "data/*.csv": Find .csv files specifically inside the data/ folder, "**/*": Find every file of every type, including files in all subfolders
    loader_cls=PyPDFLoader # loader batana padta hai ki konsa required to load these files
    )

docs = loader.lazy_load() # ek generator return krta hai jiski madad se hum jo bhi required document object hai unge yield kr skte hai one at a time taki memory and time dono bache. list ek sath multiple docs ko ek baar me load krta hai which consumes a lot of time and memory to is chiz se bachne ke liye hum DirectoryLoader me usually lazy_load() use krte hai instead load.

print(docs)

print(docs[4].page_content)
print(docs[4].metadata)