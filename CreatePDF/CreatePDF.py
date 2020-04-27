from PyPDF2 import PdfFileMerger, PdfFileReader
import sys, argparse
from shutil import copyfile
import os

# functions
def createDoc(filename, pageCount, templPath):
    if (pageCount <= 0):
        raise ValueError("pagecount darf nicht kleiner oder gleich 0 sein")
    if os.path.isfile(filename):
        raise FileExistsError("datei existiert bereits")
    merger = PdfFileMerger()
    for i in range(pageCount):
        merger.append(templPath)
    merger.write(filename)
    merger.close()

def appendPages(filename, pageCount, templPath):
    if not os.path.isfile(filename):
        raise FileNotFoundError("datei existiert nicht")
    if (pageCount <= 0):
        raise ValueError("pagecount darf nicht kleiner oder gleich 0 sein")
    copyfile(filename, os.path.join(os.environ['temp'], os.path.basename(filename)))
    merger = PdfFileMerger()
    merger.append(PdfFileReader(filename))
    for i in range(pageCount):
        merger.append(templPath)
    merger.write(filename)
    merger.close()


# script
parser = argparse.ArgumentParser()
parser.add_argument('--filename', '-f', help="full path to pdf", type= str)
parser.add_argument('--pagecount', '-c', help="the number pages", type= int, default=1)
parser.add_argument('--pagetype', '-t', help="pagetype the template should be created with", type= str, default='clean')
parser.add_argument('--append', '-a', help="appends the pages to an existing document", dest='append', action='store_true')
args = parser.parse_args()

filename = args.filename
pagecount = args.pagecount
append = args.append
pagetype = args.pagetype

pageTemplate= os.path.join(os.path.dirname(__file__), '{}.pdf'.format(pagetype))

if append:
    try:
        appendPages(filename, pagecount, pageTemplate)
        print("{} leere Seiten wurden hinzugefügt!".format(pagecount))
        print("Backup liegt in temp!")
    except ValueError:
        print("Fehler - Die Seitenzahl darf nicht 0 oder kleiner sein!")
    except FileNotFoundError:
        print("Fehler - Die angegebene Datei existiert nicht!")
else:
    try:
        createDoc(filename, pagecount, pageTemplate)
        print("Dokument mit {} Seiten erstellt!".format(pagecount))
    except ValueError:
        print("Fehler - Die Seitenzahl darf nicht 0 oder kleiner sein!")
    except FileExistsError:
        print("Fehler - Datei existiert bereits!")