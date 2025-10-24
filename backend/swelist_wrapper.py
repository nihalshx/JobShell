import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SwelistWrapper:
    """Wrapper for swelist library to fetch job data"""
    
    def __init__(self):
        self.last_fetch_time = None
        self._mock_mode = True  # Start in mock mode, can be toggled
        
    async def fetch_jobs(self, job_type: str) -> List[Dict[str, Any]]:
        """
        Fetch jobs from swelist or return mock data
        
        Args:
            job_type: 'internships', 'newgrad', or 'fulltime'
            
        Returns:
            List of job dictionaries
        """
        logger.info(f"Fetching {job_type} jobs...")
        
        try:
            if self._mock_mode:
                return self._get_mock_jobs(job_type)
            else:
                return await self._fetch_real_jobs(job_type)
                
        except Exception as e:
            logger.error(f"Error fetching jobs: {e}")
            # Fallback to mock data if real fetch fails
            return self._get_mock_jobs(job_type)
    
    async def _fetch_real_jobs(self, job_type: str) -> List[Dict[str, Any]]:
        """Fetch real jobs using swelist library"""
        try:
            # Import swelist here to handle if it's not installed
            import swelist
            
            # Map our job types to swelist types
            swelist_type_map = {
                'internships': 'internship',
                'newgrad': 'new_grad',
                'fulltime': 'full_time'
            }
            
            swelist_type = swelist_type_map.get(job_type, job_type)
            
            # Fetch jobs using swelist
            jobs_data = swelist.get(swelist_type)
            
            # Convert to our format
            jobs = []
            if isinstance(jobs_data, list):
                for job in jobs_data:
                    normalized_job = self._normalize_job_data(job)
                    if normalized_job:
                        jobs.append(normalized_job)
            
            self.last_fetch_time = datetime.now()
            logger.info(f"Successfully fetched {len(jobs)} real jobs")
            return jobs
            
        except ImportError:
            logger.warning("swelist not installed, using mock data")
            return self._get_mock_jobs(job_type)
        except Exception as e:
            logger.error(f"Error with swelist: {e}")
            return self._get_mock_jobs(job_type)
    
    def _normalize_job_data(self, job: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normalize job data from swelist to our standard format"""
        try:
            return {
                'company': job.get('company', 'Unknown Company'),
                'title': job.get('title', job.get('position', 'Unknown Position')),
                'location': job.get('location', 'Location TBD'),
                'url': job.get('url', job.get('link', job.get('apply_url', ''))),
                'description': job.get('description', ''),
                'requirements': job.get('requirements', []),
                'posted_date': job.get('posted_date', ''),
                'deadline': job.get('deadline', ''),
                'salary': job.get('salary', ''),
                'type': job.get('type', ''),
                'experience_level': job.get('experience_level', ''),
                'source': 'swelist'
            }
        except Exception as e:
            logger.error(f"Error normalizing job data: {e}")
            return None
    
    def _get_mock_jobs(self, job_type: str) -> List[Dict[str, Any]]:
        """Generate mock job data for testing"""
        mock_data = {
            'internships': [
                {
                    'company': 'Google',
                    'title': 'Software Engineering Intern',
                    'location': 'Mountain View, CA',
                    'url': 'https://careers.google.com/jobs',
                    'description': 'Work on cutting-edge projects with experienced engineers.',
                    'requirements': ['Python', 'Java', 'Data Structures'],
                    'posted_date': '2024-01-15',
                    'deadline': '2024-03-01',
                    'salary': '$8000/month',
                    'type': 'Internship',
                    'experience_level': 'Student',
                    'source': 'mock'
                },
                {
                    'company': 'Microsoft',
                    'title': 'Software Development Engineer Intern',
                    'location': 'Seattle, WA',
                    'url': 'https://careers.microsoft.com',
                    'description': 'Build features for Microsoft products used by millions.',
                    'requirements': ['C++', 'JavaScript', 'React'],
                    'posted_date': '2024-01-20',
                    'deadline': '2024-03-15',
                    'salary': '$7500/month',
                    'type': 'Internship',
                    'experience_level': 'Student',
                    'source': 'mock'
                },
                {
                    'company': 'Meta',
                    'title': 'Frontend Engineering Intern',
                    'location': 'Remote',
                    'url': 'https://www.metacareers.com',
                    'description': 'Work on React applications at massive scale.',
                    'requirements': ['React', 'TypeScript', 'GraphQL'],
                    'posted_date': '2024-01-25',
                    'deadline': '2024-04-01',
                    'salary': '$8500/month',
                    'type': 'Internship',
                    'experience_level': 'Student',
                    'source': 'mock'
                },
                {
                    'company': 'Amazon',
                    'title': 'Software Development Engineer Intern',
                    'location': 'Austin, TX',
                    'url': 'https://amazon.jobs',
                    'description': 'Build scalable systems for AWS services.',
                    'requirements': ['Java', 'Python', 'AWS'],
                    'posted_date': '2024-02-01',
                    'deadline': '2024-03-30',
                    'salary': '$7200/month',
                    'type': 'Internship',
                    'experience_level': 'Student',
                    'source': 'mock'
                },
                {
                    'company': 'Spotify',
                    'title': 'Data Science Intern',
                    'location': 'New York, NY',
                    'url': 'https://www.lifeatspotify.com/jobs',
                    'description': 'Analyze user behavior and improve recommendation algorithms.',
                    'requirements': ['Python', 'SQL', 'Machine Learning'],
                    'posted_date': '2024-02-05',
                    'deadline': '2024-04-15',
                    'salary': '$6800/month',
                    'type': 'Internship',
                    'experience_level': 'Student',
                    'source': 'mock'
                }
            ],
            'newgrad': [
                {
                    'company': 'Apple',
                    'title': 'Software Engineer - New Grad',
                    'location': 'Cupertino, CA',
                    'url': 'https://jobs.apple.com',
                    'description': 'Join the team building the next generation of Apple products.',
                    'requirements': ['Swift', 'Objective-C', 'iOS Development'],
                    'posted_date': '2024-01-10',
                    'deadline': '2024-06-01',
                    'salary': '$140000/year',
                    'type': 'Full-time',
                    'experience_level': 'New Grad',
                    'source': 'mock'
                },
                {
                    'company': 'Netflix',
                    'title': 'Backend Engineer - New Grad',
                    'location': 'Los Gatos, CA',
                    'url': 'https://jobs.netflix.com',
                    'description': 'Build microservices that power streaming for millions.',
                    'requirements': ['Java', 'Spring', 'Microservices'],
                    'posted_date': '2024-01-18',
                    'deadline': '2024-05-30',
                    'salary': '$135000/year',
                    'type': 'Full-time',
                    'experience_level': 'New Grad',
                    'source': 'mock'
                },
                {
                    'company': 'Uber',
                    'title': 'Software Engineer I',
                    'location': 'San Francisco, CA',
                    'url': 'https://www.uber.com/careers',
                    'description': 'Work on systems that connect millions of riders and drivers.',
                    'requirements': ['Go', 'Python', 'Kubernetes'],
                    'posted_date': '2024-02-01',
                    'deadline': '2024-07-01',
                    'salary': '$128000/year',
                    'type': 'Full-time',
                    'experience_level': 'New Grad',
                    'source': 'mock'
                }
            ],
            'fulltime': [
                {
                    'company': 'OpenAI',
                    'title': 'Senior Software Engineer',
                    'location': 'San Francisco, CA',
                    'url': 'https://openai.com/careers',
                    'description': 'Build AI systems that benefit humanity.',
                    'requirements': ['Python', 'TensorFlow', 'Distributed Systems'],
                    'posted_date': '2024-01-05',
                    'deadline': '2024-08-01',
                    'salary': '$200000/year',
                    'type': 'Full-time',
                    'experience_level': 'Senior',
                    'source': 'mock'
                },
                {
                    'company': 'Stripe',
                    'title': 'Staff Software Engineer',
                    'location': 'Remote',
                    'url': 'https://stripe.com/jobs',
                    'description': 'Build the financial infrastructure for the internet.',
                    'requirements': ['Ruby', 'Scala', 'Financial Systems'],
                    'posted_date': '2024-02-10',
                    'deadline': '2024-09-01',
                    'salary': '$220000/year',
                    'type': 'Full-time',
                    'experience_level': 'Staff',
                    'source': 'mock'
                }
            ]
        }
        
        jobs = mock_data.get(job_type, [])
        logger.info(f"Generated {len(jobs)} mock {job_type} jobs")
        return jobs
    
    def enable_real_mode(self):
        """Enable real swelist fetching"""
        self._mock_mode = False
        logger.info("Switched to real swelist mode")
    
    def enable_mock_mode(self):
        """Enable mock data mode"""
        self._mock_mode = True
        logger.info("Switched to mock data mode")
    
    def is_mock_mode(self) -> bool:
        """Check if currently in mock mode"""
        return self._mock_mode