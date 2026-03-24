from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_msg = data.get('message', '').lower()
            
            # Simple rule-based NLP logic
            reply = "I'm not sure I understand. Try asking for '2BHK in Hyderabad' or 'cheap sharing rooms'."
            
            if 'hi' in user_msg or 'hello' in user_msg:
                reply = "Hello! I'm your Mini NoBroker assistant. How can I help you find a property today?"
            elif 'cheap' in user_msg or 'budget' in user_msg:
                reply = "If you're looking for budget options, try searching for properties under 8000. For example: 'show me properties under 8000'."
            elif 'sharing' in user_msg:
                reply = "We have great sharing accommodations! Just search for 'sharing for 2' or 'sharing in Gachibowli'."
            elif 'bhk' in user_msg:
                match = re.search(r'(\d)bhk', user_msg)
                if match:
                    reply = f"Looking for a {match.group(1)}BHK? You can type that directly into our smart search bar at the top of the home page!"
                else:
                    reply = "We have 1BHK, 2BHK, 3BHK, etc. Just use the search bar!"
            elif 'owner' in user_msg or 'list' in user_msg or 'add' in user_msg:
                reply = "If you're an owner, you can list properties by logging in as an Owner and clicking 'Add Property'."
            elif 'rent' in user_msg:
                reply = "Finding a rental is easy! Use the search bar on the home page to filter by layout and price."
                
            return JsonResponse({'reply': reply})
        except Exception as e:
            return JsonResponse({'reply': 'Sorry, something went wrong on my end.'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
