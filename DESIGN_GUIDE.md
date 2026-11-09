# 🎨 Premium Design Guide

## Design System Overview

Your website now features a premium, modern Australian cleaning services design with professional animations, gradients, and smooth interactions.

---

## 🎯 Design Features Implemented

### Color Palette
```
Primary:        #183D39 (Deep Teal)
Primary Light:  #2d5b57 (Medium Teal)
Primary Dark:   #0d1e1b (Dark Teal)
Secondary:      #DCEFE8 (Soft Mint)
Accent:         #DCA85C (Warm Gold)
Background:     #F7F9F8 (Off-White)
Text:           #252B2A (Dark Gray)
```

### Typography
- **Headings**: Poppins (Bold, 700-800 weight)
- **Body Text**: Inter (Regular, 400-500 weight)
- **Font Sizes**: Responsive (scales on mobile)

---

## ✨ Design Enhancements

### 1. Navigation Bar
- Sticky positioning
- Smooth hover effects with underline animations
- Gradient button with shadow
- Mobile-responsive hamburger menu
- Professional spacing and typography

### 2. Hero Section
- Full gradient background (135deg angle)
- Large, bold headline with gradient text effect
- Smooth fade-in animations
- Dual CTA buttons (Book & Quote)
- Responsive typography sizing

### 3. Service Cards
- Top accent bar with gradient
- Smooth hover lift animation (+8px transform)
- Image zoom on hover
- Rounded corners (12px)
- Professional shadow system
- Clear call-to-action buttons

### 4. Testimonial Cards
- Quotation mark styling
- Border highlight on hover
- Star rating system
- Author and service information
- Smooth transitions

### 5. Buttons
- Gradient backgrounds
- Smooth transitions
- Shadow effects
- Hover animations (translateY -3px)
- Multiple variants (Primary, Outline, Light)
- Size options (sm, lg)

### 6. Forms
- Modern input styling
- 2px borders
- Focus state with shadow
- Label weight and spacing
- Rounded corners

### 7. Footer
- Gradient background matching hero
- Professional link styling
- Social media icons
- Organized sections
- Responsive layout

### 8. Cards
- Consistent rounded corners (12px)
- Professional shadow system
- Border styling
- Hover effects

---

## 🎬 Animation System

### Keyframe Animations
1. **fadeInUp** - Elements fade in while moving up (300ms delay between items)
2. **slideInLeft** - Content slides in from left
3. **slideInRight** - Content slides in from right

### Interactive Effects
- Smooth color transitions (0.3s)
- Transform animations on hover
- Shadow depth changes
- Border color animations

### Cubic-Bezier Timing
Uses `cubic-bezier(0.4, 0, 0.2, 1)` for smooth, professional motion

---

## 📱 Responsive Design

### Breakpoints
- **Large (lg)**: 992px+ (Desktop)
- **Medium (md)**: 768px+ (Tablet)
- **Small (xs)**: Below 768px (Mobile)

### Mobile Adjustments
- Hero title: 3.5rem → 2.2rem
- Section title: 2.8rem → 2rem
- Stack CTA buttons vertically
- Adjust padding and margins
- Single-column layouts

---

## 🎨 CSS Classes & Utilities

### Text Classes
```css
.gradient-text          /* Gradient text effect */
.text-white-50         /* Semi-transparent white */
.fw-800                /* Font weight 800 (extra bold) */
.fw-700                /* Font weight 700 (bold) */
.fw-600                /* Font weight 600 (semi-bold) */
```

### Layout Classes
```css
.section-padding       /* 80px top/bottom */
.section-title         /* Styled section heading */
.section-subtitle      /* Styled subtitle */
.min-vh-75            /* Minimum height 75vh */
```

### Shadow Classes
```css
.shadow-sm-custom      /* Light shadow */
.shadow-md-custom      /* Medium shadow */
```

### Transitions
```css
.transition            /* Smooth 0.3s transition */
```

---

## 🔄 Component Styling

### Navbar
- White background with subtle shadow
- Gradient "Book Now" button
- Hover underline animation on links
- Sticky positioning

### Hero Section
- 135° gradient background
- Animated fade-in sequence
- Large typography hierarchy
- Dual-action CTAs

### Feature Section
- Circular icon containers with gradient
- Centered text alignment
- Four-column grid (responsive)
- Hover effects on icons

### Service Grid
- 3-column grid (responsive to 2, then 1)
- Card hover lift animation
- Image zoom on hover
- Clear pricing display
- Dual buttons per card

### Testimonials
- "Quote mark" pseudo-element styling
- Border highlight on hover
- 5-star rating system
- Author attribution
- Clean layout

### FAQ Accordion
- Custom styling for accordion items
- Gradient background on active
- Custom arrow icon color (Accent)
- Smooth expand/collapse

### Footer
- Gradient background matching hero
- Semi-transparent text
- Social media icons with hover effects
- Link hover transformations
- Organized content sections

---

## 🌈 Gradient Usage

### Primary Gradients
```css
/* Hero & Footer */
background: linear-gradient(135deg, #183D39 0%, #2d5b57 100%);

/* Buttons */
background: linear-gradient(135deg, #183D39 0%, #2d5b57 100%);

/* Section Backgrounds */
background: linear-gradient(135deg, #F7F9F8 0%, #DCEFE8 100%);
```

### Text Gradients
```css
.gradient-text {
    background: linear-gradient(135deg, #183D39 0%, #DCA85C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
```

---

## 🔧 Customization Guide

### Change Primary Color
Edit `static/css/style.css`:
```css
:root {
    --primary: #YOUR_COLOR;
    --primary-light: #LIGHTER_SHADE;
    --primary-dark: #DARKER_SHADE;
}
```

### Change Accent Color
```css
:root {
    --accent: #YOUR_ACCENT;
    --accent-light: #LIGHTER_SHADE;
}
```

### Modify Button Styles
```css
.btn-primary {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    box-shadow: 0 4px 15px rgba(24, 61, 57, 0.2);
}
```

### Adjust Animations
```css
@keyframes fadeInUp {
    /* Modify timing and transform values */
}
```

### Change Typography
Edit font imports and sizes in CSS:
```css
/* Change Poppins to your font */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Your Font', sans-serif;
}
```

---

## 📏 Spacing System

### Standard Spacing
- **Sections**: 80px (top & bottom)
- **Cards**: 30px (padding)
- **Buttons**: 10px/24px (padding)
- **Icons**: 8px (margin)

### Gap System
- **g-3**: 1rem gap (default)
- **g-4**: 1.5rem gap
- **gap-20**: 20px gap

---

## 💡 Best Practices

1. **Hover States**
   - Always provide visual feedback
   - Use subtle transforms and shadows
   - Keep animations smooth (0.3s minimum)

2. **Color Contrast**
   - Text on primary background is white
   - Text on secondary background is dark
   - Accent color for highlights only

3. **Spacing**
   - Consistent padding across similar elements
   - Use gaps for consistent item spacing
   - Generous padding improves readability

4. **Typography**
   - Use Poppins for emphasis
   - Use Inter for body text
   - Maintain clear hierarchy

5. **Responsive Design**
   - Test on mobile, tablet, desktop
   - Use flexible grid layout
   - Stack elements on small screens

---

## 🎓 Component Examples

### Service Card
```html
<div class="service-card">
    <img src="..." alt="...">
    <div class="service-card-body">
        <h5 class="fw-700">Service Name</h5>
        <p>Description</p>
        <p class="service-price">Pricing</p>
        <div class="d-grid gap-2">
            <button class="btn btn-primary">Book Now</button>
        </div>
    </div>
</div>
```

### Feature Icon
```html
<div class="rounded-circle mx-auto mb-3" 
     style="width: 80px; height: 80px; 
             background: linear-gradient(135deg, #183D39 0%, #2d5b57 100%); 
             display: flex; align-items: center; 
             justify-content: center;">
    <i class="fas fa-icon text-white" style="font-size: 2rem;"></i>
</div>
```

### Testimonial
```html
<div class="testimonial-card h-100">
    <div class="testimonial-stars mb-3">
        <!-- Star icons -->
    </div>
    <p class="mb-3">"Quote text"</p>
    <p class="testimonial-author">Author Name</p>
    <p class="testimonial-service">Service</p>
</div>
```

---

## 📊 Design Metrics

- **Button Hover Lift**: -3px (translateY)
- **Card Hover Lift**: -8px (translateY)
- **Animation Duration**: 0.3s (most transitions)
- **Hero Fade Delay**: 0.2s between items
- **Border Radius**: 8px (standard), 12px (cards)
- **Shadow Blur**: 4px-40px (varies by depth)

---

## ✅ Tested Browsers

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile Safari (iOS 13+)
- Chrome Mobile (Android 8+)

---

## 📝 Accessibility

- Proper heading hierarchy (h1, h2, etc.)
- Color contrast ratio: 4.5:1 (WCAG AA)
- Focus states on interactive elements
- Semantic HTML structure
- Alt text on images
- ARIA labels where needed

---

## 🚀 Performance

- Efficient CSS with variables
- Minimal animations (smooth 60fps)
- Optimized shadows and gradients
- Lazy loading for images
- No JavaScript for animations
- Fast paint and reflow

---

This design system ensures a professional, modern, and delightful user experience across all devices! 🎨

