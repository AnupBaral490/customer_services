# About Page - URL Fix

## Issue
The About page was throwing a `NoReverseMatch` error:
```
Reverse for 'contact-us' not found. 'contact-us' is not a valid view function or pattern name.
```

## Root Cause
The template was trying to use `{% url 'contact:contact-us' %}` but the actual URL name in `contact/urls.py` is `'contact:contact'`.

## Solution
Updated the CTA button in `/templates/core/about.html`:

**Before**:
```html
<a href="{% url 'contact:contact-us' %}" class="btn-cta-secondary">
```

**After**:
```html
<a href="{% url 'contact:contact' %}" class="btn-cta-secondary">
```

## Status
✅ **Fixed** - The About page now loads correctly and the "Get in Touch" button works properly.

## Verification
- Django checks: ✅ Passed
- URL patterns: ✅ Correct
- About page: ✅ Working

Visit `/about/` to see the premium About Us page with all animations and styling!
