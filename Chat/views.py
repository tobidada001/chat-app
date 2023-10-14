from django.shortcuts import render, get_object_or_404
from Chat.models import Room, RoomMessages

# Create your views here.
def index(request):
    rooms = Room.objects.all()
    return render(request, 'index.html', {'rooms': rooms})



def room_detail(request, slug):
    room = get_object_or_404(Room, slug= slug)
    room_messages = RoomMessages.objects.filter(room = room)


    return render(request, 'chat.html', {'room': room, 'room_messages': room_messages})