import datetime
import os
import json
from functools import reduce

from address.models import Address
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch

from arosaje.models import Plants, Posts, Species, Keeping

class KeepingTestCase(TestCase):
    fixtures = ["user", "posts", "species", "address", "keeping", "plants"]
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
        self.keeper.save()
        self.keeper.refresh_from_db()

        fixture_path = os.path.join('arosaje', 'fixtures', 'posts.json')
        with open(fixture_path, 'r') as f:
            data = json.load(f)

        # Modifier les dates
        today = datetime.datetime.now().date()
        max_id = reduce(max, map(lambda x: x["pk"], data))
        data.append({
            "model": "arosaje.posts",
            "pk": max_id + 1,
            "fields": {
                "commentary": "besoin de s'occuper de ma plante !",
                "start_of_event": (today - datetime.timedelta(days=1)).isoformat(),
                "end_of_event": (today + datetime.timedelta(days=3)).isoformat(),
                "plant_id": 1 
            }
        })
        data.append({
            "model": "arosaje.posts",
            "pk": max_id + 2,
            "fields": {
                "commentary": "besoin de s'occuper de ma plante !",
                "start_of_event": today.isoformat(),
                "end_of_event": (today + datetime.timedelta(days=2)).isoformat(),
                "plant_id": 1 
            }
        })
        data.append({
            "model": "arosaje.keeping",
            "fields": {
                "keeper_id": self.keeper.id,
                "post_id": max_id + 1
            }
        })
        data.append({
            "model": "arosaje.keeping",
            "fields": {
                "keeper_id": self.keeper.id,
                "post_id": max_id + 2
            }
        })

        temp_fixture = os.path.join('arosaje', 'fixtures', 'tmp_fixtures.json')
        with open(temp_fixture, 'w') as f:
            json.dump(data, f)

        call_command('loaddata', 'tmp_fixtures.json', verbosity=0)

        os.remove(temp_fixture)

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

        with self.assertRaises(ValidationError):
            keeping = Keeping(
                keeper=self.keeper,
                post=self.post
            )
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

    def test_command_update_keepings_for_outdated_pending(self):
        keeping = Keeping.objects.filter(post__start_of_event__lt=datetime.datetime.now(), _status=0).first()

        self.assertEqual(keeping.status, 0)
        call_command('updateKeepings')

        keeping.refresh_from_db()
        self.assertEqual(keeping.status, 2)

    def test_command_update_keepings_for_outdated_ongoing(self):
        keeping = Keeping.objects.filter(post__end_of_event__lt=datetime.datetime.now(), _status=3).first()

        self.assertEqual(keeping.status, 3)
        call_command('updateKeepings')

        keeping.refresh_from_db()
        self.assertEqual(keeping.status, 5)

    def test_command_update_keepings_doesnt_update_future(self):
        keeping = Keeping.objects.filter(post__start_of_event__gte=datetime.datetime.now(), _status=0).first()

        self.assertEqual(keeping.status, 0)
        call_command('updateKeepings')

        keeping.refresh_from_db()
        self.assertNotEqual(keeping.status, 2)

    def test_command_update_keepings_doesnt_update_today(self):
        correct_keeping = Keeping.objects.filter(
            post__start_of_event=datetime.datetime.now().date(), 
            _status=0
        ).first()
        outdated_keeping = Keeping.objects.filter(
            post__start_of_event=(datetime.datetime.now().date() - datetime.timedelta(days=1)), 
            _status=0
        ).first()

        self.assertEqual(correct_keeping.status, 0)
        self.assertEqual(outdated_keeping.status, 0)

        call_command('updateKeepings')

        correct_keeping.refresh_from_db()
        outdated_keeping.refresh_from_db()

        self.assertNotEqual(correct_keeping.status, 2)
        self.assertEqual(outdated_keeping.status, 2)
