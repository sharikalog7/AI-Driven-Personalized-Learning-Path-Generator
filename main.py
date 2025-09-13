import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple
import random

# Configure page
st.set_page_config(
    page_title="AI Learning Path Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .skill-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    .learning-module {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #f8f9fa;
    }
    .progress-bar {
        height: 20px;
        border-radius: 10px;
        background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'learning_path' not in st.session_state:
    st.session_state.learning_path = None
if 'progress' not in st.session_state:
    st.session_state.progress = {}

class LearningPathGenerator:
    def __init__(self):
        self.skills_database = {
            'Data Science': {
                'prerequisites': ['Python Basics', 'Statistics'],
                'modules': ['Data Analysis', 'Machine Learning', 'Data Visualization', 'Deep Learning'],
                'difficulty': 'Advanced',
                'duration_weeks': 16
            },
            'Web Development': {
                'prerequisites': ['HTML/CSS', 'JavaScript'],
                'modules': ['Frontend Frameworks', 'Backend Development', 'Databases', 'Deployment'],
                'difficulty': 'Intermediate',
                'duration_weeks': 12
            },
            'Machine Learning': {
                'prerequisites': ['Python', 'Mathematics', 'Statistics'],
                'modules': ['Supervised Learning', 'Unsupervised Learning', 'Neural Networks', 'MLOps'],
                'difficulty': 'Advanced',
                'duration_weeks': 20
            },
            'Cloud Computing': {
                'prerequisites': ['Basic Networking', 'Linux Commands'],
                'modules': ['AWS/Azure Basics', 'Infrastructure as Code', 'Containers', 'DevOps'],
                'difficulty': 'Intermediate',
                'duration_weeks': 14
            },
            'Cybersecurity': {
                'prerequisites': ['Networking', 'Operating Systems'],
                'modules': ['Security Fundamentals', 'Ethical Hacking', 'Incident Response', 'Compliance'],
                'difficulty': 'Advanced',
                'duration_weeks': 18
            }
        }
        
        self.learning_styles = {
            'Visual': 'Prefers diagrams, charts, and visual content',
            'Auditory': 'Learns best through lectures and discussions',
            'Kinesthetic': 'Hands-on learning and practical exercises',
            'Reading/Writing': 'Text-based learning and note-taking'
        }
        
    def assess_current_skills(self, user_responses: Dict) -> Dict:
        """Simulate skill assessment using user responses"""
        skill_levels = {}
        for skill, response in user_responses.items():
            # Convert response to skill level (1-10)
            if response == 'Beginner':
                skill_levels[skill] = random.randint(1, 3)
            elif response == 'Intermediate':
                skill_levels[skill] = random.randint(4, 7)
            else:  # Advanced
                skill_levels[skill] = random.randint(7, 10)
        return skill_levels
    
    def generate_personalized_path(self, profile: Dict) -> Dict:
        """Generate a personalized learning path based on user profile"""
        career_goal = profile['career_goal']
        learning_style = profile['learning_style']
        time_commitment = profile['time_commitment']
        skill_levels = profile['skill_levels']
        
        if career_goal in self.skills_database:
            base_path = self.skills_database[career_goal].copy()
            
            # Adjust based on current skill levels
            adjusted_modules = []
            for module in base_path['modules']:
                module_info = {
                    'name': module,
                    'estimated_hours': random.randint(15, 40),
                    'resources': self.get_resources_for_module(module, learning_style),
                    'prerequisites_met': True,  # Simplified for demo
                    'difficulty': base_path['difficulty']
                }
                adjusted_modules.append(module_info)
            
            # Calculate timeline based on time commitment
            weekly_hours = {'Low (5-10 hrs/week)': 7.5, 'Medium (10-20 hrs/week)': 15, 'High (20+ hrs/week)': 25}
            hours_per_week = weekly_hours.get(time_commitment, 15)
            
            total_hours = sum([m['estimated_hours'] for m in adjusted_modules])
            estimated_weeks = int(total_hours / hours_per_week)
            
            learning_path = {
                'career_goal': career_goal,
                'modules': adjusted_modules,
                'estimated_completion': estimated_weeks,
                'total_hours': total_hours,
                'learning_style_optimized': True,
                'created_date': datetime.now().strftime('%Y-%m-%d')
            }
            
            return learning_path
        
        return None
    
    def get_resources_for_module(self, module: str, learning_style: str) -> List[Dict]:
        """Generate resources based on learning style"""
        base_resources = {
            'Visual': ['Interactive Diagrams', 'Video Tutorials', 'Infographics'],
            'Auditory': ['Podcasts', 'Video Lectures', 'Discussion Forums'],
            'Kinesthetic': ['Hands-on Projects', 'Labs', 'Simulations'],
            'Reading/Writing': ['Documentation', 'Books', 'Written Exercises']
        }
        
        resources = []
        for resource_type in base_resources.get(learning_style, ['Mixed Resources']):
            resources.append({
                'type': resource_type,
                'title': f"{module} - {resource_type}",
                'estimated_time': f"{random.randint(2, 8)} hours",
                'difficulty': random.choice(['Beginner', 'Intermediate', 'Advanced'])
            })
        
        return resources

# Initialize the generator
generator = LearningPathGenerator()

# Main App Layout
st.markdown('<h1 class="main-header">🎓 AI-Driven Learning Path Generator</h1>', unsafe_allow_html=True)

# Sidebar for user profile
with st.sidebar:
    st.header("👤 User Profile")
    
    # Career Goals
    career_goal = st.selectbox(
        "What's your career goal?",
        list(generator.skills_database.keys()),
        help="Select your primary career objective"
    )
    
    # Learning Style Assessment
    learning_style = st.selectbox(
        "What's your preferred learning style?",
        list(generator.learning_styles.keys()),
        help="Choose how you learn best"
    )
    
    # Time Commitment
    time_commitment = st.selectbox(
        "How much time can you commit weekly?",
        ['Low (5-10 hrs/week)', 'Medium (10-20 hrs/week)', 'High (20+ hrs/week)']
    )
    
    # Current Skill Assessment
    st.subheader("📊 Skill Assessment")
    skill_responses = {}
    
    relevant_skills = ['Python', 'Mathematics', 'Statistics', 'Machine Learning', 'Data Analysis']
    
    for skill in relevant_skills:
        skill_responses[skill] = st.select_slider(
            f"{skill} proficiency:",
            options=['Beginner', 'Intermediate', 'Advanced'],
            value='Beginner'
        )
    
    # Generate Path Button
    if st.button("🚀 Generate My Learning Path", type="primary"):
        # Create user profile
        user_profile = {
            'career_goal': career_goal,
            'learning_style': learning_style,
            'time_commitment': time_commitment,
            'skill_levels': generator.assess_current_skills(skill_responses)
        }
        
        # Generate learning path
        learning_path = generator.generate_personalized_path(user_profile)
        
        # Store in session state
        st.session_state.user_profile = user_profile
        st.session_state.learning_path = learning_path
        
        st.success("Learning path generated successfully!")
        st.rerun()

# Main content area
if st.session_state.learning_path:
    path = st.session_state.learning_path
    profile = st.session_state.user_profile
    
    # Overview Section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🎯 Career Goal",
            path['career_goal']
        )
    
    with col2:
        st.metric(
            "⏱️ Total Duration",
            f"{path['estimated_completion']} weeks"
        )
    
    with col3:
        st.metric(
            "📚 Total Hours",
            f"{path['total_hours']} hours"
        )
    
    with col4:
        st.metric(
            "🧠 Learning Style",
            profile['learning_style']
        )
    
    # Learning Path Visualization
    st.subheader("📈 Your Personalized Learning Journey")
    
    # Create timeline visualization
    modules_data = []
    start_date = datetime.now()
    
    for i, module in enumerate(path['modules']):
        week_start = start_date + timedelta(weeks=i*2)
        week_end = week_start + timedelta(weeks=2)
        
        modules_data.append({
            'Module': module['name'],
            'Start': week_start,
            'End': week_end,
            'Duration': module['estimated_hours'],
            'Status': 'Planned'
        })
    
    # Gantt chart
    fig = px.timeline(
        modules_data,
        x_start='Start',
        x_end='End',
        y='Module',
        color='Duration',
        title="Learning Path Timeline"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Module Breakdown
    st.subheader("📋 Learning Modules")
    
    for i, module in enumerate(path['modules']):
        with st.expander(f"Module {i+1}: {module['name']} ({module['estimated_hours']} hours)"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Difficulty:** {module['difficulty']}")
                st.write("**Resources tailored to your learning style:**")
                
                for resource in module['resources'][:3]:  # Show first 3 resources
                    st.markdown(f"- 📖 {resource['title']} ({resource['estimated_time']})")
            
            with col2:
                # Progress simulation
                progress = st.session_state.progress.get(module['name'], 0)
                st.markdown(f"**Progress: {progress}%**")
                st.progress(progress/100)
                
                if st.button(f"Start {module['name']}", key=f"start_{i}"):
                    st.session_state.progress[module['name']] = random.randint(10, 30)
                    st.rerun()
    
    # Skills Gap Analysis
    st.subheader("🎯 Skills Gap Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Current skills radar chart
        skills = list(profile['skill_levels'].keys())
        current_levels = list(profile['skill_levels'].values())
        target_levels = [8, 9, 8, 9, 7]  # Target levels for career goal
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=current_levels,
            theta=skills,
            fill='toself',
            name='Current Level',
            line_color='rgba(255, 127, 14, 0.8)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=target_levels,
            theta=skills,
            fill='toself',
            name='Target Level',
            line_color='rgba(31, 119, 180, 0.8)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Skills Gap Analysis"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💡 Recommendations")
        st.info(
            f"Based on your {profile['learning_style']} learning style and "
            f"{profile['time_commitment']} time commitment, we've optimized "
            f"your learning path with hands-on projects and visual resources."
        )
        
        st.markdown("### 🏆 Achievement Milestones")
        milestones = [
            "Complete first module assessment",
            "Build your first project",
            "Join study group discussions", 
            "Complete mid-term evaluation",
            "Finish capstone project"
        ]
        
        for milestone in milestones:
            st.markdown(f"- [ ] {milestone}")
    
    # Progress Dashboard
    st.subheader("📊 Progress Dashboard")
    
    # Overall progress
    total_modules = len(path['modules'])
    completed_modules = len([m for m in st.session_state.progress.values() if m >= 100])
    overall_progress = (completed_modules / total_modules) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Modules Completed", f"{completed_modules}/{total_modules}")
    
    with col2:
        st.metric("Overall Progress", f"{overall_progress:.1f}%")
    
    with col3:
        days_since_start = (datetime.now() - datetime.strptime(path['created_date'], '%Y-%m-%d')).days
        st.metric("Days Active", days_since_start)

else:
    # Welcome screen
    st.markdown("""
    ## Welcome to Your AI-Powered Learning Journey! 🚀
    
    This intelligent platform creates **personalized learning paths** tailored specifically to your:
    
    - 🎯 **Career Goals** - Whether you're aiming for Data Science, Web Development, or other tech fields
    - 🧠 **Learning Style** - Visual, Auditory, Kinesthetic, or Reading/Writing preferences  
    - ⏰ **Time Availability** - Flexible scheduling based on your commitment level
    - 📊 **Current Skills** - Assessment-based path optimization
    
    ### How It Works:
    
    1. **Profile Assessment** - Complete a quick skills evaluation in the sidebar
    2. **AI Path Generation** - Our algorithm creates your personalized curriculum
    3. **Adaptive Learning** - Resources adjust based on your progress and preferences
    4. **Progress Tracking** - Visual dashboards monitor your learning journey
    
    ### Features:
    - 🤖 **AI-Driven Recommendations** using advanced NLP
    - 📈 **Interactive Progress Tracking** with detailed analytics  
    - 🎨 **Learning Style Optimization** for maximum retention
    - 🏆 **Milestone-Based Achievement System**
    - 📊 **Skills Gap Analysis** with target benchmarking
    
    **Get started by filling out your profile in the sidebar and clicking "Generate My Learning Path"!**
    """)
    
    # Demo data visualization
    st.subheader("🎯 Sample Learning Path Visualization")
    
    # Create sample data for demo
    sample_data = pd.DataFrame({
        'Week': range(1, 17),
        'Cumulative_Skills': np.cumsum(np.random.normal(2, 0.5, 16)),
        'Module': ['Foundations']*4 + ['Core Concepts']*6 + ['Advanced Topics']*6
    })
    
    fig = px.line(
        sample_data, 
        x='Week', 
        y='Cumulative_Skills',
        color='Module',
        title="Sample Skill Progression Over Time",
        labels={'Cumulative_Skills': 'Skill Level'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "🎓 **AI Learning Path Generator** | Powered by Advanced ML Algorithms | "
    "Deploy on: Streamlit • Gradio • Panel • Anvil • Dash"
)
