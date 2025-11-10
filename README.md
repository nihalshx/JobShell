# 🚀 JobShell - Enhanced Job Hunting Terminal

A powerful, retro-styled terminal interface for exploring tech jobs. JobShell combines the nostalgia of classic terminals with modern job search capabilities, powered by the swelist library.

**JobShell** - Because finding your dream job should feel like hacking the matrix! 💼⚡

## ✨ Enhanced Features

### 🖥️ Terminal Experience
- **Multi-Theme Support**: 5 beautiful themes (green, blue, amber, red, purple)
- **Smooth Animations**: Slide-in effects, loading indicators, and transitions
- **Auto-Completion**: Tab completion for commands and parameters
- **Command History**: Navigate with arrow keys, persistent across sessions
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Accessibility**: Full ARIA support, keyboard navigation, screen reader compatible

### 📦 Job Management
- **Advanced Search**: Search across all job fields with relevance ranking
- **Pagination Support**: Browse large job lists page by page (e.g., `list 2`)
- **Smart Filtering**: Multiple filter criteria and operators
- **Bookmarking System**: Save and manage favorite job listings
- **Export Data**: Download jobs/bookmarks as JSON or CSV files

### 💾 Session & Storage
- **Session Persistence**: Auto-save preferences and bookmarks
- **Theme Persistence**: Remember your preferred theme
- **Command History**: Persistent command history across sessions
- **Browser Storage**: All data saved locally for privacy
- **Configurable Timeouts**: Customizable session timeout and cleanup

### 🎯 New Features (Latest Update)
- **Relevance-Based Search**: Search results ranked by match quality
- **Enhanced Error Messages**: Helpful tips and suggestions with errors
- **Configuration Management**: Environment-based configuration
- **Mobile Optimization**: Responsive breakpoints for all screen sizes
- **Accessibility Features**: High contrast and reduced motion support

## 🛠️ Tech Stack

- **Backend**: Flask + SocketIO
- **Frontend**: xterm.js + vanilla JavaScript
- **Data Source**: swelist Python library
- **Styling**: Pure CSS with retro CRT effects

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone & Setup**:
   ```bash
   git clone <your-repo-url>
   cd JobShell
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Open in Browser**:
   Navigate to `http://localhost:5000`

## 📋 Enhanced Commands

### 📁 Job Commands
| Command | Description | Example |
|---------|-------------|---------|
| `fetch <type>` | Fetch jobs (internships/newgrad/fulltime) | `fetch internships` |
| `list [page]` | Display current jobs with pagination | `list` or `list 2` |
| `open <id>` | Open job link in browser | `open 1` |
| `search <keyword>` | Search with relevance ranking | `search python` |

### ⭐ Bookmarks
| Command | Description | Example |
|---------|-------------|---------|
| `bookmark <id>` | Bookmark a job by ID | `bookmark 1` |
| `bookmark remove <id>` | Remove a bookmark | `bookmark remove 1` |
| `bookmarks` | Show all bookmarked jobs | `bookmarks` |

### 📤 Data Export
| Command | Description | Example |
|---------|-------------|---------|
| `export json [jobs\|bookmarks]` | Export to JSON | `export json bookmarks` |
| `export csv [jobs\|bookmarks]` | Export to CSV | `export csv jobs` |

### 🎨 Customization
| Command | Description | Example |
|---------|-------------|---------|
| `theme <color>` | Change theme | `theme blue` |
| `preferences` | Show current preferences | `preferences` |

### 💾 System
| Command | Description | Example |
|---------|-------------|---------|
| `save` | Save session data | `save` |
| `load` | Load session data | `load` |
| `status` | Show session status | `status` |
| `history` | View command history | `history` |
| `reset` | Reset all data | `reset` |
| `clear` | Clear terminal | `clear` |

### Filtering Examples

```bash
# Show only remote positions
filter remote

# Filter by location
filter location=NYC

# Filter by company
filter company=Google

# General text search
filter python
```

## 🎮 Shortcuts & Features

- **Arrow Keys**: Navigate command history
- **Ctrl+C**: Cancel current input
- **Ctrl+L**: Clear terminal
- **Tab**: Auto-completion (coming soon)
- **Konami Code**: Toggle between mock and real data mode 🎮

## 🏗️ Project Structure

```
JobShell/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── backend/
│   ├── command_handler.py      # Command parsing logic
│   └── swelist_wrapper.py      # Job fetching wrapper
└── templates/
    └── index.html              # HTML terminal interface
```

## 🔧 Configuration

### Environment Variables

JobShell supports configuration through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host address | `0.0.0.0` |
| `PORT` | Server port | `5000` |
| `FLASK_DEBUG` | Enable debug mode | `false` |
| `SECRET_KEY` | Flask secret key | `jobshell_secret_key_2024` |
| `SESSION_TIMEOUT_MINUTES` | Session timeout | `30` |
| `MAX_COMMAND_LENGTH` | Max command length | `1000` |
| `ITEMS_PER_PAGE` | Jobs per page | `20` |
| `MOCK_MODE` | Use mock data | `true` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Example Configuration

```bash
# Set custom port and debug mode
export PORT=8080
export FLASK_DEBUG=true
export ITEMS_PER_PAGE=30
python app.py
```

### Data Modes

The application starts in **mock mode** with sample data. To use real swelist data:

1. Set `MOCK_MODE=false` environment variable
2. Ensure swelist is properly configured
3. Use the Konami code (↑↑↓↓←→←→BA) to toggle modes
4. Or modify `config.py` defaults

## 🎨 Customization

### Terminal Themes

Edit the terminal theme in `templates/index.html`:

```javascript
theme: {
    background: '#000000',
    foreground: '#00ff00',  // Change terminal color
    cursor: '#00ff00',
    // ... more colors
}
```

### CRT Effects

Modify CSS variables in the `<style>` section for different visual effects:

```css
/* Change glow color */
box-shadow: 0 0 100px #004400; /* Green glow */

/* Adjust scanlines */
animation: scanlines 0.1s linear infinite;
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn --worker-class eventlet -w 1 app:app
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 To-Do List

- [ ] Command auto-completion
- [ ] Job bookmarking/favorites
- [ ] Export results to JSON/CSV
- [ ] Multiple terminal themes
- [ ] User authentication
- [ ] Advanced filtering options
- [ ] Job application tracking

## 🐛 Troubleshooting

### Common Issues

**Terminal not loading:**
- Check browser console for JavaScript errors
- Ensure all CDN resources are accessible

**Jobs not fetching:**
- Verify swelist library installation
- Check network connectivity
- Try toggling to mock mode first

**WebSocket connection fails:**
- Check if port 5000 is available
- Verify Flask-SocketIO installation
- Try restarting the server

## 📜 License

MIT License - feel free to modify and distribute!

## 🎯 Inspiration

Inspired by classic terminal interfaces and the need for a more engaging job search experience. Perfect for developers who miss the good old days of green-on-black terminals!

---

**Ready to hack your way to your dream job?** 💼✨

Fire up JobShell and type `help` to get started!

## 🚀 Deployment

### ☁️ Cloud Deployment

#### **Vercel** (Recommended)
1. Fork this repository
2. Connect your GitHub repo to [Vercel](https://vercel.com)
3. Deploy automatically with zero configuration


### 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| `PORT` | Server port | `5000` |
| `FLASK_ENV` | Environment | `production` |
| `FLASK_DEBUG` | Debug mode | `false` |

### 📦 GitHub Actions

Automatic deployment is configured with GitHub Actions:
- ✅ **Testing**: Code quality checks and testing
- 📄 **Pages**: Deploy documentation to GitHub Pages

### 🔗 Live Demo

Once deployed, your terminal will be available at your deployment URL. The application includes:
- Health check endpoint: `/health`
- Main terminal interface: `/`
- Real-time WebSocket communication
- Persistent browser storage
