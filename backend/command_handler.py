"""
Command Handler Module for JobShell Terminal

This module handles parsing and execution of terminal commands,
managing job sessions, bookmarks, and user preferences.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class JobShellSession:
    """
    Session management class for JobShell terminal.
    
    Maintains state for jobs, bookmarks, command history,
    and user preferences throughout a user session.
    """
    
    def __init__(self):
        """Initialize a new JobShell session with default values."""
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
        
    def add_command(self, command: str) -> None:
        """
        Add a command to the history.
        
        Args:
            command: The command string to add to history
        """
        if command and command.strip():
            self.command_history.append(command)
        
    def set_jobs(self, jobs: List[Dict[str, Any]]) -> None:
        """
        Set the current list of jobs and reset filters.
        
        Args:
            jobs: List of job dictionaries to store
        """
        self.jobs = jobs
        self.filtered_jobs = jobs
        self.last_fetch_time = datetime.now()
        
    def add_bookmark(self, job: Dict[str, Any]) -> bool:
        """
        Add a job to bookmarks if not already bookmarked.
        
        Args:
            job: The job dictionary to bookmark
            
        Returns:
            True if bookmark was added, False if already exists
        """
        # Input validation
        if not job or not isinstance(job, dict):
            return False
            
        job_id = f"{job.get('company', 'Unknown')}_{job.get('title', 'Unknown')}"
        
        # Check if already bookmarked
        if not any(b.get('id') == job_id for b in self.bookmarks):
            bookmark = job.copy()
            bookmark['id'] = job_id
            bookmark['bookmarked_at'] = datetime.now().isoformat()
            self.bookmarks.append(bookmark)
            return True
        return False
    
    def remove_bookmark(self, job_id: str) -> bool:
        """
        Remove a job from bookmarks by ID.
        
        Args:
            job_id: The ID of the bookmark to remove
            
        Returns:
            True if bookmark was removed, False if not found
        """
        if not job_id or not isinstance(job_id, str):
            return False
            
        original_count = len(self.bookmarks)
        self.bookmarks = [b for b in self.bookmarks if b.get('id') != job_id]
        return len(self.bookmarks) < original_count

class CommandHandler:
    """
    Command parser and handler for JobShell terminal.
    
    Parses user input and executes appropriate commands,
    managing job data, bookmarks, and session state.
    """
    
    def __init__(self, session: JobShellSession):
        """
        Initialize the command handler with a session.
        
        Args:
            session: The JobShellSession to manage
        """
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
        elif cmd.startswith("list") or cmd.startswith("ls") or cmd.startswith("jobs"):
            return self._list_command(cmd)
            
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
        """Display comprehensive help information."""
        help_text = """
🚀 JOBSHELL - JOB HUNTING TERMINAL 🚀

📁 JOB COMMANDS:
  fetch <type>            Fetch jobs (internships|newgrad|fulltime)
  list [page]             List current jobs with pagination (e.g., 'list 2')
  open <id>               Open job link in new tab
  search <keyword>        Search across all job fields with relevance ranking

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
  save                    Save session data to browser
  load                    Load session data from browser
  status                  Show session status and stats
  history                 Show command history
  reset                   Reset all session data
  clear                   Clear terminal screen

🚀 KEYBOARD SHORTCUTS:
  Tab                     Auto-complete commands
  ↑/↓ Arrow Keys         Navigate command history
  Ctrl+C                  Cancel current input
  Ctrl+L                  Clear terminal

💡 EXAMPLES:
  > fetch internships         # Fetch internship opportunities
  > search python             # Search for Python-related jobs
  > list 2                    # View page 2 of job listings
  > bookmark 1                # Bookmark the first job
  > theme blue                # Switch to blue theme
  > export json bookmarks     # Export bookmarks as JSON

📊 TIPS:
  • Search results are ranked by relevance
  • Use pagination to browse large job lists
  • Bookmarks are saved in your browser
  • Commands support auto-completion with Tab

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
    
    def _list_command(self, cmd: str = "list") -> Dict[str, Any]:
        """
        List current jobs with pagination support.
        
        Args:
            cmd: Command string (e.g., 'list', 'list 2' for page 2)
            
        Returns:
            Dictionary with output and error status
        """
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
        
        # Parse page number from command if provided (e.g., "list 2")
        page = 1
        parts = cmd.split()
        if len(parts) > 1:
            try:
                page = max(1, int(parts[1]))
            except ValueError:
                return {
                    "output": "❌ Invalid page number. Usage: list [page_number]",
                    "error": True
                }
        
        # Pagination settings
        items_per_page = 20
        total_jobs = len(self.session.filtered_jobs)
        total_pages = (total_jobs + items_per_page - 1) // items_per_page
        
        # Validate page number
        if page > total_pages:
            return {
                "output": f"❌ Page {page} doesn't exist. Total pages: {total_pages}",
                "error": True
            }
        
        # Calculate slice indices
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_jobs)
        
        output = [f"\n📋 SHOWING JOBS {start_idx + 1}-{end_idx} OF {total_jobs} (Page {page}/{total_pages}):\n"]
        
        for i, job in enumerate(self.session.filtered_jobs[start_idx:end_idx], start_idx + 1):
            company = job.get('company', 'Unknown Company')
            title = job.get('title', 'Unknown Position')
            location = job.get('location', 'Location TBD')
            
            # Truncate long titles for better display
            if len(title) > 50:
                title = title[:47] + "..."
                
            output.append(f"{i:2}. {company} - {title}")
            output.append(f"    📍 {location}")
        
        # Add pagination info
        if total_pages > 1:
            output.append(f"\n📄 Page {page} of {total_pages}")
            if page < total_pages:
                output.append(f"💡 Use 'list {page + 1}' to see the next page")
        
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
        
        # Optimized filtering logic - single pass through jobs list
        filtered = []
        
        if criteria == "remote":
            # Pre-compile remote terms for faster lookup
            remote_terms = ('remote', 'anywhere', 'distributed')
            filtered = [job for job in self.session.jobs 
                       if any(term in job.get('location', '').lower() for term in remote_terms)]
        elif "=" in criteria:
            # Handle key=value filters
            key, value = criteria.split("=", 1)
            key = key.strip()
            value = value.strip().lower()
            
            # Single list comprehension instead of loop + append
            filtered = [job for job in self.session.jobs 
                       if value in job.get(key, '').lower()]
        else:
            # General text search across all fields - optimized
            filtered = [job for job in self.session.jobs
                       if any(criteria in str(v).lower() for v in job.values())]
        
        self.session.filtered_jobs = filtered
        
        return {
            "output": f"🔍 Filter applied: '{criteria}'\n✅ Found {len(filtered)} matching jobs",
            "error": False
        }
    
    def _open_command(self, cmd: str) -> Dict[str, Any]:
        """
        Open job link in browser.
        
        Args:
            cmd: Command string (e.g., 'open 3')
            
        Returns:
            Dictionary with link opening instructions or error
        """
        if not self.session.filtered_jobs:
            return {
                "output": "❌ No jobs available. Use 'fetch' to load jobs first.",
                "error": True
            }
        
        parts = cmd.split()
        if len(parts) < 2:
            return {
                "output": "❌ Usage: open <job_id>\nExample: open 3\n💡 Use 'list' to see available job IDs",
                "error": True
            }
        
        try:
            job_id = int(parts[1]) - 1  # Convert to 0-based index
            
            if job_id < 0 or job_id >= len(self.session.filtered_jobs):
                total = len(self.session.filtered_jobs)
                return {
                    "output": f"❌ Invalid job ID: {parts[1]}\n💡 Valid range: 1-{total}\n💡 Use 'list' to see available jobs",
                    "error": True
                }
            
            job = self.session.filtered_jobs[job_id]
            url = job.get('url', job.get('link', ''))
            
            if not url or url.strip() == '':
                company = job.get('company', 'this company')
                return {
                    "output": f"❌ No URL available for {company}\n💡 This job listing may not have an application link",
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
                "output": f"❌ Invalid job ID: '{parts[1]}' is not a number\n💡 Use 'list' to see available job IDs",
                "error": True
            }
    
    def _status_command(self) -> Dict[str, Any]:
        """
        Show comprehensive session status.
        
        Returns:
            Dictionary with status information and statistics
        """
        total_jobs = len(self.session.jobs)
        filtered_jobs = len(self.session.filtered_jobs)
        bookmarks_count = len(self.session.bookmarks)
        commands_run = len(self.session.command_history)
        
        fetch_time = "Never"
        if self.session.last_fetch_time:
            fetch_time = self.session.last_fetch_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate filtering percentage
        filter_percentage = 0
        if total_jobs > 0:
            filter_percentage = (filtered_jobs / total_jobs) * 100
        
        status = f"""
📊 SESSION STATUS:
  ├─ Total jobs loaded: {total_jobs}
  ├─ Visible jobs: {filtered_jobs} ({filter_percentage:.1f}%)
  ├─ Bookmarked jobs: {bookmarks_count}
  ├─ Commands executed: {commands_run}
  └─ Last fetch: {fetch_time}

⚙️ CURRENT THEME: {self.session.user_preferences.get('theme', 'green')}
  
💡 Quick actions:
  • 'list' - View jobs
  • 'bookmarks' - View saved jobs
  • 'help' - Show all commands
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
        """
        Enhanced search across all job fields with fuzzy matching.
        
        Args:
            cmd: Command string (e.g., 'search python')
            
        Returns:
            Dictionary with search results and status
        """
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            return {"output": "❌ Usage: search <keyword>", "error": True}
        
        keyword = parts[1].strip()
        if not keyword:
            return {"output": "❌ Please provide a search keyword", "error": True}
        
        keyword_lower = keyword.lower()
        
        # Search with relevance scoring
        scored_matches = []
        for job in self.session.jobs:
            score = 0
            
            # Build searchable fields with weights
            company = job.get('company', '').lower()
            title = job.get('title', '').lower()
            location = job.get('location', '').lower()
            description = job.get('description', '').lower()
            requirements = [r.lower() for r in job.get('requirements', [])]
            
            # Exact matches get higher scores
            if keyword_lower == company:
                score += 10
            elif keyword_lower in company:
                score += 5
                
            if keyword_lower == title:
                score += 10
            elif keyword_lower in title:
                score += 7
                
            if keyword_lower in location:
                score += 3
                
            if keyword_lower in description:
                score += 2
                
            # Check requirements
            for req in requirements:
                if keyword_lower == req:
                    score += 8
                elif keyword_lower in req:
                    score += 4
            
            # Add job to results if any match found
            if score > 0:
                scored_matches.append((score, job))
        
        # Sort by relevance score (highest first)
        scored_matches.sort(key=lambda x: x[0], reverse=True)
        matches = [job for score, job in scored_matches]
        
        self.session.filtered_jobs = matches
        
        if matches:
            return {
                "output": f"🔍 Search results for '{keyword}': {len(matches)} jobs found (sorted by relevance)\n💡 Use 'list' to view results",
                "error": False
            }
        else:
            return {
                "output": f"🔍 No jobs found matching '{keyword}'\n💡 Try different keywords or use 'reset' to clear filters",
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
