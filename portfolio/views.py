from django.views.generic import TemplateView, ListView, DetailView
from .models import Profile, Service
from django.contrib.auth import get_user_model
import datetime
import math
# from django.utils.decorators import method_decorator
# from django.views.decorators.clickjacking import xframe_options_exempt


class IndexView(TemplateView):
    template_name = 'index.html'

def get_age(self):
    today = int(datetime.date.today().strftime('%Y%m%d'))
    birth = int(self.date_of_birth.strftime('%Y%m%d'))
    age = math.floor((today - birth) / 10000)
    return age

class AboutMeView(DetailView):
    template_name = 'about_me.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['age'] = get_age(context['profile'])
        context['services'] = Service.objects.prefetch_related('skills').filter(developer=context['profile'])
        context['num_services'] = len(context['services'])
        context['num_skill_category'] = 4

        # 開発に使用したスキルをカテゴリごとにまとめる
        my_skills = {i: [] for i in range(context['num_skill_category'])} 
        for service in context['services']:
            skills = service.skills.all()   # 各サービスで使用したスキル
            
            for skill in skills:
                if skill.name not in my_skills[skill.category]:
                    my_skills[skill.category].append(skill.name)

        for i,j in my_skills.items():
            # 使用した全スキルリスト（カテゴリ関係なし）
            all_skills = [s for t in my_skills.values() for s in t if s is not None]
            if i==1:
                context['languages'] = j
            elif i==2:
                context['frameworks'] = j
            else:
                context['others'] = j
        context['skills'] = all_skills
        return context

@method_decorator(xframe_options_exempt, name='dispatch')
class ServiceView(ListView):
    template_name = 'services.html'
    model = Service
    context_object_name = 'services'

    def get_queryset(self, **kwargs):
        user = get_user_model().objects.get(pk=1)
        qs = super().get_queryset(**kwargs).filter(developer=user.profile)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

