from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Customer
from .forms import CustomerForm

def customer_list(request):
    customers = Customer.objects.all()
    form = CustomerForm()
    return render(request, 'crm/customer_list.html', {'customers': customers, 'form': form})

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return JsonResponse({
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone
            })
    return JsonResponse({'error': 'Invalid form data'}, status=400)

def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'crm/edit_customer.html', {'form': form, 'customer': customer})

def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'crm/delete_customer.html', {'customer': customer})