#!/usr/bin/env python3
"""
Google OAuth Setup Script for ReviewApp

This script helps you set up Google OAuth integration.
Run this after setting up your Google Cloud Console project.

Steps to follow:
1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - http://127.0.0.1:8000/accounts/google/login/callback/
   - http://localhost:8000/accounts/google/login/callback/
6. Copy Client ID and Client Secret
7. Run this script and enter your credentials
8. Or manually add them in Django admin at /admin/socialaccount/socialapp/

Required credentials:
- Client ID: From Google Cloud Console
- Client Secret: From Google Cloud Console
"""

import os
import django
import sys

# Setup Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reviewproj.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def setup_google_oauth():
    print("🔧 Google OAuth Setup for ReviewApp")
    print("=" * 50)
    
    # Get or create the default site
    site, created = Site.objects.get_or_create(
        pk=1,
        defaults={'domain': '127.0.0.1:8000', 'name': 'ReviewApp'}
    )
    
    if created:
        print(f"✅ Created site: {site.name}")
    else:
        print(f"✅ Using existing site: {site.name}")
    
    # Check if Google app already exists
    existing_app = SocialApp.objects.filter(provider='google').first()
    
    if existing_app:
        print(f"⚠️  Google OAuth app already exists: {existing_app.name}")
        update = input("Do you want to update it? (y/n): ").lower().strip()
        if update != 'y':
            print("Setup cancelled.")
            return
        app = existing_app
    else:
        app = SocialApp()
        app.provider = 'google'
        app.name = 'Google OAuth for ReviewApp'
    
    print("\n📋 Please provide your Google OAuth credentials:")
    print("(Get these from Google Cloud Console)")
    
    client_id = input("Enter Client ID: ").strip()
    client_secret = input("Enter Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Client ID and Client Secret are required!")
        return
    
    app.client_id = client_id
    app.secret = client_secret
    app.save()
    
    # Add site to the app
    app.sites.add(site)
    
    print("\n✅ Google OAuth setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Make sure your Google Cloud Console has these redirect URIs:")
    print("   - http://127.0.0.1:8000/accounts/google/login/callback/")
    print("   - http://localhost:8000/accounts/google/login/callback/")
    print("2. Start your Django server: python manage.py runserver")
    print("3. Test Google login on your site!")
    
    print(f"\n🔗 Admin panel: http://127.0.0.1:8000/admin/socialaccount/socialapp/")

if __name__ == "__main__":
    try:
        setup_google_oauth()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you're in the correct directory and Django is properly configured.")