import reflex as rx
import validators
import asyncio
from rxconfig import config
from gemini import analyse
from firecrawl_scraper import scrape


# SCRAPE JOB DESCRIPTION AND RUN ANALYSIS
async def scrape_and_analyse(**kwargs):
    loop = asyncio.get_event_loop()

    # Make the firecrawl sdk to fit into asynchronous.
    response = await loop.run_in_executor(None, scrape, kwargs.get("link"))

    print(response)

    if response["is_valid"]:
        result = analyse(
            job_description=response["job_details"],
            industry=kwargs.get("industry"),
            years=kwargs.get("years"),
            skills=kwargs.get("skills"),
            education=kwargs.get("education"),
            career=kwargs.get("career"),
            tools=kwargs.get("tools")
        )
        return result.text
    return False



class FormState(rx.State):
    is_submitted: bool = False
    select_field_value: str = "1-2",
    is_invalid_url: bool = False
    is_loading: bool = False
    editor_content: str = "<p>content here</p>"


    # HANDLE FORM SUBMISSION
    @rx.event
    async def submit_form(self, form_data: dict):
        link = form_data["link"]
        if validators.url(link):
            try:
                result = await scrape_and_analyse(**form_data)
                if not result:
                    error_message = "The URL you submitted is either invalid, or contains no details about a job listing"
                    self.editor_content = error_message
                else:
                    self.editor_content = result
            except Exception as e:
                self.editor_content = "An error occured. Retry your request!"
            
            self.is_loading = False
            self.is_invalid_url = False
            self.is_submitted = True
        
        else:
            self.is_loading = False
            self.is_invalid_url = True

    @rx.event
    def back(self):
        self.is_submitted = False

    @rx.event
    def button_clicked(self):
        self.is_loading = True

    @rx.event
    def set_content(self, content: str):
        self.editor_content = content



def form():
    return rx.cond(
        FormState.is_submitted,
        rx.card(
            rx.vstack(
                rx.text(
                "The result of the analysis" 
                ),
                rx.editor(
                    set_contents=FormState.editor_content,
                    on_change=FormState.set_content

                ),
                rx.button("Back", on_click=FormState.back)
            )
        ),
        rx.card(
            rx.form(
                rx.vstack(
                    rx.box(
                        rx.cond(
                            FormState.is_invalid_url,
                            rx.text("Invalid URL", size="2", color="red")
                        ),
                        rx.text("Job post link"),
                        rx.input(
                            placeholder="the URL to the Job listing",
                            required=True,
                            variant="surface",
                            size="3",
                            radius="full",
                            width="100%",
                            name="link"
                        ),
                        padding="6px",
                        width="100%",
                    ),

                    rx.box(
                        rx.text("Current job title and industry"),
                        rx.input(
                            placeholder="e.g Software Engineer, Technical writer, ML engineer, etc.",
                            required=True,
                            variant="surface",
                            size="3",
                            radius="full",
                            width="100%",
                            name="industry"
                        ),
                        padding="6px",
                        width="100%",
                    ),

                    rx.box(
                        rx.text("Years of professional experience"),
                        rx.select(
                            ["0-1", "2-4", "5-7", "8-10", "10+"]
                        ),
                        padding="6px",
                        name="years"
                    ),
                    
                    rx.box(
                        rx.text("Key skills and expertise"),
                        rx.text_area(
                            placeholder="e.g Python, Project management, technical writing, software development, etc.",
                            width="100%",
                            resize="both",
                            required=True,
                            variant="surface",
                            size="3",
                            radius="full",
                            name="skills"
                        ),
                        padding="6px",
                        width="100%",
                    ),

                    rx.box(
                        rx.text("Highest educational qualification and certifications"),
                        rx.text_area(
                            placeholder="e.g Bachelor's in computer science, AWS certified solutions architect, etc.",
                            resize="both",
                            required=True,
                            variant="surface",
                            size="3",
                            radius="full",
                            width="100%",
                            name="education"
                        ),
                        padding="6px",
                        width="100%",
                    ),

                    rx.box(
                        rx.text("Career highlights and major milestones"),
                        rx.text_area(
                            placeholder="e.g Successfully led a team to deliver a product feature that increased user engagement by 20%, open source collaborations, job experience, etc.",
                            resize="both",
                            required=True,
                            variant="surface",
                            size="3",
                            radius="full",
                            width="100%",
                            name="career"
                        ),
                        padding="6px",
                        width="100%",
                    ),

                    rx.box(
                        rx.text("Tools/technologies/framweworks (if applicable)"),
                        rx.text_area(
                            placeholder="e.g Python, Javacsript, Microsoft word, etc.",
                            resize="both",
                            required=True,
                            variant="surface",
                            size="3",
                            radius="full",
                            width="100%",
                            name="tools"
                        ),
                        padding="6px",
                        width="100%",
                    ),
                    rx.button(
                        rx.cond(
                            FormState.is_loading,
                            rx.vstack(
                                rx.spinner(size="3"),
                                rx.text(rx.text.em("Processing, may take up to 10-15 seconds..."), size="2", color="#E38E49")
                            ),
                            rx.text("Submit")
                        ),
                        type="submit",
                        on_click=FormState.button_clicked,
                        disabled=FormState.is_loading,
                        bg="#E38E49" 

                    )
                ),
                on_submit=FormState.submit_form,
            ),
            font_family="SUSE",
        )
    )

def features():
    return rx.grid(
        rx.card(
            rx.box(
                rx.icon("circle_check_big", color="#E38E49"),
                rx.text("Get a matching score based on your profile and the job description."),
            )
        ),

        rx.card(
            rx.box(
                rx.icon("circle_check_big", color="#E38E49"),
                rx.text("Generate a personalized cover letter tailored to the job description, reflecting the company’s style and tone."),
            )
        ),

        rx.card(
            rx.box(
                rx.icon("circle_check_big", color="#E38E49"),
                rx.text("Get personalized advice to improve your application and make it stand out")
            ),
        ),
        width="100%",
        spacing="4",
        font_family="SUSE",
        columns=rx.breakpoints(initial="1", sm="1", md="3", lg="3")
    )


def navbar():
    return rx.box(
        rx.hstack(
            rx.image(
                src="",
                width="2.25em",
                height="auto",
                border_radius="25%",
            ),

            rx.heading(
                rx.text.em("Coverly", font_family="Sacramento"), size="6", weight="bold", color="#E38E49"
            ),
            align_items="center"
        ),
        width="100%",
        padding="1em",
        top="0px"
    )


def footer():
    return rx.el.footer(
        rx.vstack(
            rx.text("Built with love by Edun Rilwan."),
            width="100%"
        ),
        justify="center"
    )

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        navbar(),
        rx.color_mode.button(position="top-right"),
        rx.section(
            rx.center(
                rx.vstack(
                    rx.heading("Get",  rx.text.em(" hired faster", color="#E38E49"), " with Tailored applications!", size="7"),
                    rx.text(
                        "Analyze job descriptions, improve your profile, and create compelling cover letters effortlessly.",
                        size="4",
                    ),
                    width="80%",
                    spacing="5",
                    justify="center",
                    font_family="SUSE",
                )
            )
        ),

        rx.section(
            rx.center(
                features()
            )
        ),

        rx.section(
            rx.center(
                form() 
            )
        )
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Sacramento&family=Inconsolata&family=New+Amsterdam&family=SUSE:wght@100..800&display=swap"
    ]
)
app.add_page(index)
