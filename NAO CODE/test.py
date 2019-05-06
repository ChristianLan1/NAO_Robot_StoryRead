import re
with open('C:/Users/Zoe Chai/Desktop/books/book_pages.txt') as f:
    lines = f.readlines()
    #print lines
    book = []
    count = 0
    pages = []
    for line in lines:
        
        line = line.rstrip()
        if count==1:
            
            line = re.findall("[0-9]+",line)
            print line
            for element in line:
                
                pages.append(int(element))
            line = pages

        book.append(line)
        count += 1
    print book

    
        
  
            
            