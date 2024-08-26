from django.shortcuts import render
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
def subscribe(request):
    link = os.getenv('TG_LINK')
    return render(request, 'notifications/subscribe.html', context={'link':link})