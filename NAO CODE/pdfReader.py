from StringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams,LTTextBoxHorizontal, LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.layout import LTTextBox, LTTextLine, LTFigure, LTImage,LTPage
import re
import sys, os
sys.path.append('NAO CODE/books/')

locationImg = []
locationTxt = []
def convert(fname,pages=None):
    
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(os.path.join(sys.path[0],fname), 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    #print text 

    # write Content to .txt
    text_file = open(os.path.join(sys.path[0],"output.txt"), "w")
    text = re.sub("\s\s+", " ", text)
    text_file.write("%s" % text)
    text_file.close()

#convert("60744-whoop-goes-the-pufferfish.pdf",pages=[1,2,3,4,5,6,7,8,9,10,11])

def getloction (pagesize, bbox):
    x = pagesize[2]/2
    y = pagesize[3]/2
    x0 = (bbox[2]+bbox[0])/2
    y0 = (bbox[3]+bbox[1])/2
   
    if (abs(x0-x)<=30) and (abs(y0-y)<=30):
        return "middle"
    elif (x0 < x) and (y0 < y):
        return "leftbottom"
    elif (x0 > x) and (y0 > y):
        return "righttop"
    elif (x0 < x) and (y0 > y):
        return "lefttop"
    else:
        return "rightbottom"
    


"""Function to parse the layout tree."""
def parse_layout(pagesize, layout):
    
    locations_image = []
    locations_text = []
    
    for lt_obj in layout:   
        if isinstance(lt_obj,LTFigure):
            parse_layout(pagesize, lt_obj)
        if isinstance(lt_obj, LTImage):
         
            location_img = getloction(pagesize, lt_obj.bbox)
            print (lt_obj.__class__.__name__ + ":" + location_img)
            locations_image.append(location_img)
            locationImg.append(locations_image[0])
            break
    for lt_obj in layout:  
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            text = (lt_obj.get_text()).encode('utf-8')
            
            if not (text == "([0-9]+)\/([0-9]+)"):
                location_txt = getloction(pagesize, lt_obj.bbox)           
                print (lt_obj.__class__.__name__ + ":" + location_txt)
                locations_text.append(location_txt)
                print "locationtext:",locations_text
                print(text)
                locationTxt.append(locations_text[0])
                break
                
    
    
        
def layout(isText, fname, pages=None):
    
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    infile = file(os.path.join(sys.path[0],fname), 'rb')
    
    #get the page zise
    parser = PDFParser(open(os.path.join(sys.path[0],fname), 'rb')) 
    doc = PDFDocument(parser)
    pagelist = []
    for page in PDFPage.create_pages(doc):
        pagelist.append(page)
    pagesize = pagelist[1].mediabox        

    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
        layout = device.get_result()
        parse_layout(pagesize, layout)
    infile.close()
   
    dict_img = dict(zip(pages,locationImg))
    dict_txt = dict(zip(pages,locationTxt))

    if isText == True:
        return dict_txt
    else:
        return dict_img

#layout(True, "60744-whoop-goes-the-pufferfish.pdf", pages=[1,2,3,4,5,6,7,8,9,10,11])


