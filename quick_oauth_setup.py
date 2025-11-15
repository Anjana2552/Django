#!/usr/bin/env python3
"""
Quick Setup Script for Google OAuth
Run this to configure Google OAuth without needing Django admin access
"""

import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reviewproj.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def quick_setup():
    print("🔧 Quick Google OAuth Setup")
    print("=" * 40)
    
    # Create default site if it doesn't exist
    site, created = Site.objects.get_or_create(
        pk=1,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'ReviewApp Local'
        }
    )
    print(f"✅ Site ready: {site.domain}")
    
    # Create a dummy Google app to prevent errors
    app, created = SocialApp.objects.get_or_create(
        provider='google',
        name='Google OAuth (Not Configured)',
        defaults={
            'client_id': 'YOUR_CLIENT_ID_HERE',
            'secret': 'YOUR_CLIENT_SECRET_HERE'
        }
    )
    
    if created:
        app.sites.add(site)
        print("✅ Created placeholder Google OAuth app")
    else:
        print("✅ Google OAuth app already exists")
    
    print("\n📋 Next Steps:")
    print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Create OAuth 2.0 credentials")
    print("3. Add redirect URI: http://127.0.0.1:8000/accounts/google/login/callback/")
    print("4. Update the SocialApp in Django admin with real credentials")
    print("5. Go to: http://127.0.0.1:8000/admin/socialaccount/socialapp/")
    
    print("\n🚀 Your app should now load without errors!")

if __name__ == "__main__":
    quick_setup()