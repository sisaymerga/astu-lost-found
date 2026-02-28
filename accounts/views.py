from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ItemForm
from .models import Item, Category, Claim
from django.db.models import Q
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

def home(request):
    items = Item.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    status = request.GET.get('status')

    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        items = items.filter(category_id=category_id)
    if status:
        items = items.filter(status=status)
    paginator = Paginator(items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'selected_status': status,
        'query': query,
    }
    return render(request, 'accounts/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def report_item(request):
    initial_data = {}
    if request.GET.get('status') in ['lost', 'found']:
        initial_data['status'] = request.GET.get('status')
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Item reported successfully!')
            return redirect('home')
    else:
        form = ItemForm(initial=initial_data)
    
    return render(request, 'accounts/report_item.html', {'form': form})
@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('home')
    else:
        form = ItemForm(instance=item)
    return render(request, 'accounts/edit_item.html', {'form': form, 'item': item})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('home')
    return render(request, 'accounts/delete_item.html', {'item': item})


@login_required
def submit_claim(request, item_id):
    item = Item.objects.get(id=item_id, status='found')
    
    if request.method == 'POST':
        message = request.POST.get('message')
        Claim.objects.create(
            item = item,
            user = request.user,
            message = message
        )
        messages.success(request, 'Claim submitted succsessfuly!')
        return redirect('home')

    return render(request, 'accounts/submit_claim.html', {'item': item})
@login_required
def dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    total_lost = Item.objects.filter(status='lost').count()
    total_found = Item.objects.filter(status='found').count()
    total_claimed = Item.objects.filter(status='claimed').count()
    total_resolved = Item.objects.filter(status='resolved').count()
    pending_claims = Claim.objects.filter(status='pending').count()

    context = {
        'total_lost': total_lost,
        'total_found': total_found,
        'total_claimed': total_claimed,
        'total_resolved': total_resolved,
        'pending_claims': pending_claims,
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required
def my_claims(request):
    claims = Claim.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/my_claims.html', {'claims': claims})
def security_report(request):
    return render(request, 'accounts/security_report.html')

def custom_logout(request):
    logout(request)
    return redirect('login')

@staff_member_required
def manage_claims(request):
    claims = Claim.objects.all().order_by('-created_at')
    return render(request, 'accounts/manage_claims.html', {'claims': claims})

@staff_member_required
def approve_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    claim.status = 'approved'
    claim.save()
    item = claim.item
    item.status = 'claimed'
    item.save()
    messages.success(request, f'Claim for "{item.title}" approved.')
    return redirect('manage_claims')

@staff_member_required
def reject_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    claim.status = 'rejected'
    claim.save()
    messages.success(request, f'Claim for "{claim.item.title}" rejected.')
    return redirect('manage_claims')