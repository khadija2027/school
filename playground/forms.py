from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        label="Nom",
        widget=forms.TextInput(attrs={
            'placeholder': 'Votre nom complet',
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Votre adresse email',
            'class': 'form-control',
        })
    )
    message = forms.CharField(
        required=True,
        label="Message",
        widget=forms.Textarea(attrs={
            'placeholder': 'Votre message ici...',
            'class': 'form-control',
            'rows': 5,
        })
    )
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label="",
    )

    def clean_honeypot(self):
        """
        Valide le champ honeypot pour détecter les bots.
        Si le champ est rempli, considère que c'est un spam.
        """
        honeypot = self.cleaned_data.get('honeypot', '')
        if honeypot:
            raise forms.ValidationError("Spam détecté.")
        return honeypot
