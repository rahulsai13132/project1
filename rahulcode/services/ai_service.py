"""
SmartCampus AI - AI Assistant Service
Integrates OpenAI API for intelligent student Q&A, notice summaries, placement guidance, mock interview prep, and career roadmaps.
Includes a robust fallback response generator for offline or unconfigured API key environments.
"""
from typing import List, Dict, Any, Optional
from core.config import Config
from utils.logger import logger

class AIService:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.client = None
        if self.api_key and self.api_key != "YOUR_OPENAI_API_KEY":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")

    def generate_chat_response(
        self,
        user_message: str,
        chat_history: List[Dict[str, str]],
        user_context: Optional[Dict[str, Any]] = None,
        notices_context: Optional[List[Dict[str, Any]]] = None,
        placements_context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Generates AI assistant response using OpenAI API or fallback engine."""
        # Check if live client available
        if self.client:
            try:
                system_prompt = self._build_system_prompt(user_context, notices_context, placements_context)
                messages = [{"role": "system", "content": system_prompt}]
                
                # Append last 6 messages of conversation history for context
                for msg in chat_history[-6:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                
                messages.append({"role": "user", "content": user_message})

                response = self.client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=800
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"OpenAI API call failed: {str(e)}. Falling back to SmartCampus AI Knowledge Engine.")
                return self._generate_fallback_response(user_message, user_context, notices_context, placements_context)
        else:
            return self._generate_fallback_response(user_message, user_context, notices_context, placements_context)

    def _build_system_prompt(self, user_context, notices_context, placements_context) -> str:
        """Constructs system prompt with campus context."""
        user_name = user_context.get("full_name", "Student") if user_context else "Student"
        user_dept = user_context.get("department", "Engineering") if user_context else "Engineering"
        user_year = user_context.get("year", "Final Year") if user_context else "Final Year"

        prompt = (
            f"You are SmartCampus AI, an expert academic and career advisor assistant for {user_name} "
            f"in {user_dept} ({user_year}).\n"
            "Provide helpful, encouraging, accurate, and concise guidance regarding college notices, placements, "
            "resume improvements, interview preparation, workshop recommendations, and career roadmaps.\n"
        )

        if notices_context:
            prompt += f"\nCurrent Active College Notices: {str(notices_context[:3])}\n"
        if placements_context:
            prompt += f"\nCurrent Placement Opportunities: {str(placements_context[:3])}\n"

        return prompt

    def _generate_fallback_response(
        self,
        user_message: str,
        user_context: Optional[Dict[str, Any]],
        notices_context: Optional[List[Dict[str, Any]]],
        placements_context: Optional[List[Dict[str, Any]]]
    ) -> str:
        """Generates dynamic domain-aware responses when API key is missing or offline."""
        msg = user_message.lower()
        user_name = user_context.get("full_name", "Student") if user_context else "Student"
        user_dept = user_context.get("department", "Engineering") if user_context else "Engineering"

        if "notice" in msg or "announcement" in msg or "summary" in msg:
            if notices_context:
                top_notice = notices_context[0]
                return (
                    f"📢 **SmartCampus Notice Summary for {user_name}**:\n\n"
                    f"**Latest Notice**: {top_notice.get('title')}\n"
                    f"**Publisher**: {top_notice.get('publisher')} | **Priority**: {top_notice.get('priority')}\n\n"
                    f"{top_notice.get('description')}\n\n"
                    "💡 *Tip: Visit the Notice Board page for full filters and priority sorting.*"
                )
            return "📢 Currently there are no active notices on the notice board."

        elif "placement" in msg or "job" in msg or "interview" in msg or "resume" in msg:
            if placements_context:
                top_job = placements_context[0]
                return (
                    f"💼 **Placement Guidance & Active Opportunity**:\n\n"
                    f"🚀 **Featured Role**: {top_job.get('company')} - Package: {top_job.get('package')}\n"
                    f"📍 **Location**: {top_job.get('location')}\n"
                    f"🛠 **Key Skills**: {top_job.get('skills_required')}\n"
                    f"⏳ **Deadline**: {top_job.get('deadline')}\n\n"
                    "🎯 **Resume & Interview Preparation Tips**:\n"
                    "1. Highlight projects using Python, Cloud Services, or AI/ML frameworks.\n"
                    "2. Follow the STAR method (Situation, Task, Action, Result) in technical interviews.\n"
                    "3. Ensure your LinkedIn and GitHub profiles feature clean, documented repositories."
                )
            return "💼 High placement activity expected soon! Keep your resume updated in your Settings."

        elif "workshop" in msg or "event" in msg or "train" in msg:
            return (
                f"🎯 **Recommended Workshops for {user_dept}**:\n\n"
                "1. **Generative AI & LLM Fine-Tuning**: Learn LangChain, PyTorch, and AI Agent architecture.\n"
                "2. **Modern Cloud DevOps**: Hands-on Kubernetes, Docker, and Terraform labs.\n\n"
                "👉 Visit the **Workshops** section from the sidebar to reserve your seat!"
            )

        elif "roadmap" in msg or "career" in msg or "skill" in msg:
            return (
                f"🗺 **Career Growth Roadmap for {user_dept} ({user_context.get('year', 'Student')})**:\n\n"
                "1. **Phase 1 (Core Foundations)**: Master Data Structures, Algorithms, System Design basics.\n"
                "2. **Phase 2 (Specialization)**: Build 2-3 full-stack AI/ML or Cloud projects with clean code.\n"
                "3. **Phase 3 (Industry Readiness)**: Conduct mock technical interviews, update resume, apply to campus drives."
            )

        else:
            return (
                f"Hello {user_name}! 👋 I am **SmartCampus AI Assistant**.\n\n"
                f"How can I assist your studies or career journey today in **{user_dept}**?\n\n"
                "You can ask me to:\n"
                "• Summarize campus notices 📢\n"
                "• Give placement prep & resume tips 💼\n"
                "• Recommend skill workshops 🎯\n"
                "• Generate a career growth roadmap 🗺\n"
                "• Prepare mock interview questions 🧠"
            )
