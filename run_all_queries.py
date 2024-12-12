import os
import sys
import re

# Ensure the current project root is in PYTHONPATH so backend can be imported.
project_root = os.path.abspath(os.path.join(os.getcwd()))
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.apis import generate_cosine_similarity_graph

# Define a broader set of queries:
# queries = [
#     "How can I prepare for an interview?",
#     "Interview preparation resources provided by Humber Career Services",
#     "Tips from Humber's career resources on interview preparation",
#     "Mock interview sessions at Humber College",
#     "Interview preparation workshops Humber College",
#     "Humber Career Centre interview coaching",
#     "Resources on career preparation from Humber College virtual advising",
#     "Career resources at Humber College for improving interview skills",
#     "Behavioral interview preparation guides from Humber career resources",
#     "What documents do I need to prepare before an interview at Humber?",
#     "How to improve my resume for interviews using Humber's resources",
#     "Does Humber College offer practice interviews or mock sessions?",
#     "Advice on answering common interview questions from Humber Career Services",
#     "How to handle behavioral interviews with Humber’s career guidance",
#     "Interview follow-up email tips from Humber College career site",
#     "Detailed interview preparation checklist from Humber career resources",
#     "Step-by-step interview preparation guide on Humber College career site",
#     "Humber career services resume and interview improvement tools",
#     "Virtual advising sessions for interview skill-building at Humber",
#     "FAQs about interview strategies from Humber's career Q&A page",
#     "Faculty support pages offering interview guidance at Humber College",
#     "Techniques to handle behavioral interview questions on Humber resources-career page",
#     "Humber career advising appointments for interview rehearsal and coaching",
#     "Improving interview confidence through Humber's career advising Q&A",
#     "List of interview preparation resources for Humber students and alumni"
# ]

# queries = [
#     "How can I schedule an interview coaching appointment through Humber's student-online-services page?",
#     "Interview preparation advice offered on Humber's career-advising page",
#     "Improving interview techniques using Humber’s resources-career and student-online-services",
#     "Common interview questions answered on Humber’s questions-answers page for better preparation",
#     "Finding behavioral interview preparation tips on Humber's faculty-services and resources-career pages",
#     "What interview preparation workshops are listed on Humber’s faculty-services and career-advising pages?",
#     "Enhancing interview readiness through Humber's student-online-services and questions-answers pages",
#     "Does Humber’s career-advising section provide interview rehearsal sessions or coaching?",
#     "How to use Humber’s student-online-services to find mock interview opportunities?",
#     "Guidance on answering interview questions through Humber’s resources-career and career-advising pages"
# ]

# queries = [
#     "Where can I find online-learning modules for enhancing interview techniques through Humber’s student-online-services?",
#     "Interactive video tutorials on interview preparation offered by Humber’s resources-online-learning and career-advising pages",
#     "Step-by-step online interview preparation course available at Humber’s resources-online-learning platform",
#     "How to access interview skill-building tutorials on Humber’s resources-online-learning combined with faculty-services?",
#     "Comprehensive online guides for interview readiness found on Humber’s student-online-services and resources-career sections",
#     "Improving behavioral interview strategies through Humber’s resources-online-learning and questions-answers pages",
#     "Online resume and interview improvement tools accessible through Humber’s student-online-services and resources-online-learning",
#     "Finding a virtual, structured interview coaching program at Humber’s resources-online-learning and career-advising",
#     "Enhancing interview confidence with Humber’s interactive online-learning modules and student-online-services support",
#     "Where does Humber’s resources-online-learning platform provide mock interview practice sessions and step-by-step preparation?"
# ]

queries = [
    "Advanced interactive modules on Humber’s resources-online-learning for step-by-step interview preparation and improvement",
    "How to enroll in a comprehensive online interview preparation course using Humber’s resources-online-learning and student-online-services",
    "Interactive mock interview simulations available at Humber’s resources-online-learning page to improve interview readiness",
    "Online career coaching sessions focused on interview techniques accessible through Humber’s resources-online-learning and student-online-services platforms",
    "Detailed resume and interview preparation toolkit integrated with Humber’s student-online-services and resources-online-learning"
]



def sanitize_filename(s: str) -> str:
    # Replace non-alphanumeric characters with underscores
    return re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')

top_n = 5

for i, query in enumerate(queries, start=1):
    print(f"\n=== Query {i}: {query} ===")
    generate_cosine_similarity_graph(query, top_n=top_n)

    # Rename the generated plot for easier identification
    output_filename = f"cosine_similarity_plot_{sanitize_filename(query)[:50]}.png"
    if os.path.exists("cosine_similarity_plot.png"):
        # If a file with the same name exists, remove it first
        if os.path.exists(output_filename):
            os.remove(output_filename)
        os.rename("cosine_similarity_plot.png", output_filename)
        print(f"Plot saved as {output_filename}\n")
    else:
        print("No plot file found. Check if the function created it.\n")
