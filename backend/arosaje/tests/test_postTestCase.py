import datetime

from address.models import Address
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from arosaje.models import Plants, Posts, Species 

class PostsTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='secure_password123'
        )

        self.address = Address.objects.create(
            raw="Parc de haute technologie du Moulin Leblanc, Campu Sup, 08000 Charleville-Mézières"
        )

        # Créer une plante pour les tests
        self.species = Species.objects.create(
            name="Rose",
            water_dependency=2,
            light_dependency=3,
        )

        self.plant = Plants.objects.create(
            species=self.species,
            owner=self.user,
            address=self.address,
            picture="/media/hortensia.png",
            lat=0,
            lon=0
        )
        
        # Créer une période existante
        self.post = Posts.objects.create(
            commentary="origin post",
            plant=self.plant,
            start_of_event=timezone.now().date() + datetime.timedelta(days=5),
            end_of_event=timezone.now().date() + datetime.timedelta(days=8)
        )

    def test_with_non_overlapping_after_existing_periods(self):
        new_post = Posts(
            commentary="cool post",
            plant=self.plant,
            start_of_event=timezone.now().date() + datetime.timedelta(days=9),
            end_of_event=timezone.now().date() + datetime.timedelta(days=10)
        )

        try:
            new_post.save()
        except ValidationError:
            self.fail("post with non overlappings periods are not inserted")

        self.assertTrue(True)

    def test_with_non_overlapping_before_existing_periods(self):
        new_post = Posts(
            commentary="cool post",
            plant=self.plant,
            start_of_event=timezone.now().date() + datetime.timedelta(days=1),
            end_of_event=timezone.now().date() + datetime.timedelta(days=4)
        )

        try:
            new_post.save()
        except ValidationError:
            self.fail("post with non overlappings periods are not inserted")

        self.assertTrue(True) 

    def test_with_overlapping_start_of_event(self):
        new_post = Posts(
            commentary="cool post",
            plant=self.plant,
            start_of_event=timezone.now().date() + datetime.timedelta(days=6),
            end_of_event=timezone.now().date() + datetime.timedelta(days=10)
        )

        with self.assertRaises(ValidationError):
            new_post.save()

    def test_with_overlapping_end_of_event(self):
        new_post = Posts(
            commentary="cool post",
            plant=self.plant,
            start_of_event=timezone.now().date() + datetime.timedelta(days=2),
            end_of_event=timezone.now().date() + datetime.timedelta(days=6)
        )

        with self.assertRaises(ValidationError):
            new_post.save()
    
    def test_with_overlapping_start_and_end_of_event(self):
        new_post = Posts(
            commentary="cool post",
            plant=self.plant,
            start_of_event=timezone.now().date() + datetime.timedelta(days=6),
            end_of_event=timezone.now().date() + datetime.timedelta(days=7)
        )

        with self.assertRaises(ValidationError):
            new_post.save()
    
    def test_with_wrapping_period(self):
        new_post = Posts(
            commentary="cool post",
            plant=self.plant,
            start_of_event=timezone.now().date() + datetime.timedelta(days=2),
            end_of_event=timezone.now().date() + datetime.timedelta(days=10)
        )

        with self.assertRaises(ValidationError):
            new_post.save()
    
    def test_with_starting_date_to_today(self):
        new_post = Posts(
            commentary="cool post",
            plant=self.plant,
            start_of_event=timezone.now().date(),
            end_of_event=timezone.now().date() + datetime.timedelta(days=2)
        )

        with self.assertRaises(ValidationError):
            new_post.save()
