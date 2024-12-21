from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MessageForm
from .models import Message

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Mensaje enviado con éxito.')
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'appMensajeria/send_message.html', {'form': form})

@login_required
def inbox(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'appMensajeria/inbox.html', {'messages_received': messages_received})