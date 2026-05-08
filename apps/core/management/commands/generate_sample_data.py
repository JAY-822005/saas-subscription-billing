from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization
from apps.subscriptions.models import SubscriptionPlan, Subscription
from faker import Faker
from django.utils import timezone
from datetime import timedelta

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Generate sample data for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of test users to create'
        )
        parser.add_argument(
            '--orgs',
            type=int,
            default=10,
            help='Number of organizations to create'
        )
        parser.add_argument(
            '--plans',
            type=int,
            default=4,
            help='Number of subscription plans to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting data generation...'))

        # Create subscription plans if they don't exist
        if SubscriptionPlan.objects.count() < options['plans']:
            self.create_plans(options['plans'])

        # Create users
        users = self.create_users(options['users'])

        # Create organizations and subscriptions
        for user in users:
            self.create_organizations(user, options['orgs'] // len(users) + 1)

        self.stdout.write(self.style.SUCCESS('Data generation completed!'))

    def create_users(self, count):
        """Create test users"""
        users = []
        for i in range(count):
            email = f'user{i+1}@example.com'
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    username=f'testuser{i+1}',
                    email=email,
                    password='testpass123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    role='org_admin' if i == 0 else 'member'
                )
                users.append(user)
                self.stdout.write(f'Created user: {email}')
            else:
                users.append(User.objects.get(email=email))

        return users

    def create_plans(self, count):
        """Create subscription plans"""
        plans_data = [
            {
                'name': 'Starter',
                'description': 'Perfect for getting started',
                'monthly_price': 29.99,
                'yearly_price': 299.99,
                'max_users': 5,
                'usage_limit': 1000,
                'free_trial_days': 14,
            },
            {
                'name': 'Professional',
                'description': 'For growing teams',
                'monthly_price': 99.99,
                'yearly_price': 999.99,
                'max_users': 50,
                'usage_limit': 50000,
                'free_trial_days': 14,
            },
            {
                'name': 'Enterprise',
                'description': 'For large organizations',
                'monthly_price': 299.99,
                'yearly_price': 2999.99,
                'max_users': 500,
                'usage_limit': 1000000,
                'free_trial_days': 30,
            },
            {
                'name': 'Free',
                'description': 'Always free',
                'monthly_price': 0,
                'yearly_price': 0,
                'max_users': 3,
                'usage_limit': 100,
                'free_trial_days': 0,
            },
        ]

        for plan_data in plans_data[:count]:
            if not SubscriptionPlan.objects.filter(name=plan_data['name']).exists():
                SubscriptionPlan.objects.create(**plan_data)
                self.stdout.write(f'Created plan: {plan_data["name"]}')

    def create_organizations(self, user, count):
        """Create organizations and subscriptions"""
        plans = list(SubscriptionPlan.objects.all())

        for i in range(count):
            org_name = fake.company()
            slug = f"{user.username}-org{i+1}".lower()

            if not Organization.objects.filter(slug=slug).exists():
                org = Organization.objects.create(
                    name=org_name,
                    slug=slug,
                    owner=user,
                    contact_email=fake.email(),
                )

                # Create a subscription
                plan = plans[i % len(plans)]
                Subscription.objects.create(
                    organization=org,
                    plan=plan,
                    status='active',
                    billing_cycle='monthly',
                    trial_ends_at=timezone.now() + timedelta(days=14),
                    renews_at=timezone.now() + timedelta(days=30),
                )

                self.stdout.write(f'Created organization: {org_name} with subscription to {plan.name}')
