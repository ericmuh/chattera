# users/management/commands/seed_users.py
from django.core.management.base import BaseCommand
from users.models import CustomUser
from faker import Faker
from random import randint
from django.core.files import File
from io import BytesIO
from PIL import Image


class Command(BaseCommand):
    help = "Seeds the database with sample users"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Define how many users you want to create
        num_users = 10

        # Path to sample image (for testing purposes)
        sample_image_path = "path_to_sample_image.jpg"

        for _ in range(num_users):
            username = fake.user_name()
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            password = fake.password()
            gender = fake.random_element(elements=["Male", "Female"])

            # Create the user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                gender=gender,
            )

            # Add fake bio
            user.bio = fake.text(max_nb_chars=200)

            # Add fake profile picture (optional)
            image = Image.new("RGB", (100, 100), color="blue")  # Example image creation
            image_file = BytesIO()
            image.save(image_file, format="JPEG")
            image_file.seek(0)

            # Assign image to user (using a random image if you don't have a sample)
            user.profile_picture.save(
                f"{username}_profile.jpg", File(image_file), save=True
            )

            # Save the user instance
            user.save()

            # Print success message
            self.stdout.write(
                self.style.SUCCESS(
                    f"User {username} created successfully with gender {gender}"
                )
            )
