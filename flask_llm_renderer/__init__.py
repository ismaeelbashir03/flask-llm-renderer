import importlib
from .core import render_html_from_json
import logging
from flask import Flask
from importlib.resources import files

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LLMRenderer:
    def __init__(self, app=None, api_key=None, model_name=None):
        """
        Initialize the LLMRenderer with an optional Flask app and OpenAI API key.
        
        :param app: Flask application instance
        :param api_key: OpenAI API key for authentication
        :type app: Flask

        :type api_key: str
        :return: None
        """
        self.api_key = api_key
        self.model_name = model_name
        if app: self.__init_app(app)

    def __init_app(self, app):

        # setup sockets fot real time rendering
        from flask_socketio import SocketIO
        socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")
        app.llm_renderer_socketio = socketio

        # setup llm extension configs
        model_name = self.model_name or app.config.get("LLM_RENDERER_MODEL_NAME", "gpt-3.5-turbo")
        app.llm_renderer_model_name = app.config.get("LLM_RENDERER_MODEL_NAME", "gpt-3.5-turbo")
        
        if "gpt" in model_name:
            openai_api_key = self.api_key or app.config.get("OPENAI_API_KEY")
            
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_api_key)
                app.llm_renderer_client = client
                app.llm_renderer_chat_fn = lambda prompt, temp=0.5: client.chat.completions.create(
                    model=model_name,
                    temperature=temp,
                    messages=[
                        {"role": "system", "content": "You are a frontend assistant."},
                        {"role": "user", "content": prompt}
                    ]
                ).choices[0].message.content
            except (ImportError, AttributeError):
                import openai
                openai.api_key = openai_api_key
                app.llm_renderer_client = openai
                app.llm_renderer_chat_fn = lambda prompt, temp=0.5: openai.ChatCompletion.create(
                    model=model_name,
                    temperature=temp,
                    messages=[
                        {"role": "system", "content": "You are a frontend assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )['choices'][0]['message']['content']

        elif "claude" in model_name:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key or app.config.get("ANTHROPIC_API_KEY"))
            app.llm_renderer_client = client
            app.llm_renderer_chat_fn = lambda prompt, temp=0.5: client.messages.create(
                model=model_name,
                temperature=temp,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            ).content[0].text

        else:
            raise ValueError(f"Unsupported model name: {model_name}")

        logger.debug(f"LLM Renderer initialized with model: {model_name}")
        logger.debug(f"Template folder: {app.template_folder}")

        # setup the html template view at /view endpoint
        @app.route("/")
        def view_json():
            from flask import render_template
            return render_template("viewer.html")

        return socketio

    def get_socketio(self, app):
        return app.llm_renderer_socketio

def create_app(api_key=None, model_name=None, **flask_kwargs):
    from importlib.resources import files
    from flask import Flask

    template_path = files(__package__).joinpath("templates")
    app = Flask(__name__, template_folder=str(template_path), **flask_kwargs)
    app.config["OPENAI_API_KEY"] = api_key
    renderer = LLMRenderer(app, api_key=api_key, model_name=model_name)
    socketio = renderer.get_socketio(app)
    return app, renderer, socketio
