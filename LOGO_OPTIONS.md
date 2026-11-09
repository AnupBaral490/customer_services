# 🎨 Logo Options for Your Cleaning Business

The logo has been added to your navbar! Currently using a **Premium Sparkle Drop Design**.

## Current Logo Design

**File**: `static/images/logo.svg`

**Features:**
- Clean, professional design
- Sparkle stars representing premium service
- Water droplet representing cleaning
- Teal background (#183D39)
- Gold accents (#DCA85C)
- Subtle shine effects
- Hover animation: rotate + scale

## How to Use the Logo

The logo is now in your navbar at the top-left of the website. It:
- ✅ Links back to the homepage when clicked
- ✅ Has a smooth hover animation (rotates 10° and scales up)
- ✅ Displays at 40x40px in the navbar
- ✅ Automatically responsive on mobile

## To Upload Your Own Logo

1. **Prepare your logo**
   - Format: SVG (recommended) or PNG
   - Size: 40x40px for navbar
   - Background: Transparent (if PNG)

2. **Upload the file**
   - Save to: `static/images/logo.svg` (or `.png`)

3. **Update the navbar** (if needed)
   - File: `templates/includes/navbar.html`
   - Keep the same HTML structure

## Logo Placement

The logo appears in:
- **Navigation bar** - Top left of every page
- **Sticky position** - Visible when scrolling
- **Mobile** - Collapses with hamburger menu
- **Hover effect** - Rotates 10° and scales 1.05x

## Logo Size Guidelines

| Location | Size | File Size |
|----------|------|-----------|
| Navbar | 40x40px | < 5KB |
| Hero Section (optional) | 100x100px | < 10KB |
| Favicon (optional) | 32x32px | < 5KB |

## Where to Add Additional Logos

If you want to add the logo to other sections:

### 1. Hero Section
```html
<img src="{% static 'images/logo.svg' %}" alt="Logo" height="80" class="mb-4">
```

### 2. Footer
```html
<img src="{% static 'images/logo.svg' %}" alt="Logo" height="40" class="mb-3">
```

### 3. Favicon (Browser Tab)
```html
<!-- In templates/base.html, add to <head>: -->
<link rel="icon" type="image/svg+xml" href="{% static 'images/logo.svg' %}">
```

## Customization Options

### Change Logo Size
Edit `templates/includes/navbar.html`:
```html
<img src="..." alt="Logo" height="50">  <!-- Change 40 to 50 -->
```

### Change Hover Animation
Edit `static/css/style.css`:
```css
.navbar-brand:hover img {
    transform: rotate(15deg) scale(1.1);  /* Adjust values */
}
```

### Make Logo Grayscale on Hover
```css
.navbar-brand:hover img {
    filter: grayscale(1);
}
```

## Logo Design Specifications

### Current Logo Colors
- **Background**: #183D39 (Primary teal)
- **Accent Stars**: #DCA85C (Gold)
- **Water Drop**: #DCEFE8 (Mint)
- **Highlights**: #FFFFFF (White)

### Design Elements
- ✓ Sparkle stars (premium quality)
- ✓ Water droplet (cleaning action)
- ✓ Shine effects (professional look)
- ✓ Brush stroke (service indicator)

## PNG Logo Alternative

If you want to use a PNG logo instead:

1. Save your logo as `static/images/logo.png` (40x40px)
2. Update navbar:
```html
<img src="{% static 'images/logo.png' %}" alt="Logo" height="40">
```

## Logo File Optimization

For best performance:
- **SVG**: Scalable, perfect for any size (recommended)
- **PNG**: Use only if SVG not available
- Keep file size < 5KB
- Use web-safe colors

## Next Steps

1. ✅ Logo is already in place and working
2. 📝 Customize colors if desired
3. 🎨 Replace with your own logo if needed
4. 🔧 Adjust sizing/animations as needed

## Support

To modify the logo:
- **SVG editing**: Use Illustrator, Figma, or Inkscape
- **PNG editing**: Use Photoshop or GIMP
- **Online tools**: Canva, Looka (AI-generated logos)

Your cleaning services company now has a professional, branded navbar! 🎉

