# 🎨 Guardian Frontend - Setup Guide

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- Guardian backend running on `http://127.0.0.1:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

**Frontend will be available at**: `http://localhost:3000`

### Build for Production

```bash
npm run build
npm run preview
```

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx           # Top navigation with system status
│   │   ├── Hero.jsx              # Hero section with stats
│   │   ├── IncidentCard.jsx      # Individual incident card
│   │   ├── IncidentList.jsx      # List of incidents
│   │   └── MonitoringPanel.jsx   # Live monitoring panel
│   ├── pages/
│   │   └── Dashboard.jsx         # Main dashboard page
│   ├── services/
│   │   └── api.js                # API service layer
│   ├── App.jsx                   # Root component
│   ├── main.jsx                  # Entry point
│   └── index.css                 # Global styles
├── index.html                    # HTML template
├── package.json                  # Dependencies
├── vite.config.js                # Vite configuration
├── tailwind.config.js            # Tailwind CSS configuration
└── postcss.config.js             # PostCSS configuration
```

---

## 🎨 Design System

### Color Palette

```css
/* Primary Colors */
--cyber-blue: #00f0ff      /* Cyan accent */
--cyber-purple: #a855f7    /* Purple accent */
--cyber-pink: #ec4899      /* Pink accent */

/* Background Colors */
--dark-bg: #0a0a0f         /* Main background */
--dark-card: #1a1a2e       /* Card background */
--dark-border: #2a2a3e     /* Border color */
```

### Typography

- **Font Family**: Inter (Google Fonts)
- **Headings**: Bold, gradient text
- **Body**: Regular, gray-400

### Effects

- **Glassmorphism**: `backdrop-filter: blur(10px)`
- **Glow**: Animated box-shadow
- **Float**: Subtle up/down animation
- **Pulse**: Slow pulsing animation

---

## 🔧 Configuration

### API Endpoint

Edit `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';
```

### Auto-Refresh Interval

Edit `frontend/src/pages/Dashboard.jsx`:

```javascript
// Auto-refresh every 5 seconds
const interval = setInterval(() => {
  fetchIncidents();
  checkHealth();
}, 5000); // Change this value
```

### Vite Proxy

Edit `frontend/vite.config.js`:

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    }
  }
}
```

---

## 🎯 Features

### 1. Futuristic UI
- ✅ Dark theme with neon accents
- ✅ Glassmorphism effects
- ✅ Animated gradients
- ✅ Glowing borders
- ✅ 3D hover effects

### 2. Real-Time Monitoring
- ✅ Auto-refresh every 5 seconds
- ✅ Live system status indicators
- ✅ Animated status dots
- ✅ Health monitoring

### 3. Incident Management
- ✅ Expandable incident cards
- ✅ AI diagnosis display
- ✅ Remediation action tracking
- ✅ Status badges
- ✅ Timestamp display

### 4. Animations
- ✅ Framer Motion animations
- ✅ Fade-in effects
- ✅ Hover animations
- ✅ Floating effects
- ✅ Smooth transitions

### 5. Responsive Design
- ✅ Mobile-friendly
- ✅ Tablet-optimized
- ✅ Desktop-optimized
- ✅ Flexible grid layout

---

## 📊 Components

### Navbar
**Location**: `src/components/Navbar.jsx`

**Features**:
- Guardian logo with rotating animation
- System status indicators (Kubernetes, Prometheus, AI Engine)
- Live indicator with pulsing animation

**Props**:
```javascript
<Navbar systemStatus={{
  kubernetes: 'online',
  prometheus: 'online',
  aiEngine: 'online'
}} />
```

---

### Hero
**Location**: `src/components/Hero.jsx`

**Features**:
- Large futuristic heading
- Animated background gradients
- Stats cards with hover effects
- Gradient text

**Props**:
```javascript
<Hero stats={{
  activeIncidents: 5,
  resolvedIncidents: 12,
  autoRemediated: 8,
  uptime: '99.9%'
}} />
```

---

### IncidentCard
**Location**: `src/components/IncidentCard.jsx`

**Features**:
- Expandable card with smooth animation
- Status badge with color coding
- AI diagnosis section
- Recommended solution section
- Auto-remediation details
- Timestamp display

**Props**:
```javascript
<IncidentCard 
  incident={{
    id: '123',
    issue: '[default] crash-test → CrashLoopBackOff',
    status: 'detected',
    cause: 'Container crashes on startup',
    solution: 'Check logs and restart pod',
    action_taken: 'restart_pod',
    action_status: 'success',
    created_at: '2026-05-06T21:00:00Z'
  }}
  index={0}
/>
```

---

### IncidentList
**Location**: `src/components/IncidentList.jsx`

**Features**:
- List of incident cards
- Loading skeletons
- Empty state with animation
- Staggered animations

**Props**:
```javascript
<IncidentList 
  incidents={[...]}
  loading={false}
/>
```

---

### MonitoringPanel
**Location**: `src/components/MonitoringPanel.jsx`

**Features**:
- Service status indicators
- Animated status dots
- System health bar
- Hover effects

**Props**:
```javascript
<MonitoringPanel systemStatus={{
  kubernetes: 'online',
  prometheus: 'online',
  aiEngine: 'online',
  remediation: 'online'
}} />
```

---

## 🎨 Styling Guide

### Glassmorphism Card

```jsx
<div className="glass rounded-xl p-6 border border-dark-border">
  {/* Content */}
</div>
```

### Gradient Text

```jsx
<h1 className="gradient-text">
  Autonomous AI Ops Platform
</h1>
```

### Glow Effect

```jsx
<div className="glow-cyan rounded-lg">
  {/* Content */}
</div>
```

### Hover Animation

```jsx
<motion.div
  whileHover={{ scale: 1.05, y: -5 }}
  className="glass rounded-xl p-6"
>
  {/* Content */}
</motion.div>
```

---

## 🔍 Troubleshooting

### Frontend Not Loading

**Check**:
1. Node.js version: `node --version` (should be 18+)
2. Dependencies installed: `npm install`
3. Backend running: `curl http://127.0.0.1:8000/health`

### CORS Errors

**Solution**: Backend should allow CORS from `http://localhost:3000`

Add to `backend/app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Incidents Not Showing

**Check**:
1. Backend API: `curl http://127.0.0.1:8000/incidents`
2. Browser console for errors
3. Network tab in DevTools

### Animations Not Working

**Check**:
1. Framer Motion installed: `npm list framer-motion`
2. Browser supports CSS animations
3. No JavaScript errors in console

---

## 📦 Dependencies

### Production

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "framer-motion": "^10.16.4"
}
```

### Development

```json
{
  "@vitejs/plugin-react": "^4.2.0",
  "autoprefixer": "^10.4.16",
  "postcss": "^8.4.31",
  "tailwindcss": "^3.3.5",
  "vite": "^5.0.0"
}
```

---

## 🚀 Deployment

### Build

```bash
npm run build
```

**Output**: `dist/` directory

### Preview Build

```bash
npm run preview
```

### Deploy to Production

**Options**:
1. **Vercel**: `vercel deploy`
2. **Netlify**: `netlify deploy`
3. **Static Server**: Serve `dist/` directory

---

## 🎯 Performance

### Optimizations

- ✅ Vite for fast builds
- ✅ Code splitting
- ✅ Lazy loading
- ✅ Optimized animations
- ✅ Minimal dependencies

### Bundle Size

- **React**: ~140KB
- **Framer Motion**: ~60KB
- **Total**: ~200KB (gzipped)

---

## 📖 Best Practices

### Component Structure

```jsx
import { motion } from 'framer-motion';

const MyComponent = ({ prop1, prop2 }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="glass rounded-xl p-6"
    >
      {/* Content */}
    </motion.div>
  );
};

export default MyComponent;
```

### API Calls

```javascript
// Use try-catch for error handling
try {
  const data = await api.getIncidents();
  setIncidents(data);
} catch (error) {
  console.error('Error:', error);
  setError('Failed to fetch data');
}
```

### State Management

```javascript
// Use useState for local state
const [incidents, setIncidents] = useState([]);
const [loading, setLoading] = useState(true);

// Use useEffect for side effects
useEffect(() => {
  fetchIncidents();
}, []);
```

---

## 🎨 Customization

### Change Color Scheme

Edit `tailwind.config.js`:

```javascript
colors: {
  'cyber-blue': '#00f0ff',    // Change to your color
  'cyber-purple': '#a855f7',  // Change to your color
  'cyber-pink': '#ec4899',    // Change to your color
}
```

### Change Animations

Edit `tailwind.config.js`:

```javascript
animation: {
  'glow': 'glow 2s ease-in-out infinite alternate',
  'float': 'float 3s ease-in-out infinite',
}
```

### Change Font

Edit `index.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

Edit `index.css`:

```css
body {
  font-family: 'YourFont', sans-serif;
}
```

---

## 🎯 Quick Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Check for updates
npm outdated

# Update dependencies
npm update
```

---

## 📚 More Information

- **React**: https://react.dev
- **Vite**: https://vitejs.dev
- **Tailwind CSS**: https://tailwindcss.com
- **Framer Motion**: https://www.framer.com/motion
- **Guardian Backend**: See `PHASE14_DATABASE_COMPLETE.md`
