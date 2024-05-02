from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from contact.forms import ContactForm
from contact.models import Contact


@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')

    # Checa se o metódo é igual a POST
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        context = {
            'forms': form,
            'form_action': form_action
        }

        # Salva contatos
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect('contact:update', contact_id=contact.pk)

        return render(request, 'contact/create.html', context)

    context = {
        'forms': ContactForm(),
        'form_action': form_action
    }

    return render(request, 'contact/create.html', context)


@login_required(login_url='contact:login')
def update(request, contact_id):
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user)
    form_action = reverse('contact:update', args=(contact_id,))

    # Checa se o metódo é igual a POST
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)

        context = {
            'forms': form,
            'form_action': form_action
        }

        # Atualiza contatos
        if form.is_valid():
            contact = form.save()
            # Possível manipular dados
            return redirect('contact:update', contact_id=contact.pk)

        return render(request, 'contact/create.html', context)

    context = {
        'forms': ContactForm(instance=contact),
        'form_action': form_action
    }

    return render(request, 'contact/create.html', context)


def delete(request, contact_id):
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user)
    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')

    return render(request, 'contact/contact.html', {
        'contact': contact,
        'confirmation': confirmation,
    })
