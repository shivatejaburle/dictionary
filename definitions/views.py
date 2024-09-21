from django.shortcuts import render
from django.views import View
from django.conf import settings

# Import json to load JSON Data to Python Dictionary 
import json

# To make a request to API
import urllib.request

# Create your views here.

class IndexView(View):
    template_name = 'definitions/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        word = request.POST['search_word']
        search_word = word.replace(" ", "%20")
        
        try:

            # Get your API Key from Wordnik
            # https://developer.wordnik.com/

            # Get JSON data from API
            api_url_def = str('https://api.wordnik.com/v4/word.json/'+search_word+'/definitions?limit=200&includeRelated=false&sourceDictionaries=wordnet&useCanonical=false&includeTags=false&api_key='+settings.DICTIONARY_API_KEY)
            source_data_def = urllib.request.urlopen(api_url_def).read()
            
            # Convert JSON Data to a Python Dictionary
            list_of_data_def = json.loads(source_data_def)

            # For definitions of search word
            definitions = ""

            for d in list_of_data_def:
                definitions += "<i>" + d['partOfSpeech'] + "</i><br><strong>" + d['text'] + "</strong><br><br>"
 
            dictionary = {
                'search_word': word,
                'definitions': definitions,
            }

            # Get audio for the search word
            try:
                api_url_audio = str('https://api.wordnik.com/v4/word.json/'+search_word+'/audio?useCanonical=false&limit=50&api_key='+settings.DICTIONARY_API_KEY)
                source_data_audio = urllib.request.urlopen(api_url_audio).read()
                list_of_data_audio = json.loads(source_data_audio)
                pronunciation = list_of_data_audio[1]['fileUrl']
                # Add audio to dictionary
                dictionary.update(pronunciation=pronunciation)
            except:
                # When Audio not found
                print("Audio not found...")

            context = {
                'dictionary': dictionary
            }
        
        except:
            # When Word not found
            print("Word not found...")
            dictionary = {
                'error': '"'+ word + '" is not available in the dictionary...',
            }

            context = {
                'dictionary': dictionary
            }

        return render(request, self.template_name, context)