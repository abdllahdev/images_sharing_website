from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import generic as generic_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Profile

from .forms import AccountCreateForm, AccountUpdateForm, ProfileUpdateForm
from common.decorators import ajax_required
from actions.models import Action
from actions.utils import create_action


class AccountCreateView(generic_views.FormView):
    form_class = AccountCreateForm
    template_name = 'accounts/account_create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super(AccountCreateView, self).form_valid(form)


class AccountUpdateView(LoginRequiredMixin, generic_views.TemplateView):
    template_name = 'accounts/account_update.html'

    def post(self, request):
        account_update_form = AccountUpdateForm(instance=request.user,
                                                data=request.POST)
        profile_update_form = ProfileUpdateForm(instance=request.user.user_profile,
                                                data=request.POST,
                                                files=request.FILES)

        if account_update_form.is_valid and profile_update_form.is_valid:
            account_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Account updated successfully')
            return redirect(reverse('account_update'))
        messages.error(request, 'Error updating your account')
        return redirect(reverse('account_update'))

    def get_context_data(self, **kwargs):
        context = super(AccountUpdateView, self).get_context_data(**kwargs)
        context['account_update_form'] = AccountUpdateForm(instance=self.request.user)
        context['profile_update_form'] = ProfileUpdateForm(instance=self.request.user.user_profile)
        return context


class DashboardView(LoginRequiredMixin, generic_views.TemplateView, ):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        actions = Action.objects.all().exclude(user=self.request.user)
        following_ids = self.request.user.following.values_list('id', flat=True)
        if following_ids:
            actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__user_profile').prefetch_related('target')
        actions = actions[:10]
        context['actions'] = actions
        return context


class AccountListView(generic_views.ListView):
    model = User
    template_name = 'accounts/account_list.html'

    def get_queryset(self):
        return User.objects.filter(is_active=True).select_related('user_profile')


class AccountDetailView(generic_views.DetailView):
    model = User
    template_name = 'accounts/account_detail.html'


class FollowView(LoginRequiredMixin, generic_views.View):
    def post(self, request):
        if request.is_ajax():
            user_id = request.POST.get('id')
            action = request.POST.get('action')
            if user_id and action:
                try:
                    user = User.objects.get(id=user_id)
                    if action == 'follow':
                        user.followers.add(request.user)
                        create_action(request.user, 'follows', target=user)
                    elif action == 'unfollow':
                        user.followers.remove(request.user)
                    return JsonResponse({'status': True})
                except:
                    pass
        else:
            return HttpResponseBadRequest()


class FollowersFollowingView(LoginRequiredMixin, generic_views.TemplateView):
    template_name = 'accounts/followers_following.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FollowersFollowingView, self).get_context_data(*args, **kwargs)
        user = User.objects.filter(username=kwargs['username']).first()

        if kwargs['type'] == 'followers':
            context['users'] = user.followers.all().select_related('user_profile')
        elif kwargs['type'] == 'following':
            context['users'] = user.following.all().select_related('user_profile')

        context['type'] = kwargs['type'].title
        context['username'] = kwargs['username']
        return context
    
