from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(file_path="DocumentLoaders/pdf_file.pdf")

# pdf files ko load krta hai and har page ke liye ek alag document object banata hai for e.g yadi pdf file me 20 pages hai to loader.load() list return krega and is list ke andar 20 document objects honge each representing one single page. har ek document object me page_content and metadata hoga.  
docs = loader.load()

print(docs) 
