#from googletrans import Translator
#from google_trans_new import google_translator  

from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from ScriptyHome import grammer_checker
from ScriptyHome import scripty_gtranslate
from ScriptyHome import scripty_pdfread
from ScriptyHome import scripty_ocr
from ScriptyHome import scripty_dictionary

# Create your views here.

def home(request):
    return render(request, 'home.html')

def grammarCheck(request):
    text = request.POST['text']

    parser = grammer_checker.GingerIt()
    print(parser.parse(text))
    return JsonResponse({'result': parser.parse(text)})


def login(request):
    return HttpResponse('Login')

def translateText(request):
    text = request.POST['text']
    src = request.POST['src']
    dest = request.POST['dest']
    #print(dest)

    translate_text = scripty_gtranslate.gtranslate(text,src=src,dest=dest)
    #print(translate_text)
    return JsonResponse({'result': translate_text})

def getDict(request):
    word = request.POST['word']
    find = request.POST['find']
    
    def synonym():
        return JsonResponse({'result': scripty_dictionary.getsynonym(word) })
    def antonym():
        return JsonResponse({'result':scripty_dictionary.getantonym(word) })
    def meaning():
        return JsonResponse({'result': scripty_dictionary.getmeaning(word) })
    
    switcher = {'synonym': synonym,'antonym': antonym,'meaning': meaning}
    func = switcher.get(find, "nothing")
    return func()


def readPdfImage(request):
    fileToRead = request.FILES['formFile']

    if fileToRead.name.endswith('.pdf'):
        #Save the file to the server
        file_path = 'ScriptyHome/static/UploadedFiles/' + fileToRead.name
        with open(file_path, 'wb+') as destination:
            for chunk in fileToRead.chunks():
                destination.write(chunk)

        #Read the file
        pdf_text = scripty_pdfread.read_pdf(file_path)

        return JsonResponse({'result': pdf_text})

    elif fileToRead.name.endswith('.jpg') or fileToRead.name.endswith('.png'):
        #Save the file to the server
        file_path = 'ScriptyHome/static/UploadedFiles/' + fileToRead.name
        with open(file_path, 'wb+') as destination:
            for chunk in fileToRead.chunks():
                destination.write(chunk)

        #Read the file
        image_text = scripty_ocr.ocr_space_file(filename=file_path)

        return JsonResponse({'result': image_text})

    


    