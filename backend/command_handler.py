import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

class JobShellSession:
    def __init__(self):
        self.jobs: List[Dict[str, Any]] = []
        self.filtered_jobs: List[Dict[str, Any]] = []
        self.command_history: List[str] = []
        self.bookmarks: List[Dict[str, Any]] = []
        self.filters: Dict[str, str] = {}
        self.last_fetch_time: Optional[datetime] = None
        self.user_preferences: Dict[str, Any] = {
            'theme': 'green',
            'notifications': True,
            'auto_save': True
        }
        
    def add_command(self, command: str):
        self.command_history.append(command)
        
    def set_jobs(self, jobs: List[Dict[str, Any]]):
        self.jobs = jobs
        self.filtered_jobs = jobs
        self.last_fetch_time = datetime.now()
        
    def add_bookmark(self, job: Dict[str, Any]) -> bool:
        """Add a job to bookmarks"""
        job_id = f"{job.get('company', 'Unknown')}_{job.get('title', 'Unknown')}"
        if not any(b.get('id') == job_id for b in self.bookmarks):
            bookmark = job.copy()
            bookmark['id'] = job_id
            bookmark['bookmarked_at'] = datetime.now().isoformat()
            self.bookmarks.append(bookmark)
            return True
        return False
    
    def remove_bookmark(self, job_id: str) -> bool:
        """Remove a job from bookmarks"""
        original_count = len(self.bookmarks)
        self.bookmarks = [b for b in self.bookmarks if b.get('id') != job_id]
        return len(self.bookmarks) < original_count

class CommandHandler:
    def __init__(self, session: JobShellSession):
        self.session = session
        self.available_commands = [
            'help', 'fetch', 'list', 'filter', 'open', 'bookmark', 'bookmarks',
            'export', 'theme', 'status', 'history', 'reset', 'clear', 'search',
            'notifications', 'preferences', 'save', 'load'
        ]
        self.job_types = ['internships', 'newgrad', 'fulltime']
        self.themes = ['green', 'blue', 'amber', 'red', 'purple']
        
    def get_completions(self, partial_command: str) -> List[str]:
        """Get command completions for partial input"""
        if not partial_command:
            return self.available_commands[:5]  # Show top 5 commands
        
        # Split command to handle subcommands
        parts = partial_command.split()
        if len(parts) == 1:
            # Complete main commands
            matches = [cmd for cmd in self.available_commands if cmd.startswith(parts[0].lower())]
            return matches[:5]
        elif len(parts) == 2:
            # Complete subcommands based on main command
            main_cmd = parts[0].lower()
            partial_sub = parts[1].lower()
            
            if main_cmd == 'fetch':
                return [jt for jt in self.job_types if jt.startswith(partial_sub)]
            elif main_cmd == 'theme':
                return [t for t in self.themes if t.startswith(partial_sub)]
            elif main_cmd == 'export':
                return [fmt for fmt in ['json', 'csv'] if fmt.startswith(partial_sub)]
        
        return []
        
    def parse_command(self, command: str) -> Dict[str, Any]:
        """Parse and execute terminal commands"""
        cmd = command.strip().lower()
        self.session.add_command(command)
        
        if not cmd:
            return {"output": "", "error": False}
            
        # Help command
        if cmd == "help":
            return self._help_command()
            
        # Clear command
        elif cmd == "clear":
            return {"output": "CLEAR", "error": False}
            
        # Fetch commands
        elif cmd.startswith("fetch"):
            return self._fetch_command(cmd)
            
        # List commands
        elif cmd in ["list", "ls", "jobs"]:
            return self._list_command()
            
        # Filter commands
        elif cmd.startswith("filter"):
            return self._filter_command(cmd)
            
        # Open command
        elif cmd.startswith("open"):
            return self._open_command(cmd)
            
        # Status command
        elif cmd in ["status", "info"]:
            return self._status_command()
            
        # History command
        elif cmd == "history":
            return self._history_command()
            
        # Bookmark commands
        elif cmd.startswith("bookmark"):
            return self._bookmark_command(cmd)
            
        # Show bookmarks
        elif cmd == "bookmarks":
            return self._bookmarks_command()
            
        # Export command
        elif cmd.startswith("export"):
            return self._export_command(cmd)
            
        # Theme command
        elif cmd.startswith("theme"):
            return self._theme_command(cmd)
            
        # Search command
        elif cmd.startswith("search"):
            return self._search_command(cmd)
            
        # Preferences command
        elif cmd == "preferences":
            return self._preferences_command()
            
        # Save session
        elif cmd == "save":
            return self._save_command()
            
        # Load session
        elif cmd == "load":
            return self._load_command()
            
        # Reset command
        elif cmd == "reset":
            return self._reset_command()
            
        # Auto-completion request
        elif cmd.startswith("complete "):
            return self._complete_command(cmd)
            
        # Unknown command
        else:
            return {
                "output": f"❌ Unknown command: '{command}'\nType 'help' to see available commands.\n💡 Try 'complete {command.split()[0]}' for suggestions.",
                "error": True
            }
    
    def _help_command(self) -> Dict[str, Any]:
        help_text = """
🚀 SWELIST WEB TERMINAL v4.0 - ENHANCED 🚀

📁 JOB COMMANDS:
  fetch <type>            Fetch jobs (internships|newgrad|fulltime)
  list                    List current jobs (aliases: ls, jobs)
  open <id>               Open job link in new tab
  search <keyword>        Search across all job fields

🔍 FILTERING:
  filter <criteria>       Filter jobs by criteria
  filter remote           Show only remote jobs
  filter location=NYC     Filter by specific location
  filter company=Google   Filter by company name

⭐ BOOKMARKS:
  bookmark <id>           Bookmark a job by ID
  bookmark remove <id>    Remove a bookmark
  bookmarks               Show all bookmarked jobs

📤 DATA EXPORT:
  export json [jobs|bookmarks]    Export to JSON format
  export csv [jobs|bookmarks]     Export to CSV format

🎨 CUSTOMIZATION:
  theme <color>           Change theme (green|blue|amber|red|purple)
  preferences             Show current preferences
  
💾 SESSION:
  save                    Save session data
  load                    Load session data
  status                  Show session status and stats
  history                 Show command history
  reset                   Reset all session data
  clear                   Clear terminal screen

🚀 SHORTCUTS:
  Tab                     Auto-complete commands
  ↑/↓ Arrow Keys        Navigate command history
  Ctrl+C                  Cancel current input
  Ctrl+L                  Clear terminal

💡 EXAMPLES:
  > fetch internships
  > search python
  > bookmark 1
  > theme blue
  > export json bookmarks

Happy job hunting! 🎯
        """
        return {"output": help_text.strip(), "error": False}
    
    def _fetch_command(self, cmd: str) -> Dict[str, Any]:
        """Handle fetch commands"""
        parts = cmd.split()
        if len(parts) < 2:
            return {
                "output": "❌ Usage: fetch [internships|newgrad|fulltime]",
                "error": True
            }
        
        job_type = parts[1]
        valid_types = ["internships", "newgrad", "fulltime"]
        
        if job_type not in valid_types:
            return {
                "output": f"❌ Invalid job type. Use: {', '.join(valid_types)}",
                "error": True
            }
        
        return {
            "output": "FETCH",
            "job_type": job_type,
            "error": False
        }
    
    def _list_command(self) -> Dict[str, Any]:
        """List current jobs"""
        if not self.session.filtered_jobs:
            if not self.session.jobs:
                return {
                    "output": "📭 No jobs loaded. Use 'fetch' to get job listings first.",
                    "error": False
                }
            else:
                return {
                    "output": "📭 No jobs match current filters. Use 'reset' to clear filters.",
                    "error": False
                }
        
        output = [f"\n📋 SHOWING {len(self.session.filtered_jobs)} JOBS:\n"]
        
        for i, job in enumerate(self.session.filtered_jobs[:20], 1):  # Limit to 20
            company = job.get('company', 'Unknown Company')
            title = job.get('title', 'Unknown Position')
            location = job.get('location', 'Location TBD')
            
            # Truncate long titles
            if len(title) > 50:
                title = title[:47] + "..."
                
            output.append(f"{i:2}. {company} - {title}")
            output.append(f"    📍 {location}")
            
        if len(self.session.filtered_jobs) > 20:
            output.append(f"\n... and {len(self.session.filtered_jobs) - 20} more jobs")
            output.append("Use filters to narrow down results.")
        
        return {"output": "\n".join(output), "error": False}
    
    def _filter_command(self, cmd: str) -> Dict[str, Any]:
        """Filter jobs based on criteria"""
        if not self.session.jobs:
            return {
                "output": "❌ No jobs to filter. Use 'fetch' first.",
                "error": True
            }
        
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            return {
                "output": "❌ Usage: filter <criteria>\nExample: filter remote OR filter location=NYC",
                "error": True
            }
        
        criteria = parts[1].lower()
        
        # Simple filtering logic
        filtered = []
        
        if criteria == "remote":
            filtered = [job for job in self.session.jobs 
                       if any(term in job.get('location', '').lower() 
                             for term in ['remote', 'anywhere', 'distributed'])]
        elif "=" in criteria:
            # Handle key=value filters
            key, value = criteria.split("=", 1)
            key = key.strip()
            value = value.strip().lower()
            
            for job in self.session.jobs:
                job_value = job.get(key, '').lower()
                if value in job_value:
                    filtered.append(job)
        else:
            # General text search across all fields
            filtered = [job for job in self.session.jobs
                       if any(criteria in str(v).lower() for v in job.values())]
        
        self.session.filtered_jobs = filtered
        
        return {
            "output": f"🔍 Filter applied: '{criteria}'\n✅ Found {len(filtered)} matching jobs",
            "error": False
        }
    
    def _open_command(self, cmd: str) -> Dict[str, Any]:
        """Open job link"""
        parts = cmd.split()
        if len(parts) < 2:
            return {
                "output": "❌ Usage: open <job_id>\nExample: open 3",
                "error": True
            }
        
        try:
            job_id = int(parts[1]) - 1  # Convert to 0-based index
            
            if job_id < 0 or job_id >= len(self.session.filtered_jobs):
                return {
                    "output": f"❌ Invalid job ID. Use 'list' to see available jobs (1-{len(self.session.filtered_jobs)})",
                    "error": True
                }
            
            job = self.session.filtered_jobs[job_id]
            url = job.get('url', job.get('link', ''))
            
            if not url:
                return {
                    "output": "❌ No URL available for this job",
                    "error": True
                }
            
            return {
                "output": "OPEN_LINK",
                "url": url,
                "job": job,
                "error": False
            }
            
        except ValueError:
            return {
                "output": "❌ Job ID must be a number",
                "error": True
            }
    
    def _status_command(self) -> Dict[str, Any]:
        """Show session status"""
        total_jobs = len(self.session.jobs)
        filtered_jobs = len(self.session.filtered_jobs)
        commands_run = len(self.session.command_history)
        
        fetch_time = "Never"
        if self.session.last_fetch_time:
            fetch_time = self.session.last_fetch_time.strftime("%Y-%m-%d %H:%M:%S")
        
        status = f"""
📊 SESSION STATUS:
  Total jobs loaded: {total_jobs}
  Visible jobs: {filtered_jobs}
  Commands executed: {commands_run}
  Last fetch: {fetch_time}
  
💡 Use 'list' to see jobs or 'help' for commands
        """
        
        return {"output": status.strip(), "error": False}
    
    def _history_command(self) -> Dict[str, Any]:
        """Show command history"""
        if not self.session.command_history:
            return {"output": "📜 No command history yet", "error": False}
        
        output = ["📜 COMMAND HISTORY:"]
        for i, cmd in enumerate(self.session.command_history[-10:], 1):  # Last 10 commands
            output.append(f"  {i}. {cmd}")
        
        return {"output": "\n".join(output), "error": False}
    
    def _reset_command(self) -> Dict[str, Any]:
        """Reset session data"""
        self.session.jobs = []
        self.session.filtered_jobs = []
        self.session.last_fetch_time = None
        
        return {
            "output": "🔄 Session reset. All jobs and filters cleared.",
            "error": False
        }
    
    def _bookmark_command(self, cmd: str) -> Dict[str, Any]:
        """Handle bookmark commands"""
        parts = cmd.split()
        if len(parts) < 2:
            return {
                "output": "❌ Usage: bookmark <job_id> OR bookmark remove <job_id>",
                "error": True
            }
        
        if parts[1] == "remove" and len(parts) >= 3:
            job_id = parts[2]
            if self.session.remove_bookmark(job_id):
                return {"output": f"🗑️ Removed bookmark: {job_id}", "error": False}
            else:
                return {"output": f"❌ Bookmark not found: {job_id}", "error": True}
        else:
            try:
                job_idx = int(parts[1]) - 1
                if 0 <= job_idx < len(self.session.filtered_jobs):
                    job = self.session.filtered_jobs[job_idx]
                    if self.session.add_bookmark(job):
                        return {"output": f"⭐ Bookmarked: {job.get('company')} - {job.get('title')}", "error": False}
                    else:
                        return {"output": "📌 Job already bookmarked", "error": False}
                else:
                    return {"output": "❌ Invalid job ID", "error": True}
            except ValueError:
                return {"output": "❌ Job ID must be a number", "error": True}
    
    def _bookmarks_command(self) -> Dict[str, Any]:
        """List all bookmarks"""
        if not self.session.bookmarks:
            return {"output": "📭 No bookmarks saved yet.", "error": False}
        
        output = [f"\n⭐ BOOKMARKS ({len(self.session.bookmarks)}):\n"]
        for i, bookmark in enumerate(self.session.bookmarks, 1):
            company = bookmark.get('company', 'Unknown')
            title = bookmark.get('title', 'Unknown')
            bookmarked_at = bookmark.get('bookmarked_at', 'Unknown time')
            output.append(f"{i:2}. {company} - {title}")
            output.append(f"    📅 Saved: {bookmarked_at[:19]}")
            
        return {"output": "\n".join(output), "error": False}
    
    def _export_command(self, cmd: str) -> Dict[str, Any]:
        """Export jobs to file format"""
        parts = cmd.split()
        if len(parts) < 2:
            return {
                "output": "❌ Usage: export [json|csv] [jobs|bookmarks]",
                "error": True
            }
        
        format_type = parts[1].lower()
        data_type = parts[2].lower() if len(parts) > 2 else 'jobs'
        
        if format_type not in ['json', 'csv']:
            return {"output": "❌ Format must be 'json' or 'csv'", "error": True}
        
        if data_type == 'bookmarks':
            data = self.session.bookmarks
        else:
            data = self.session.filtered_jobs
        
        if not data:
            return {"output": f"📭 No {data_type} to export", "error": False}
        
        return {
            "output": "EXPORT",
            "format": format_type,
            "data_type": data_type,
            "data": data,
            "error": False
        }
    
    def _theme_command(self, cmd: str) -> Dict[str, Any]:
        """Change terminal theme"""
        parts = cmd.split()
        if len(parts) < 2:
            current_theme = self.session.user_preferences.get('theme', 'green')
            available = ', '.join(self.themes)
            return {
                "output": f"🎨 Current theme: {current_theme}\nAvailable: {available}\nUsage: theme <color>",
                "error": False
            }
        
        new_theme = parts[1].lower()
        if new_theme in self.themes:
            self.session.user_preferences['theme'] = new_theme
            return {
                "output": "THEME_CHANGE",
                "theme": new_theme,
                "error": False
            }
        else:
            available = ', '.join(self.themes)
            return {"output": f"❌ Invalid theme. Available: {available}", "error": True}
    
    def _search_command(self, cmd: str) -> Dict[str, Any]:
        """Enhanced search across all job fields"""
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            return {"output": "❌ Usage: search <keyword>", "error": True}
        
        keyword = parts[1].lower()
        matches = []
        
        for job in self.session.jobs:
            # Search across all job fields
            searchable_text = ' '.join([
                job.get('company', ''),
                job.get('title', ''),
                job.get('location', ''),
                job.get('description', ''),
                ' '.join(job.get('requirements', []))
            ]).lower()
            
            if keyword in searchable_text:
                matches.append(job)
        
        self.session.filtered_jobs = matches
        return {
            "output": f"🔍 Search results for '{keyword}': {len(matches)} jobs found",
            "error": False
        }
    
    def _preferences_command(self) -> Dict[str, Any]:
        """Show user preferences"""
        prefs = self.session.user_preferences
        output = ["\n⚙️ USER PREFERENCES:"]
        for key, value in prefs.items():
            status = "✅" if value else "❌" if isinstance(value, bool) else "📝"
            output.append(f"  {status} {key}: {value}")
        
        output.append("\n💡 Use 'theme <color>' to change theme")
        return {"output": "\n".join(output), "error": False}
    
    def _save_command(self) -> Dict[str, Any]:
        """Save session data"""
        return {
            "output": "SAVE_SESSION",
            "session_data": {
                "bookmarks": self.session.bookmarks,
                "preferences": self.session.user_preferences,
                "command_history": self.session.command_history[-20:]
            },
            "error": False
        }
    
    def _load_command(self) -> Dict[str, Any]:
        """Load session data"""
        return {
            "output": "LOAD_SESSION",
            "error": False
        }
    
    def _complete_command(self, cmd: str) -> Dict[str, Any]:
        """Handle auto-completion"""
        parts = cmd.split(maxsplit=1)
        partial = parts[1] if len(parts) > 1 else ""
        
        completions = self.get_completions(partial)
        if completions:
            return {
                "output": "COMPLETIONS",
                "completions": completions,
                "error": False
            }
        else:
            return {"output": "💭 No completions available", "error": False}
