#!/usr/bin/env python3
"""
Swelist Web Terminal - Flask Backend
A retro-styled web terminal for job searching using swelist
"""

import asyncio
import logging
from typing import Dict, Any
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
import sys

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.command_handler import CommandHandler, JobShellSession
from backend.swelist_wrapper import SwelistWrapper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jobshell_secret_key_2024'

# Initialize SocketIO with CORS enabled
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global session storage (in production, use Redis or database)
sessions: Dict[str, JobShellSession] = {}
swelist_client = SwelistWrapper()

def get_or_create_session(session_id: str) -> JobShellSession:
    """Get existing session or create new one"""
    if session_id not in sessions:
        sessions[session_id] = JobShellSession()
        logger.info(f"Created new session: {session_id}")
    return sessions[session_id]

@app.route('/')
def index():
    """Serve the main terminal page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        'status': 'ok', 
        'sessions': len(sessions),
        'swelist_mode': 'mock' if swelist_client.is_mock_mode() else 'real'
    }

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    session_id = request.sid
    logger.info(f"Client connected: {session_id}")
    
    # Send welcome message
    welcome_msg = """
🚀 JOBSHELL - JOB HUNTING TERMINAL 🚀

Welcome to the ultimate job exploration experience!
Type 'help' to see available commands.

Ready to hack your way to your dream job? Let's go! 💼⚡
    """.strip()
    
    emit('terminal_output', {
        'output': welcome_msg,
        'type': 'welcome'
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    session_id = request.sid
    logger.info(f"Client disconnected: {session_id}")
    
    # Clean up session (optional, or keep for reconnection)
    if session_id in sessions:
        del sessions[session_id]

@socketio.on('command')
def handle_command(data):
    """Handle terminal commands from client"""
    session_id = request.sid
    command = data.get('command', '').strip()
    
    if not command:
        return
    
    logger.info(f"Session {session_id}: '{command}'")
    
    try:
        # Get session and handler
        session = get_or_create_session(session_id)
        handler = CommandHandler(session)
        
        # Parse command
        result = handler.parse_command(command)
        
        # Handle special cases
        if result['output'] == 'CLEAR':
            emit('clear_terminal')
            return
        elif result['output'] == 'FETCH':
            # Handle async job fetching
            job_type = result.get('job_type')
            emit('terminal_output', {
                'output': f"🔄 Fetching {job_type} jobs... Please wait...",
                'type': 'info'
            })
            
            # Use asyncio to fetch jobs
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            jobs = loop.run_until_complete(swelist_client.fetch_jobs(job_type))
            loop.close()
            
            # Update session with jobs
            session.set_jobs(jobs)
            
            mode = "mock" if swelist_client.is_mock_mode() else "real"
            emit('terminal_output', {
                'output': f"✅ Fetched {len(jobs)} {job_type} jobs! ({mode} data)\\nUse 'list' to see them.",
                'type': 'success'
            })
            return
        elif result['output'] == 'OPEN_LINK':
            # Handle opening job links
            job_data = result.get('job', {})
            url = result.get('url', '')
            
            emit('open_link', {'url': url})
            emit('terminal_output', {
                'output': f"🌐 Opening {job_data.get('company', 'job')} position in new tab...",
                'type': 'info'
            })
            return
        elif result['output'] == 'EXPORT':
            # Handle data export
            import json
            import csv
            import io
            
            data = result.get('data', [])
            format_type = result.get('format', 'json')
            data_type = result.get('data_type', 'jobs')
            
            if format_type == 'json':
                export_data = json.dumps(data, indent=2)
                filename = f"swelist_{data_type}.json"
            else:  # CSV
                if not data:
                    emit('terminal_output', {'output': '📭 No data to export', 'type': 'info'})
                    return
                
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                export_data = output.getvalue()
                filename = f"swelist_{data_type}.csv"
            
            emit('download_file', {
                'data': export_data,
                'filename': filename,
                'type': format_type
            })
            emit('terminal_output', {
                'output': f"📥 Exported {len(data)} {data_type} to {filename}",
                'type': 'success'
            })
            return
        elif result['output'] == 'THEME_CHANGE':
            # Handle theme change
            new_theme = result.get('theme', 'green')
            emit('theme_change', {'theme': new_theme})
            emit('terminal_output', {
                'output': f"🎨 Theme changed to {new_theme}",
                'type': 'success'
            })
            return
        elif result['output'] == 'SAVE_SESSION':
            # Handle session save
            session_data = result.get('session_data', {})
            emit('save_session', session_data)
            emit('terminal_output', {
                'output': "💾 Session saved to browser storage",
                'type': 'success'
            })
            return
        elif result['output'] == 'LOAD_SESSION':
            # Handle session load
            emit('load_session')
            emit('terminal_output', {
                'output': "🔄 Loading session from browser storage...",
                'type': 'info'
            })
            return
        elif result['output'] == 'COMPLETIONS':
            # Handle auto-completions
            completions = result.get('completions', [])
            emit('show_completions', {'completions': completions})
            return
        
        # Send regular output
        output_type = 'error' if result.get('error') else 'output'
        emit('terminal_output', {
            'output': result['output'],
            'type': output_type
        })
        
    except Exception as e:
        logger.error(f"Error handling command '{command}': {e}")
        emit('terminal_output', {
            'output': f"❌ Internal error: {str(e)}\\nPlease try again.",
            'type': 'error'
        })

@socketio.on('toggle_mode')
def handle_toggle_mode():
    """Toggle between mock and real swelist mode"""
    session_id = request.sid
    
    if swelist_client.is_mock_mode():
        swelist_client.enable_real_mode()
        mode = "real swelist"
    else:
        swelist_client.enable_mock_mode()
        mode = "mock data"
    
    emit('terminal_output', {
        'output': f"🔄 Switched to {mode} mode",
        'type': 'info'
    })

if __name__ == '__main__':
    print("🚀 Starting Swelist Web Terminal...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🎯 Ready for job hunting!")
    print()
    
    # Run with SocketIO
    socketio.run(
        app, 
        host='0.0.0.0', 
        port=5000, 
        debug=True,
        use_reloader=False  # Disable reloader for stability
    )
