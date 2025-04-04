from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Manufacturer, Product
from .serializers import ManufacturerSerializer, ProductSerializer
from django.contrib import messages
from rest_framework.decorators import api_view
from .scraper import scrape_products
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import EmailMessage


@login_required
def home(request):
    manufacturers = []
    query = ""

    if request.method == "POST":
        if "query" in request.POST:
            # Handle search
            query = request.POST.get("query", "")
            if query:
                scraped_data = scrape_products(query)  # Call the scraper
                for item in scraped_data:
                    manufacturer_info = item.get("Manufacturer", {})
                    name = manufacturer_info.get("name")
                    email = manufacturer_info.get("contact_email")

                    if name and email:  # Only add if both are present
                        manufacturers.append(
                            {
                                "name": name,
                                "website": manufacturer_info.get("website", "#"),
                                "contact_email": email,
                            }
                        )

        elif "manufacturer_email" in request.POST:
            # Handle AJAX email sending
            manufacturer_email = request.POST.get("manufacturer_email")
            manufacturer_name = request.POST.get("manufacturer_name")
            user_email = request.user.email

            if not manufacturer_email or manufacturer_email == "Not Available":
                return JsonResponse(
                    {
                        "success": False,
                        "message": "No email available for this manufacturer.",
                    }
                )

            subject = f"Business Inquiry Regarding {manufacturer_name}"
            message = f"""
            Dear {manufacturer_name},

            I am reaching out as I am interested in collaborating with your company. 
            I would love to discuss potential business opportunities with you. 

            Please let me know a convenient time to connect.

            Looking forward to your response.

            Best Regards,  
            {request.user.username}  
            {user_email}
            """

            try:
                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,  # Sender (your configured email)
                    [manufacturer_email],  # Recipient
                    bcc=[user_email],  # BCC: User also gets a copy
                    reply_to=[user_email],  # Reply goes to the user
                )
                email.send()

                return JsonResponse(
                    {"success": True, "message": "Email sent successfully!"}
                )
            except Exception as e:
                return JsonResponse(
                    {"success": False, "message": f"Error sending email: {str(e)}"}
                )

    return render(
        request,
        "home.html",
        {"manufacturers": manufacturers, "query": query},
    )


from django.http import JsonResponse


@api_view(["GET"])
def scrape_view(request):
    query = request.GET.get("query", "default_product")
    products = scrape_products(query)
    return Response({"products": products})


@login_required
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        title = request.POST.get("title")
        message = request.POST.get("message")

        full_message = f"From: {name} ({email})\n\n{message}"

        send_mail(
            subject=title,
            message=full_message,
            from_email=email,
            recipient_list=["vikasreach02@gmail.com"],
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully!")

    return render(request, "contact.html")


def about_view(request):
    return render(request, "about.html")


# Manufacturer List/Create API
class ManufacturerListCreateView(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Only authenticated users can access


# Manufacturer Retrieve/Update/Delete API
class ManufacturerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [permissions.IsAuthenticated]


# Product List/Create API
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


# Product Retrieve/Update/Delete API
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
