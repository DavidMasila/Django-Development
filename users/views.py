from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
# Create your views here.


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Account created! Please log in')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created! Please log in')
        return response

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # added request.FILES because of the form data type we receive for profile update
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Account details updated successfully')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

# class ProfileUpdateView(LoginRequiredMixin,UpdateView):
#     form_class = UserUpdateForm
#     template_name='users/profile.html'
#     success_url =reverse_lazy('profile')

#     def get_object(self, queryset=None):
#         return self.request.user.profile
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['u_form'] = UserUpdateForm(instance=self.request.user)
#         return context
    
#     def form_valid(self, form):
#         u_form = UserUpdateForm(self.request.POST, instance=self.request.user)
#         if u_form.is_valid() and form.is_valid():
#             u_form.save()
#             form.save()
#             messages.success(self.request, 'Account details updated successfully')
#             return redirect('profile')
#         return self.render_to_response(self.get_context_data(form=form))


