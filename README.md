# Book Rental System - Frontend Static Version

This is a static HTML/CSS frontend version of the Django Book Rental System, converted for deployment without a backend.

## Features

- Browse available books
- View book details
- Login and registration pages
- My rentals page
- Responsive design
- Mobile-friendly interface

## Files

- `index.html` - Home page with book catalog
- `book-detail.html` - Book detail page
- `login.html` - Login page
- `register.html` - Registration page
- `rentals.html` - My rentals page
- `css/style.css` - Stylesheet

## How to Deploy on GitHub Pages

### Option 1: Using GitHub Pages Settings (Recommended)

1. Go to your repository settings: **Settings → Pages**
2. Under "Source", select the **`frontend-static`** branch
3. Set the folder to **`/ (root)`**
4. Click **Save**
5. Your site will be live at: `https://saint-archylax.github.io/Django-Web-Application-Demo/`

### Option 2: Using a Different Platform

You can also deploy this to:
- **Netlify**: Drag and drop the files or connect your GitHub repo
- **Vercel**: Import your repository
- **Surge**: `surge` command in terminal
- **Heroku**: Static site buildpack

## Local Testing

1. Open `index.html` in your web browser
2. Navigate through the pages using the navigation links

## Notes

- This version uses mock/sample data (books, user interactions)
- Login and registration forms are static (don't submit anywhere)
- To add real backend functionality, connect to a Django API or other backend service
- All styling is responsive and works on mobile, tablet, and desktop

## Technologies Used

- HTML5
- CSS3
- Responsive Grid Layout
- Flexbox
