from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
class News(models.Model):
    THEME_CHOICES = [
         ('Aasociations', 'Associations'),
         ('compétition','Compétition'),
        ('conférence', 'Conférence'),
        ('distinction',' Distinction'),
         ('ecole', 'Ecole'),
         ('entreprises', 'Entreprises'),
         ('entreprenariat', 'Entreprenariat'),
        ('formations', 'Formations'),
        ('international', 'International'),
        
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(null=True ,max_length=200)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='news_images/',null=True)
    theme = models.CharField(max_length=50, choices=THEME_CHOICES , null=True, blank=True)
    publish = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    lieu = models.CharField(null=True ,max_length=200)
    date = models.DateTimeField(null=True) 
    def __str__(self):
        return self.title
    class Meta:
        ordering =['publish','created']

class Event(models.Model):
    THEME_CHOICES = [
         ('Associations', 'Associations'),
        ('artistique',' Artistique'),
         ('compétition', 'Compétition'),
        ('conférence', 'Conférence'),
         ('ecole', 'Ecole'),
         ('entreprises', 'Entreprises'),
         ('entreprenariat', 'Entreprenariat'),
        ('formations', 'Formations'),
        ('sportif',' Sportif'),
        ('international', 'International'),
        
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='events_images/',null=True,)
    theme = models.CharField(max_length=50, choices=THEME_CHOICES , null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    event_start_date = models.DateTimeField(null=True) 
    event_finish_date = models.DateTimeField(null=True)
    publish = models.BooleanField(default=False) 
    lieu = models.CharField(null=True ,max_length=200)
    def __str__(self):
        return self.title
    def is_upcoming(self):
        return self.event_finish_date > timezone.now()  
    class Meta:
        ordering =['created','publish','event_finish_date']

class Equipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200 , null=True)
    position = models.CharField(max_length=200,null=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='equipe_images/',null=True)
    publish = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    class Meta:
        ordering =['publish']

      
class Objectif(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.title

class Prerequi(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.description    
    
class Prof(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True)
    position = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='professors/',null=True)

    def __str__(self):
        return self.name
    
class Objec(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title
    
class Formati(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    description=models.TextField(null=True) 
    presentation=models.TextField(null=True)
    formation_type = models.CharField(max_length=50, null=True)  # Plus flexible
    im = models.ImageField(upload_to='formations/', null=True)
    ima = models.ImageField(upload_to='formations/', null=True)
    imag = models.ImageField(upload_to='formations/', null=True)
    obj = models.ManyToManyField(Objec)
    prof = models.ManyToManyField(Prof)
    prerequi = models.ManyToManyField(Prerequi)
    conditions_access = models.FileField(upload_to='formations/documents/',  blank=True)
    programme = models.FileField(upload_to='formations/documents/', blank=True)
    def __str__(self):
        return self.name
  


class Formation(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    formation_type = models.CharField(max_length=50, null=True)  # Plus flexible
    image = models.ImageField(upload_to='formations/', null=True)
    obj = models.ManyToManyField(Objec)
    def __str__(self):
        return self.name

class FormationObjec(models.Model):
    formation = models.ForeignKey(Formati, on_delete=models.CASCADE)
    objec = models.ForeignKey(Objec, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.objec.title} - {self.formation.name}"
   
class FormationProf(models.Model):
    formation = models.ForeignKey(Formati, on_delete=models.CASCADE)
    prof = models.ForeignKey(Prof, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.prof.name} - {self.formation.name}"


class FormationPrerequi(models.Model):
    formation = models.ForeignKey(Formati, on_delete=models.CASCADE)
    prerequi = models.ForeignKey(Prerequi, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.prerequi.description} - {self.formation.name}"
    
class Retour(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return self.name  
    
class Histoire(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100,null=True)
    content = models.TextField(null=True)

    def __str__(self):
        return self.title

class Reseau(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True)
    poste = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name
    
class Deplome(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True)
    poste = models.CharField(max_length=100,null=True)
    promo = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='deplomes/', null=True)

    def __str__(self):
        return self.name
      
class Alumni(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    NbL = models.FloatField(null=True)  
    echange = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        null=True
    )  # Nombre positif entre 1 et 100
    insertion = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        null=True
    )  # Nombre positif entre 1 et 100
    retour = models.ManyToManyField(Retour)
    histoire = models.ManyToManyField(Histoire)
    reseau = models.ManyToManyField(Reseau)
    deplome = models.ManyToManyField(Deplome)
    def __Str__(self):
        return f"NbL: {self.NbL}"
    
class AlumniRetour(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    retour = models.ForeignKey(Retour, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.retour.name} - {self.alumni.NbL}"    
    
class AlumniHistoire(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    histoire = models.ForeignKey(Histoire, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.histoire.title} - {self.alumni.NbL}"        
    
class AlumniReseau(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    reseau = models.ForeignKey(Reseau, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reseau.name} - {self.alumni.NbL}" 

class AlumniDeplome(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    deplome = models.ForeignKey(Deplome, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.deplome.name} - {self.alumni.NbL}"    

class Partenaire(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='partenaires/',null=True)

    def __str__(self):
        return self.name            

class Sport(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='sports/',null=True)

    def __str__(self):
        return self.title  

class Clubs (models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, unique=True)  # Nom du club, unique
    image = models.ImageField(upload_to='club_images/', null=True, blank=True)  # Image du club
    instagram_link = models.URLField(max_length=200, null=True, blank=True)  # Lien Instagram

    def __str__(self):
        return self.name

class Club(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True  )
    clubs = models.ManyToManyField(Clubs)
    def __str__(self):
        return self.description            
    
class ClubClubs(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    clubs = models.ForeignKey(Clubs, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.clubs.name} - {self.club.description}" 

class MissionBDA (models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    title= models.CharField(max_length=100, null=False)  # Nom du club, unique
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

class BDA (models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    titre = models.CharField(max_length=100, null=False)
    paragraphe = models.TextField(null=True) 
    MotPresident = models.TextField(null=True) 
    Presidentname = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True) 
    mission = models.ManyToManyField(MissionBDA)
    def __str__(self):
        return self.titre  

class BDAMission(models.Model):
    bda = models.ForeignKey(BDA, on_delete=models.CASCADE)
    mission = models.ForeignKey(MissionBDA, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mission.title} - {self.bda.titre}" 

class MissionBDE (models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    title= models.CharField(max_length=100, null=False)  # Nom du club, unique
    description = models.TextField(null=True)

    def __str__(self):
        return self.title
    
class PartenaireBDE (models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    title= models.CharField(max_length=100, null=False)  # Nom du club, unique
    image = models.ImageField(upload_to='partenairebdes_images/', null=True, blank=True)  # Image du club
    description = models.TextField(null=True)

    def __str__(self):
        return self.title    

class BDE (models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True) 
    mission = models.ManyToManyField(MissionBDE)
    partenaire = models.ManyToManyField(PartenaireBDE)
    instagram_link = models.URLField(max_length=200, null=True, blank=True)  # Lien Instagram
    facebook_link = models.URLField(max_length=200, null=True, blank=True)  # Lien Instagram
    tiktok_link = models.URLField(max_length=200, null=True, blank=True)  # Lien Instagram
    def __str__(self):
        return self.description 
    
   
class BDEMission(models.Model):
    bde = models.ForeignKey(BDA, on_delete=models.CASCADE)
    mission = models.ForeignKey(MissionBDE, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mission.title} - {self.bde.description}" 
    
class BDEParteanire (models.Model):  
    bde = models.ForeignKey(BDE, on_delete=models.CASCADE)
    partenaire = models.ForeignKey(PartenaireBDE, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.partenaire.title} - {self.bde.description}"