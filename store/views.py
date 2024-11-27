from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
import json
from .models import Product, Customer, Order, OrderItem, View
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import time
from django.contrib import messages
from .forms import *
import datetime
import requests
import random
import tempfile
from django.core.files import File
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .decorators import *
# Unsplash API key
API_KEY = "wYgceGijHpAwJQSMwrFkNIqDC0jQrBTymFNzFcMPtyQ"
UNSPLASH_URL = "https://api.unsplash.com/search/photos"

# List of food items
food_items = [
    "uncooked Rice", "uncooked vegetables", "uncooked potatoes", "uncooked Flour in a sack", "uncooked beans", "uncooked cassava", "uncooked yam", "uncooked egg", "uncooked meat",
   
]

def get_food_images(food_item):
    params = {
        "query": food_item,
        "client_id": API_KEY,
        "per_page": 1
    }
    response = requests.get(UNSPLASH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            image_url = data['results'][0]['urls']['regular']
            return image_url
    return None

def download_image(image_url):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        # Create a temporary file
        img_temp = tempfile.NamedTemporaryFile(delete=True)
        # Write the image content to the temporary file
        img_temp.write(response.content)
        img_temp.flush()  # Flush the buffer
        return img_temp
    return None

# Function to save products to the database
def save_food_products():
    for food in food_items:
        image_url = get_food_images(food)
        if image_url:
            price = random.randint(100,300)  # Assign random price between 5 and 100
            # Download the image and store it temporarily
            img_temp = download_image(image_url)
            
            if img_temp:
                # Create a new product instance
                product = Product(
                    name=food,
                    price=price,
                    digital=False,  # Set digital to True
                )
                # Save the image to the Product's ImageField using Django's File class
                product.image.save(f"{food}.jpg", File(img_temp), save=True)
                img_temp.close()  # Close and delete the temporary file
                print(f"Saved: {food} with price {price} and image from {image_url}")

# Call the function to save the products

# Create your views here.
@non_driver_required
def store(request):
    # save_food_products()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request,'store/store.html', context)
    


def store_details(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.get(id=id)
    context = {'products': products, 'cartItems': cartItems}
    return render(request,'store/store_details.html', context)

@login_required
@non_driver_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        messages.error(request, 'You need to login')
        return redirect('/login')

    total = order.get_cart_total + 1300
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'total': total,
    }
    # print('sam',order.get_cart_total)

    return render(request, 'store/cart.html', context)

@login_required
@non_driver_required
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        messages.error(request, 'You need to login')
        return redirect('/login')
        
    total = order.get_cart_total + 1300
    context = {
        'cartItems': cartItems,
        'items': items,
        'order': order,
        'total': total
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        if product.quantity > 0:
            orderItem.quantity += 1
            product.quantity -= 1
            product.save()
        else:
            return JsonResponse('Out of stock', safe=False)
    elif action == 'remove':
        orderItem.quantity -= 1
        product.quantity += 1
        product.save()

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    # Prepare the updated data for JSON response
    cart_items_count = order.get_cart_items  # Assuming get_cart_items is a method in your Order model
    cart_total = order.get_cart_total  # Assuming get_cart_total is a method in your Order model
    item_quantity = product.quantity if product.id else 0

    return JsonResponse({
        'item_quantity': item_quantity,
        'cart_total': cart_total,
        'cart_items_count': cart_items_count,
    })

def view(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    product = get_object_or_404(Product,id=id)
    views = View.objects.filter(product=product)
    context = {
        'product': product,
        "cartItems": cartItems
    }
    return render(request, 'store/store_details.html', context)

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username Exists.")
            return redirect('register')

        if not username or not password1 or not password2:
            messages.error(request, "Username and passwords are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('register')
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)
            messages.success(request, 'Registration Successful')
            return redirect('/login')
        else:
            messages.error(request, 'Registration Failed')
    else:
        form = CreateUserForm()

    return render(request,'store/register.html',{'form': form})


@login_required
@non_driver_required
def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/contact-us')
    else:
        form = Contact()
    return render(request, 'store/contact.html', {'form': form, 'cartItems': cartItems})
    
def assign_driver_to_delivery(delivery):
    # Get the driver with the least number of active deliveries
    driver = DeliveryDriver.objects.order_by('current_deliveries').first()

    if driver:
        # Assign the driver to the delivery
        delivery.driver = driver
        delivery.save()

        # Increase the driver's workload
        driver.current_deliveries += 1
        driver.save()

    return driver


def processOrder(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        transaction_id = datetime.datetime.now().timestamp()
        order.transaction_id = transaction_id
        order.complete = True  # Mark the order as complete
        order.save()

        # Handle shipping details if applicable
        if order.shipping == True:
            shipping, created = Shipping.objects.get_or_create(
                customer=customer,
                order=order,
                defaults={
                    'address': data['shipping']['address'],
                    'zipcode': data['shipping']['zipcode'],
                    'country': data['shipping']['country'],
                    'state': data['shipping']['state'],
                }
            )

            # Create a delivery for this order
            delivery = Delivery.objects.create(
                order=order,
                customer=customer,
                address=shipping.address,
                delivery_method=data.get('delivery_method', 'STANDARD'),  # 'STANDARD' by default
                delivery_fee=data.get('delivery_fee', 1500.00), 
                status='PENDING',  # Initial status
            )

            assign_driver_to_delivery(delivery)
    else:
        print('User is not logged in')

    print('Data:', request.body)
    return JsonResponse('Payment Complete!', safe=False)

@login_required
@non_driver_required
def order_list_view(request):

    orders = Order.objects.filter(customer=request.user.customer)  # Get all orders
    completed_orders = orders.filter(complete=True)  # Filter completed orders
    incomplete_orders = orders.filter(complete=False)  # Filter incomplete orders
    
    context = {
        'completed_orders': completed_orders,
        'incomplete_orders': incomplete_orders,
    }
    
    return render(request, 'store/orders.html', context)


def confirm_order_completion(request, order_id):
    # Get the order by ID
    order = get_object_or_404(Order, id=order_id)
    
    # Update the completion status
    order.complete = True
    order.save()

    # Redirect back to the order list or any other page
    return redirect('orders') 


def send_delivery_update_email(delivery):
    # Prepare the context for the email template
    context = {
        'delivery': delivery,
    }

    # Load HTML template and generate email content
    html_content = render_to_string('store/delivery_status_update.html', context)  # This is the HTML template
    text_content = strip_tags(html_content)  # Strip HTML tags to create a plain text version

    # Prepare the email
    subject = 'Your Delivery Status Has Been Updated'
    from_email = 'kayodeola47@gmail.com'
    to_email = [delivery.customer.user.email]  # Customer's email

    # Create the email with both HTML and plain text
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send(fail_silently=False)




def send_driver_id(driver):
    # Prepare the context for the email template
    context = {
        'driver': driver,
    }

    # Load HTML template and generate email content
    html_content = render_to_string('store/driver_email.html', context)  # This is the HTML template
    text_content = strip_tags(html_content)  # Strip HTML tags to create a plain text version

    # Prepare the email
    subject = 'Your account has been created'
    from_email = 'kayodeola47@gmail.com'
    to_email = [driver.email]  # Customer's email

    # Create the email with both HTML and plain text
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send(fail_silently=False)






def mark_delivery_as_completed(delivery):
    if delivery.status == 'DELIVERED' and delivery.driver:
        # Decrease the driver's current deliveries count
        delivery.driver.current_deliveries -= 1
        delivery.driver.save()



@login_required
def all_deliveries(request):
    try:
        # Check if the user is a delivery driver by accessing the related DeliveryDriver model
        driver = request.user
        if DeliveryDriver.objects.filter(user=driver).exists():
            print('sam')
        else:
            return HttpResponse("You can't view this page. It only for drivers", status=403)

    except DeliveryDriver.DoesNotExist:
        return HttpResponse("You can't view this", status=403)
        messages.error(request, "You do not have permission to view this page.")
    driver = DeliveryDriver.objects.get(user=driver)

    # Filter deliveries for the logged-in delivery driver
    deliveries = Delivery.objects.filter(driver=driver)
    
    # List of forms matching the deliveries
    forms = [DeliveryStatusUpdateForm(instance=delivery) for delivery in deliveries]

    # Zip deliveries and forms
    deliveries_with_forms = zip(deliveries, forms)

    if request.method == 'POST':
        delivery_id = request.POST.get('delivery_id')
        delivery = Delivery.objects.get(id=delivery_id)
        form = DeliveryStatusUpdateForm(request.POST, instance=delivery)

        if form.is_valid():
            form.save()
            send_delivery_update_email(delivery)
            if delivery.status == 'DELIVERED':
                mark_delivery_as_completed(delivery)
            messages.success(request, f"Delivery status for Tracking Number {delivery.tracking_number} updated successfully.")
            return redirect('all_deliveries')  # Refresh the page

    context = {
        'deliveries_with_forms': deliveries_with_forms,  # Pass zipped data
    }
    return render(request, 'store/deliveries.html', context)

@login_required
@non_driver_required
def user_delivery_status(request):
    # Get the customer associated with the logged-in user
    customer = request.user.customer

    # Get all deliveries associated with the customer
    deliveries = Delivery.objects.filter(customer=customer)

    context = {
        'deliveries': deliveries,
    }
    
    return render(request, 'store/user_delivery_status.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')




def driver_signup(request):
    if request.method == 'POST':
        form = DriverSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the driver after signing up
            send_driver_id(user)
            login(request, user)
            messages.success(request, f"Account created successfully. Your Driver ID is {user.username}!")
            return redirect('all_deliveries')  # Redirect to a driver dashboard or homepage
    else:
        form = DriverSignupForm()
    
    context = {
        'form': form
    }
    return render(request, 'store/driver_signup.html', context)



def driver_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if hasattr(user, 'deliverydriver'):
                login(request, user)
                messages.success(request, "Logged in successfully! ")
                return redirect('all_deliveries')  # Redirect to a driver-specific dashboard
            else:
                messages.error(request, "You are not registered as a delivery driver.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'store/driver_login.html')




def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully! ")
            return redirect('store')  # Redirect to a driver-specific dashboard
            
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'store/login.html')