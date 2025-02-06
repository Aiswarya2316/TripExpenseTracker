from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password


def get_admin(request):
    """Retrieve the logged-in staff object from the session."""
    if 'admin' not in request.session:
        return None  
    try:
        return adminregister.objects.get(email=request.session['admin'])
    except adminregister.DoesNotExist:
        return None

def get_user(request):
    """Retrieve the logged-in staff object from the session."""
    if 'user' not in request.session:
        return None  
    try:
        return userregister.objects.get(email=request.session['user'])
    except userregister.DoesNotExist:
        return None

def adminregisterr(request):
     if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        password = request.POST['password']       
        if adminregister.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken!")
            return redirect('adminregisterr')
        admin = adminregister(email=email, name=name, phone=phone, password=password)
        admin.save()
        user = User.objects.create_user(username=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        messages.success(request, "Admin registered successfully!")
        return redirect('adminlogin')
     return render(request,'admin/adminregister.html')

def userregisterr(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Password confirmation check
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('userregister')

        # Email format validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Invalid email format!")
            return redirect('userregister')

        # Check if email is already registered
        if userregister.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('userregister')

        # Create a User instance
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name  # Save the name to the User model
        user.save()

        # Create userregister instance and associate it with the created user
        user_register = userregister(user=user, email=email, phone=phone, location=location, confirm_password=confirm_password)
        user_register.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('userlogin')

    return render(request, 'user/userregister.html')

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        print(password)
        try:
            admin = adminregister.objects.get(email=email , password=password)
            request.session['admin'] = admin.email
            return redirect('adminhome')             
        except adminregister.DoesNotExist:
            messages.error(request, "No admin account found with this email!")
            return redirect('adminlogin')
    return render(request, 'admin/adminlogin.html')
    

def userlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate the user using Django's built-in authenticate method
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Login the user if authentication is successful
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('userhome')  # Redirect to home page or any other page
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid email or password.")
            return redirect('userlogin')

    return render(request, 'user/userlogin.html')



def userlogout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')  

def adminlogout(request):
    logout(request)
    messages.success(request, "Admin logged out successfully!")
    return redirect('home')


def home(request):
    return render(request,'home.html')

def adminhome(request):
    return render(request,'admin/adminhome.html')

def userhome(request):
    return render(request,'user/userhome.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ExpenseGroup, userregister  # Import your models properly

@login_required
def addgroup(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        
        # Get the associated userregister instance for the logged-in user
        try:
            user_register_instance = userregister.objects.get(user=request.user)
        except userregister.DoesNotExist:
            messages.error(request, "User registration details not found.")
            return redirect('home')

        if not group_name or not group_name.strip():  # Ensure no empty or whitespace-only names
            messages.error(request, "Group name cannot be empty!")
            return redirect('addgroup')

        # Check if the group name already exists for this user
        if ExpenseGroup.objects.filter(name=group_name, created_by=request.user).exists():
            messages.error(request, f'Group "{group_name}" already exists!')
            return redirect('addgroup')

        # Create the new group
        ExpenseGroup.objects.create(name=group_name, created_by=request.user)
        messages.success(request, f'Group "{group_name}" created successfully!')
        return redirect('viewgroup')

    # Handle GET requests properly
    return render(request, 'user/addgroup.html')



@login_required
def viewgroup(request):
    # Get all groups created by the logged-in user
    user_groups = ExpenseGroup.objects.filter(created_by=request.user)
    return render(request, 'user/viewgroup.html', {'user_groups': user_groups})




@login_required
def addgroupmember(request):
    if request.method == "POST":
        group_id = request.POST.get("group_id")
        member_name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")

        # Ensure all fields are provided
        if not group_id or not member_name or not phone_number:
            messages.error(request, "All fields are required!")
            return redirect("addgroupmember")

        # Validate phone number
        if not phone_number.isdigit():
            messages.error(request, "Phone number must contain only digits!")
            return redirect("addgroupmember")

        try:
            group = ExpenseGroup.objects.get(id=group_id, created_by=request.user)  # Ensure group belongs to the user
        except ExpenseGroup.DoesNotExist:
            messages.error(request, "Invalid group selection!")
            return redirect("addgroupmember")

        # Add the new member to the group
        GroupMember.objects.create(group=group, name=member_name, phone_number=phone_number)

        messages.success(request, f"Member '{member_name}' added to group '{group.name}'!")
        return redirect("viewgroupmember")  # Redirect to group list or member list

    # Fetch groups created by the logged-in user
    user_groups = ExpenseGroup.objects.filter(created_by=request.user)

    return render(request, "user/addgroupmember.html", {"user_groups": user_groups})


@login_required
def viewgroupmember(request):
    # Get the list of groups created by the logged-in user
    user_groups = ExpenseGroup.objects.filter(created_by=request.user)
    
    group_id = request.GET.get("group_id")  # Get the selected group ID from request
    members = None
    selected_group = None

    if group_id:
        try:
            selected_group = ExpenseGroup.objects.get(id=group_id, created_by=request.user)
            members = GroupMember.objects.filter(group=selected_group)  # Fetch members of selected group
        except ExpenseGroup.DoesNotExist:
            messages.error(request, "Invalid group selection!")
            return redirect("viewgroupmember")

    return render(request, "user/viewgroupmember.html", {
        "user_groups": user_groups,
        "members": members,
        "selected_group": selected_group
    })

from decimal import Decimal

@login_required
def addexpense(request):
    if request.method == 'POST':
        # Get form data (group, title, amount, date)
        group_id = request.POST.get('group')
        title = request.POST.get('title')
        amount = request.POST.get('amount')  # This will be a string
        date = request.POST.get('date')

        # Convert amount to Decimal
        amount = Decimal(amount)

        # Get the group and its members
        group = ExpenseGroup.objects.get(id=group_id)
        members = GroupMember.objects.filter(group=group)

        # Ensure userregister instance is used for paid_by
        user_register = userregister.objects.get(user=request.user)

        # Create the expense
        expense = Expense.objects.create(
            title=title,
            amount=amount,
            date=date,
            group=group,
            paid_by=user_register  # Pass the userregister instance
        )

        # Calculate the share for each member
        amount_per_member = amount / len(members)

        # Split the expense among group members
        for member in members:
            ExpenseSplit.objects.create(
                expense=expense,
                member=member,
                amount=amount_per_member
            )

        # Redirect to some page (e.g., expense list)
        return redirect('viewexpense')  # Replace with the actual URL

    # If GET request, just display the add expense form
    groups = ExpenseGroup.objects.all()
    return render(request, 'user/addexpense.html', {'groups': groups})


@login_required
def viewexpense(request):
    # Get all expenses for the user or for a specific group
    expenses = Expense.objects.all()

    expense_data = []
    for expense in expenses:
        # Get the group name
        group_name = expense.group.name  # Assuming the group has a 'name' field
        
        # Get the members and their respective share
        splits = ExpenseSplit.objects.filter(expense=expense)
        member_share = {}
        
        for split in splits:
            member_share[split.member.name] = split.amount
        
        expense_data.append({
            'expense': expense,
            'group_name': group_name,
            'splits': member_share
        })

    return render(request, 'user/viewexpense.html', {'expense_data': expense_data})


from django.shortcuts import render
from .models import userregister

def viewusers(request):
    users = userregister.objects.all()  
    return render(request, 'admin/viewusers.html', {'users': users})



@login_required
def viewexpenses(request):
    users = userregister.objects.all()
    user_expenses = []
    for user in users:
        expenses = Expense.objects.filter(user=user.user)
        user_expenses.append({
            'user': user,
            'expenses': expenses
        })
    return render(request, 'admin/viewexpenses.html', {'user_expenses': user_expenses})


