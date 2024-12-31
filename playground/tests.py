from django.core.mail import send_mail
from django.test import TestCase
from django.core import mail
from django.conf import settings

class EmailTest(TestCase):
    def test_send_email(self):
        # Envoi d'un email de test
        subject = 'Test SMTP'
        message = 'Ceci est un test pour vérifier SMTP.'
        from_email = settings.EMAIL_HOST_USER  # Votre email
        recipient_list = ['ali0braiki0@gmail.com']  # L'email du destinataire

        # Envoi de l'email
        send_mail(subject, message, from_email, recipient_list)

        # Vérifier que l'email a bien été envoyé
        self.assertEqual(len(mail.outbox), 1)  # Vérifie qu'un email a été ajouté à la boîte d'envoi
        self.assertEqual(mail.outbox[0].subject, subject)  # Vérifie le sujet de l'email
        self.assertEqual(mail.outbox[0].from_email, from_email)  # Vérifie l'adresse de l'expéditeur
        self.assertEqual(mail.outbox[0].to, recipient_list)  # Vérifie les destinataires
        self.assertIn('Ceci est un test pour vérifier SMTP.', mail.outbox[0].body)  # Vérifie le corps du message
