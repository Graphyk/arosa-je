import datetime

from address.models import Address
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch

from arosaje.models import Plants, Posts, Species, Keeping

class KeepingTestCase(TestCase):
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
            picture="/media/hortensia.png"
        )

        self.keeper = User.objects.create_user(
            username='johndeer',
            email='johndeer@example.com',
            password='secure_password123'
        )
        
        self.post = Posts.objects.create(
            commentary="origin post",
            plant=self.plant,
            start_of_event=timezone.now().date() + datetime.timedelta(days=5),
            end_of_event=timezone.now().date() + datetime.timedelta(days=8)
        )

    def test_insert_keeping_before_start_of_event(self):
        keeping = Keeping(
            keeper=self.keeper,
            post=self.post
        )

        keeping.save()
        self.assertEqual(keeping.status, 0)

    def test_insert_keeping_same_day_than_start_of_event(self):
        # don't save because it will raise a validation error, but you normally need to save an object after editing it
        self.post.start_of_event = timezone.now().date()

        keeping = Keeping(
            keeper=self.keeper,
            post=self.post
        )
        with self.assertRaises(ValidationError):
            keeping.save()
    
    def test_insert_keeping_after_start_of_event(self):
        # don't save because it will raise a validation error, but you normally need to save an object after editing it
        self.post.start_of_event = timezone.now().date() - datetime.timedelta(days=1)

        keeping = Keeping(
            keeper=self.keeper,
            post=self.post
        )
        with self.assertRaises(ValidationError):
            keeping.save()

    
    def test_cancel_keeping(self):
        keeping = Keeping(
            keeper=self.keeper,
            post=self.post
        )

        keeping.cancel()
        keeping.refresh_from_db()
        self.assertEqual(keeping.status, 1)

    def test_cancel_after_plant_taken(self):
        keeping = Keeping(
            keeper=self.keeper,
            post=self.post
        )

        keeping.take()
        keeping.refresh_from_db()

        with self.assertRaises(ValidationError):
            keeping.cancel()

    def test_take_plant(self):
        keeping = Keeping(
            keeper=self.keeper,
            post=self.post
        )

        keeping.take()
        keeping.refresh_from_db()
        self.assertEqual(keeping.status, 3)

    def test_take_plant_after_cancellation(self):
        keeping = Keeping(
            keeper=self.keeper,
            post=self.post
        )

        keeping.cancel()
        keeping.refresh_from_db()

        with self.assertRaises(ValidationError):
            keeping.take()

    def test_validate_keeping(self):
        keeping = Keeping(
            keeper=self.keeper,
            post=self.post
        )

        keeping.take()
        keeping.refresh_from_db()

        keeping.validate()
        keeping.refresh_from_db()
        self.assertEqual(keeping.status, 4)

    def test_validate_keeping_without_plant_taken(self):
        keeping = Keeping(
            keeper=self.keeper,
            post=self.post
        )

        with self.assertRaises(ValidationError):
            keeping.validate()

    def test_validate_keeping_after_cancellation(self):
        keeping = Keeping(
            keeper=self.keeper,
            post=self.post
        )

        keeping.cancel()
        keeping.refresh_from_db()

        with self.assertRaises(ValidationError):
            keeping.validate()