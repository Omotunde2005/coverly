import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()


genai.configure(api_key=os.environ.get("GEMINI_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")



def analyse(**kwargs):
   prompt = f"""
   **Task**: You are an AI assistant helping users analyze job descriptions and improve their applications. Your goal is to:  
   1. Provide a **matching score** based on the user's profile and the job description.  
   2. Generate a **personalized cover letter** tailored to the job description, reflecting the company’s style and tone.  
   3. Offer **advice to improve the application** and make it stand out.  
   4. IF the score is below %70, automatically let the user know they are not qualified. Do not include a cover letter. Only include advice that could help the user gain required experience
   to apply for the job.

   **Inputs**:  
   {kwargs.get("job_description")}

   - **User Profile**:  
   - Current Job Title and Industry: {kwargs.get("industry")}
   - Years of Experience: {kwargs.get("years")}
   - Key Skills: {kwargs.get("skills")}  
   - Education and Certifications: {kwargs.get("education")}
   - Career Highlights: {kwargs.get("career")}
   - Tools and Technologies:  {kwargs.get("tools")}

   ---

   **Output Requirements**:  

   1. **Matching Score**:  
      - Calculate a score out of 100 to show how well the user matches the job description.  
      - Base the score on alignment of required skills, qualifications, and experience in the JD with the user profile.  

   2. **Cover Letter**:  
      - Write a personalized cover letter tailored to the job description.  
      - Analyze the tone and style of the JD to match the company's voice (e.g., playful, serious, professional).  
      - Highlight the user's most relevant skills, achievements, and qualifications in a concise, impactful way.  

   3. **Application Improvement Advice**:  
      - Identify gaps between the user's profile and the job requirements (e.g., missing skills or certifications).  
      - Suggest actionable steps to improve their application, such as taking specific courses, gaining relevant experience, or rephrasing their resume.  
      - Provide tips for making the cover letter and resume more compelling based on industry best practices.  
   4. **The response should be HTML formatted**:
      - <p>a paragraph...</p>
      - <h3>An header.</h3>
      

   ---

   **Example Output**:  

   1. **Matching Score**:  
      - "Your profile matches 85% of the requirements for this job."  

   2. **Cover Letter**:  
      - *Dear [Hiring Manager’s Name],  
      I am excited to apply for the [Job Title] role at [Company Name]. With over [X years] of experience in [relevant field/industry], I have honed skills such as [key skills] that directly align with the requirements in your job posting.  
      [Include an achievement relevant to the role, tied to a requirement in the JD.]  
      I admire your company’s [tone/style element from JD, e.g., innovative approach to marketing], and I am eager to contribute my [specific expertise] to support your goals. I would welcome the opportunity to discuss how my skills align with your needs.  
      Sincerely,  
      [Your Name]*  

   3. **Advice**:  
      - "To enhance your application:  
      - Add [specific certification/skill from JD].  
      - Highlight more examples of [a missing requirement].  
      - Emphasize [a unique strength or qualification] in your resume or LinkedIn profile."  

   ---


   """

   response = model.generate_content(prompt)
   return response