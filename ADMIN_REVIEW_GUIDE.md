# Admin Guide - Managing Customer Reviews

## Quick Start

### Access Admin Panel
```
URL: http://yoursite.com/admin/
Username: [your admin username]
Password: [your admin password]
```

### Navigate to Reviews
1. Log in to admin
2. Look for **"Core"** section on left sidebar
3. Click **"Testimonials"**

## Managing Reviews

### View All Reviews
- See list of all customer reviews
- Shows: Name, Service, Rating, Approval Status, Date

### Approve a Review

**To approve one review:**
1. Click on the review in the list
2. Check the box: **"Is Approved"**
3. Click **"Save"** button
4. Review now appears on website

**To approve multiple reviews:**
1. Select reviews using checkboxes on left
2. Use dropdown at top: **"Action"**
3. Select **"Mark selected as approved"** (if available)
4. Or approve individually

### Reject/Delete Reviews

**To reject/delete a single review:**
1. Click on the review
2. Scroll to bottom
3. Click **"Delete"** button
4. Confirm deletion

**To delete multiple reviews:**
1. Select reviews using checkboxes
2. Action dropdown
3. Select **"Delete selected testimonials"**
4. Confirm

## Filtering Reviews

### By Status
- Click filter: **"Is Approved"**
- Select **"No"** → Shows pending reviews
- Select **"Yes"** → Shows approved reviews
- Leave blank → Shows all

### By Date
- Filter: **"Created At"**
- Shows reviews by submission date

### Search
- Use search box at top
- Search by:
  - Customer name
  - Service type
  - Review text keywords

## Review Details

When you click a review, you see:

- **Customer Name** - Person who submitted
- **Service** - What service they used
- **Rating** - 1-5 stars
- **Comment** - Full review text
- **Is Approved** - Checkbox to approve/disapprove
- **Created At** - When submitted (read-only)

## Best Practices

✅ **Do:**
- Approve genuine reviews
- Delete spam/inappropriate reviews
- Review regularly (check admin daily)
- Approve quickly (within 24-48 hours)

❌ **Don't:**
- Approve obviously fake reviews
- Delete negative but fair reviews
- Leave all reviews pending
- Modify review text (delete instead)

## Keyboard Shortcuts

- Save: `Ctrl + S`
- Delete: No shortcut (use button)
- Search: `Ctrl + F`

## Export Reviews

To export reviews (if needed):
1. Select all reviews
2. Scroll to top
3. Use action dropdown
4. Look for "Export" option (if installed)

## Stats & Insights

### Average Rating
To calculate manually:
1. View all approved reviews
2. Add up all ratings
3. Divide by number of reviews

Example: 5+5+4+5+4 = 23 ÷ 5 = 4.6 stars average

### Review Count
- Check count shown in admin list header
- Example: "Showing 1-10 of 42 testimonials"

## Troubleshooting

### Review not showing on website?
- Check: Is box "Is Approved" checked? ✓
- Check: At least 1 review approved?
- Refresh website browser cache

### Can't find testimonials section?
- Path: `/admin/core/testimonial/`
- Look for "Core" app in left sidebar
- Under "Core" find "Testimonials"

### Want to see pending reviews only?
- Click "Is Approved" filter
- Select "No"
- Shows only unapproved reviews

### How to mass approve?
Django admin doesn't have bulk approve by default:
- Approve individually by:
  1. Click review
  2. Check "Is Approved"
  3. Save
  4. Click Next/Back
  5. Repeat

Or modify in admin if you know Django

## Daily Workflow

**Every morning:**
1. Go to `/admin/core/testimonial/`
2. Filter: Is Approved = "No"
3. Review pending reviews (should take 5-10 min)
4. Approve good ones
5. Delete spam/inappropriate ones

**Tips:**
- Read full review before approving
- Check for spam keywords/links
- Use common sense about authenticity
- Approve within 24 hours for better UX

## Contact & Support

If you need help:
- Check `USER_REVIEW_SYSTEM.md` for full docs
- Check `REVIEW_SYSTEM_SUMMARY.md` for overview
- Django admin help: Press `?` in admin

---

**That's it!** You now have a system where customers can submit reviews and you can easily approve/manage them in the admin dashboard.
