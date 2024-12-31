from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Alumni,Deplome,Reseau,Histoire,Retour,News ,Event ,Prof,Equipe ,Prerequi ,Formati ,Objec
from django.views.generic.edit import CreateView , UpdateView ,DeleteView , FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages



class HOMEView(TemplateView):
    template_name = 'Acceuil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.objects.all()  # Tous les objets de News
        context['formatis'] = Formati.objects.all()  # Tous les objets de Formati
        context['contact_form'] = ContactForm()  # Ajouter le formulaire de contact
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Récupération des données du formulaire
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Vérification du champ honeypot
            honeypot = form.cleaned_data.get('honeypot')
            if honeypot:  # Si le champ honeypot est rempli, c'est un bot
                return HttpResponse("Erreur: spam détecté.")

            # Envoi de l'email
            try:
                send_mail(
                    subject=f'Contact de {name}',
                    message=f'Nom: {name}\\nEmail: {email}\\nMessage: {message}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['khadijaelmrabt2025@gmail.com'],
                    fail_silently=False,
                )
                return self.render_to_response({
                    'message_sent': True,
                    'contact_form': ContactForm(),  # Réinitialiser le formulaire après envoi
                    'news_list': News.objects.all(),
                    'formatis': Formati.objects.all(),
                })
            except Exception as e:
                return HttpResponse(f"Erreur lors de l'envoi de l'email : {e}")
        else:
            # Si le formulaire n'est pas valide, renvoyer les erreurs
            return self.render_to_response({
                'contact_form': form,
                'form_errors': form.errors,
                'news_list': News.objects.all(),
                'formatis': Formati.objects.all(),
            })


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    Model = News
    context_object_name = 'news'

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields =  '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
    
class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user =True
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        user = form.save()
        if user  :
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    def get(self, *args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterPage,self).get(*args,**kwargs)


class NewsList( ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()  # Récupère tous les objets News par défaut
        search_input = self.request.GET.get('search_area') or ''  # Si un terme de recherche est fourni
        if search_input:
            queryset = queryset.filter(title__startswith=search_input)  # Filtrer par titre
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
   
class NewssList(ListView):
    model = News
    template_name = 'NewsList.html'
    context_object_name = 'news'
    def get_queryset(self):
        queryset = super().get_queryset()  # Récupère tous les objets News par défaut
        theme_filter = self.request.GET.get('theme')  # Récupère le thème sélectionné dans la liste
        if theme_filter:
            queryset = queryset.filter(theme=theme_filter)  # Filtrer les actualités par thème
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['themes'] = sorted(set([theme.strip().lower() for theme in News.objects.values_list('theme', flat=True).distinct()])) # Liste des thèmes uniques
        context['selected_theme'] = self.request.GET.get('theme', '')  # Thème actuellement sélectionné
        context['news_list'] = News.objects.all() 
        context['formatis'] = Formati.objects.all() 
        return context
    
class NewsDetail(DetailView):
    model = News    
    template_name = 'news.html'
    context_object_name = 'news'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formatis'] = Formati.objects.all() 
        return context
    
class NewsCreate(CreateView):
    model = News
    fields = ['title','image','theme','lieu','date','content','publish']
    template_name = 'news_form.html'  
    success_url = reverse_lazy('news_list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NewsCreate,self).form_valid(form)

class NewsUpdate(UpdateView):
    model = News
    fields = ['title','image','theme','lieu','date','content','publish']
    template_name = 'news_form.html' 
    success_url = reverse_lazy('news_list')

class Newsdelete(DeleteView):
    model = News
    context_object_name = 'news'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('news_list')

class EventList(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset()  # Récupère tous les objets News par défaut
        search_input = self.request.GET.get('search_area') or ''  # Si un terme de recherche est fourni
        if search_input:
            queryset = queryset.filter(title__startswith=search_input)  # Filtrer par titre
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
   
class Events_List(ListView):
    model = Event
    template_name = 'EventsList.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset()  # Récupère tous les objets News par défaut
        theme_filter = self.request.GET.get('theme')  # Récupère le thème sélectionné dans la liste
        if theme_filter:
            queryset = queryset.filter(theme=theme_filter)  # Filtrer les actualités par thème
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['themes'] = sorted(set([theme.strip().lower() for theme in Event.objects.values_list('theme', flat=True).distinct()])) # Liste des thèmes uniques
        context['selected_theme'] = self.request.GET.get('theme', '')  # Thème actuellement sélectionné
        context['event_list'] = News.objects.all() 
        context['formatis'] = Formati.objects.all() 
        return context
            
    
class EventDetail(DetailView):
    model = Event    
    template_name = 'event.html'
    context_object_name = 'event'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formatis'] = Formati.objects.all()  # Tous les objets de Formati
        return context

class EventCreate(CreateView):
    model = Event
    fields = ['title','image','theme','content','lieu','event_start_date','event_finish_date','publish']
    template_name = 'event_form.html'  
    success_url = reverse_lazy('event_list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreate,self).form_valid(form)

class EventUpdate(UpdateView):
    model = Event
    fields = ['title','image','theme','content','lieu','event_start_date','event_finish_date','publish']
    template_name = 'event_form.html' 
    success_url = reverse_lazy('event_list')

class Eventdelete(DeleteView):
    model = Event
    context_object_name = 'event'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('event_list')

class EquipeList( ListView):
    model = Equipe
    template_name = 'equipe_list.html'
    context_object_name = 'Equipe'
    def get_queryset(self):
        queryset = super().get_queryset()  # Récupère tous les objets News par défaut
        search_input = self.request.GET.get('search_area') or ''  # Si un terme de recherche est fourni
        if search_input:
            queryset = queryset.filter(name__startswith=search_input)  # Filtrer par titre
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
    
   
class EquipesList(ListView):
    model = Equipe
    template_name = 'EquipeList.html'
    context_object_name = 'Equipe'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formatis'] = Formati.objects.all()  # Ajoute tous les objets Formati au contexte
        return context

    
class EquipeDetail(DetailView):
    model = Equipe   
    template_name = 'equipe.html'
    context_object_name = 'equipe'
  

class EquipeCreate(CreateView):
    model = Equipe
    fields = ['name','position','content','image','publish']
    template_name = 'equipe_form.html'  
    success_url = reverse_lazy('equipe_list')
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associer l'utilisateur authentifié
        return super(EquipeCreate, self).form_valid(form)  # Appel correct de super()

class EquipeUpdate(UpdateView):
    model = Equipe
    fields = ['name','position','content','image','publish']
    template_name = 'equipe_form.html' 
    success_url = reverse_lazy('equipe_list')

class Equipedelete(DeleteView):
    model = Equipe
    context_object_name = 'equipe'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('equipe_list')

class FormationList(ListView):
    model = Formati
    template_name = 'formation_list.html'
    context_object_name = 'formatis'
    def get_queryset(self):
        queryset = super().get_queryset()  # Récupère tous les objets News par défaut
        search_input = self.request.GET.get('search_area') or ''  # Si un terme de recherche est fourni
        if search_input:
            queryset = queryset.filter(name__startswith=search_input)  # Filtrer par titre
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context 

class FormationsList(ListView):
    model = Formati
    template_name = 'Acceuil.html'
    context_object_name = 'formatis'

class FormationDetail(DetailView):
    model = Formati
    template_name = 'formation.html'
    context_object_name = 'formati'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profs'] = self.object.prof.all()  # Accès à la relation ManyToMany
        context['prerequisites'] = self.object.prerequi.all()
        context['Objec'] = self.object.obj.all()
        context['formatis'] = Formati.objects.all()  # Tous les objets de Formati
        return context


class FormationForm(forms.ModelForm):
    class Meta:
        model = Formati
        fields = ['name','description','presentation','formation_type','im','ima','imag','obj','prof','prerequi','conditions_access','programme']
        widgets = {
            'obj': forms.CheckboxSelectMultiple(),  # Affiche des cases à cocher
            'prof': forms.CheckboxSelectMultiple(),
            'prerequi': forms.CheckboxSelectMultiple(),
        }

class FormationCreate(CreateView):
    model = Formati
    form_class = FormationForm
    template_name = 'formation_form.html'
    success_url = reverse_lazy('formation_list')
    def form_valid(self, form):
        print("FILES reçus :", self.request.FILES)
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class FormationUpdate(UpdateView):
    model = Formati
    form_class = FormationForm
    template_name = 'formation_form.html'
    success_url = reverse_lazy('formation_list')

class Formationdelete(DeleteView):
    model = Formati
    context_object_name = 'formati'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('formation_list')

class ProfList(ListView):
    model = Prof
    template_name = 'prof_list.html'
    context_object_name = 'profs'
    def get_queryset(self):
        queryset = super().get_queryset()  # Récupère tous les objets News par défaut
        search_input = self.request.GET.get('search_area') or ''  # Si un terme de recherche est fourni
        if search_input:
            queryset = queryset.filter(name__startswith=search_input)  # Filtrer par titre
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
    
   
class ProfsList(ListView):
    model = Prof
    template_name = 'ProfsList.html'
    context_object_name = 'profs'

    
class ProfDetail(DetailView):
    model = Prof
    template_name = 'prof.html'
    context_object_name = 'prof'
  

class ProfCreate(CreateView):
    model = Prof
    fields = ['name','position','image']
    template_name = 'prof_form.html'  
    success_url = reverse_lazy('prof_list')
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associer l'utilisateur authentifié
        return super(ProfCreate, self).form_valid(form)  # Appel correct de super()

class ProfUpdate(UpdateView):
    model = Prof
    fields = ['name','position','image']
    template_name = 'prof_form.html' 
    success_url = reverse_lazy('prof_list')

class Profdelete(DeleteView):
    model = Prof
    context_object_name = 'prof'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('prof_list')

class ObjectifList(ListView):
    model = Objec
    template_name = 'objectif_list.html'
    context_object_name = 'Objec'  # Use plural and lowercase
    def get_queryset(self):
        queryset = super().get_queryset()  # Get all Objectif instances by default
        search_input = self.request.GET.get('search_area') or ''  # Get search input, default to empty string
        if search_input:
            queryset = queryset.filter(title__startswith=search_input)  # Filter by title
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')  # Add search input to context
        return context
    
   
class ObjectifsList(ListView):
    model = Objec
    template_name = 'ObjectifList.html'
    context_object_name = 'Objec'

    
class ObjectifDetail(DetailView):
    model = Objec
    template_name = 'objectif.html'
    context_object_name = 'objec'
  

class ObjectifCreate(CreateView):
    model = Objec
    fields = ['title','description']
    template_name = 'objectif_form.html'  
    success_url = reverse_lazy('objectif_list')
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associer l'utilisateur authentifié
        return super(ObjectifCreate, self).form_valid(form)  # Appel correct de super()
  
    
class ObjectifUpdate(UpdateView):
    model = Objec
    fields = ['title','description']
    template_name = 'objectif_form.html' 
    success_url = reverse_lazy('objectif_list')

class Objectifdelete(DeleteView):
    model = Objec
    context_object_name = 'Objec'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('objectif_list')

class PrerequisiteList( ListView):
    model = Prerequi
    template_name = 'prerequisite_list.html'
    context_object_name = 'Prerequisites'
    def get_queryset(self):
        queryset = super().get_queryset()  # Récupère tous les objets News par défaut
        search_input = self.request.GET.get('search_area') or ''  # Si un terme de recherche est fourni
        if search_input:
            queryset = queryset.filter(description__startswith=search_input)  # Filtrer par titre
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context

    
class PrerequisiteDetail(DetailView):
    model = Prerequi
    template_name = 'prerequisite.html'
    context_object_name = 'prerequisite'
  

class PrerequisiteCreate(CreateView):
    model = Prerequi
    fields = ['description']
    template_name = 'prerequisite_form.html'  
    success_url = reverse_lazy('prerequisite_list')
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associer l'utilisateur authentifié
        return super(PrerequisiteCreate, self).form_valid(form)  # Appel correct de super()

class PrerequisiteUpdate(UpdateView):
    model = Prerequi
    fields = ['description']
    template_name = 'prerequisite_form.html' 
    success_url = reverse_lazy('prerequisite_list')

class Prerequisitedelete(DeleteView):
    model = Prerequi
    context_object_name = 'prerequisite'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('prerequisite_list')    

class RetourList( ListView):
    model = Retour
    template_name = 'retour_list.html'
    context_object_name = 'retours'
    def get_queryset(self):
        queryset = super().get_queryset()  # Récupère tous les objets News par défaut
        search_input = self.request.GET.get('search_area') or ''  # Si un terme de recherche est fourni
        if search_input:
            queryset = queryset.filter(name__startswith=search_input)  # Filtrer par titre
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context

    
class RetourDetail(DetailView):
    model = Retour
    template_name = 'retour.html'
    context_object_name = 'retour'
  

class RetourCreate(CreateView):
    model = Retour
    fields = ['name','comment']
    template_name = 'retour_form.html'  
    success_url = reverse_lazy('retour_list')
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associer l'utilisateur authentifié
        return super(RetourCreate, self).form_valid(form)  # Appel correct de super()


class RetourUpdate(UpdateView):
    model = Retour
    fields = ['name','comment']
    template_name = 'retour_form.html' 
    success_url = reverse_lazy('retour_list')

class Retourdelete(DeleteView):
    model = Retour
    context_object_name = 'retour'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('retour_list')   

class HistoireList(ListView):
    model = Histoire
    template_name = 'histoire_list.html'
    context_object_name = 'histoires'  # Use plural and lowercase
    def get_queryset(self):
        queryset = super().get_queryset()  # Get all Objectif instances by default
        search_input = self.request.GET.get('search_area') or ''  # Get search input, default to empty string
        if search_input:
            queryset = queryset.filter(title__startswith=search_input)  # Filter by title
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')  # Add search input to context
        return context
    
    
class HistoireDetail(DetailView):
    model = Histoire
    template_name = 'histoire.html'
    context_object_name = 'histoire'
  

class HistoireCreate(CreateView):
    model = Histoire
    fields = ['title','content']
    template_name = 'histoire_form.html'  
    success_url = reverse_lazy('histoire_list')
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associer l'utilisateur authentifié
        return super(HistoireCreate, self).form_valid(form)  # Appel correct de super()
  
    
class HistoireUpdate(UpdateView):
    model = Histoire
    fields = ['title','content']
    template_name = 'histoire_form.html' 
    success_url = reverse_lazy('histoire_list')

class Histoiredelete(DeleteView):
    model = Histoire
    context_object_name = 'histoire'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('histoire_list')

class ReseauList(ListView):
    model = Reseau
    template_name = 'reseau_list.html'
    context_object_name = 'reseaus'
    def get_queryset(self):
        queryset = super().get_queryset()  # Récupère tous les objets News par défaut
        search_input = self.request.GET.get('search_area') or ''  # Si un terme de recherche est fourni
        if search_input:
            queryset = queryset.filter(name__startswith=search_input)  # Filtrer par titre
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context

    
class ReseauDetail(DetailView):
    model = Reseau
    template_name = 'reseau.html'
    context_object_name = 'reseau'
  

class ReseauCreate(CreateView):
    model = Reseau
    fields = ['name','poste']
    template_name = 'reseau_form.html'  
    success_url = reverse_lazy('reseau_list')
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associer l'utilisateur authentifié
        return super(ReseauCreate, self).form_valid(form)  # Appel correct de super()

class ReseauUpdate(UpdateView):
    model = Reseau
    fields = ['name','poste']
    template_name = 'reseau_form.html' 
    success_url = reverse_lazy('reseau_list')

class Reseaudelete(DeleteView):
    model = Reseau
    context_object_name = 'reseau'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('reseau_list')

class DeplomeList(ListView):
    model = Deplome
    template_name = 'deplome_list.html'
    context_object_name = 'deplomes'  # Use plural and lowercase
    def get_queryset(self):
        queryset = super().get_queryset()  # Get all Objectif instances by default
        search_input = self.request.GET.get('search_area') or ''  # Get search input, default to empty string
        if search_input:
            queryset = queryset.filter(name__startswith=search_input)  # Filter by title
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')  # Add search input to context
        return context
    
    
class DeplomeDetail(DetailView):
    model = Deplome
    template_name = 'deplome.html'
    context_object_name = 'deplome'
  

class DeplomeCreate(CreateView):
    model = Deplome
    fields = ['name','poste','promo','image']
    template_name = 'deplome_form.html'  
    success_url = reverse_lazy('deplome_list')
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associer l'utilisateur authentifié
        return super(DeplomeCreate, self).form_valid(form)  # Appel correct de super()
  
    
class DeplomeUpdate(UpdateView):
    model = Deplome
    fields = ['name','poste','promo','image']
    template_name = 'deplome_form.html' 
    success_url = reverse_lazy('deplome_list')

class Deplomedelete(DeleteView):
    model = Deplome
    context_object_name = 'deplome'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('deplome_list')

class AlumniDetail(TemplateView):
    template_name = 'alumni.html'
    context_object_name = 'alumni'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Charger l'unique instance de Alumni
        context['alumni'] = get_object_or_404(Alumni)
        context['retours'] = context['alumni'].retour.all()
        context['histoires'] = context['alumni'].histoire.all()
        context['reseaus'] = context['alumni'].reseau.all()
        context['deplomes'] = context['alumni'].deplome.all()
        context['formatis'] = Formati.objects.all()  # Tous les objets de Formati
        return context

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['NbL', 'echange', 'insertion', 'retour', 'histoire', 'reseau', 'deplome']
        widgets = {
            'retour': forms.CheckboxSelectMultiple(),  # Affiche des cases à cocher
            'histoire': forms.CheckboxSelectMultiple(),
            'reseau': forms.CheckboxSelectMultiple(),
            'deplome': forms.CheckboxSelectMultiple(),
        }

class AlumniUpdate(UpdateView):
    model = Alumni
    form_class = AlumniForm
    template_name = 'alumni_form.html'
    success_url = reverse_lazy('alumni_detail')

    def get_object(self, queryset=None):
        alumni, created = Alumni.objects.get_or_create(id=1)
        return alumni
    

class Alumnidelete(DeleteView):
    model = Alumni
    context_object_name = 'alumni'
    template_name = 'alumni_delete.html' 
    success_url = reverse_lazy('alumni_list')       

def faculte(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'faculte.html', {'formatis': formatis})  

def mot_president(request):
    return render(request, 'mot_president.html')    
  
def avis(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'avis.html', {'formatis': formatis})

def bda(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'bda.html', {'formatis': formatis})
  
def bde(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'bde.html', {'formatis': formatis})

def club(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'clubs.html', {'formatis': formatis})  
 
def ecole(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'ecole.html', {'formatis': formatis})  
def eservice(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'eservice.html', {'formatis': formatis})  
def partein(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'partenaire_in.html', {'formatis': formatis}) 
def partelocaux(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'partenaire_lo.html', {'formatis': formatis}) 
def recrutement(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'recrutement.html', {'formatis': formatis}) 
def reglements(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'reglement.html', {'formatis': formatis})
def stage(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'stage.html', {'formatis': formatis})
def viesportive(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'viesportive.html', {'formatis': formatis})
def equipement(request):
    formatis = Formati.objects.all()  # Tous les objets de Formati
    return render(request, 'equipements.html', {'formatis': formatis})


  
 

