from datetime import datetime
import base64
import os

import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from myapp.models import Contact

# M-Pesa Daraja API Credentials from environment variables
CONSUMER_KEY = os.environ.get("MPESA_CONSUMER_KEY", "")
CONSUMER_SECRET = os.environ.get("MPESA_CONSUMER_SECRET", "")
SHORTCODE = os.environ.get("MPESA_SHORTCODE", "174379")
PASSKEY = os.environ.get("MPESA_PASSKEY", "")
CALLBACK_URL = os.environ.get("MPESA_CALLBACK_URL", "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest")


def home(request):
    if request.method == "POST":
        mycontact = Contact(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )
        mycontact.save()
        return render(request, "index.html")
    else:
        return render(request, "index.html")


def blog(request):
    return render(request, "blog.html")


def details(request):
    return render(request, "blog-details.html")


def portfolio(request):
    return render(request, "portfolio-details.html")


def services(request):
    return render(request, "service-details.html")


def starter(request):
    return render(request, "starter-page.html")


def show(request):
    all = Contact.objects.all()
    return render(request, "show.html", {"all": all})


def delete(request, id):
    mycontact = Contact.objects.get(id=id)
    mycontact.delete()
    return redirect("/show")


def edit(request, id):
    editappointment = get_object_or_404(Contact, id=id)
    
    if request.method == "POST":
        editappointment.name = request.POST.get("name")
        editappointment.email = request.POST.get("email")
        editappointment.subject = request.POST.get("subject")
        editappointment.message = request.POST.get("message")
        editappointment.save()
        return redirect("/show")
    else:
        return render(request, "edit.html", {"editappointment": editappointment})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    
    return render(request, "register.html", {"form": form})


def get_access_token():
    """Get M-Pesa access token from Safaricom API."""
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET), timeout=30)
    token = response.json()["access_token"]
    return token


def stk_push(phone, amount):
    """Send STK push to customer's phone."""
    token = get_access_token()
    
    # Timestamp format required by Safaricom: YYYYMMDDHHmmss
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Password = Base64(Shortcode + Passkey + Timestamp)
    password = base64.b64encode((SHORTCODE + PASSKEY + timestamp).encode()).decode()
    
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "Biashara",
        "TransactionDesc": "Payment"
    }
    
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    return response.json()


def payment(request):
    """Show payment form (GET) or trigger STK push (POST)."""
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        amount = request.POST.get("amount", "").strip()
        
        try:
            result = stk_push(phone, amount)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=503)
    
    # GET request -> show the payment form
    return render(request, "payment.html")


def callback(request):
    """M-Pesa sends payment results here after the customer pays."""
    print("M-Pesa Callback:", request.body)
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
