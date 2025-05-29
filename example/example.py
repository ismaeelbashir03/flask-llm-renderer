from flask import Flask
from flask_llm_renderer import LLMRenderer, render_html_from_json, create_app
from importlib.resources import files

app, renderer, socketio = create_app(api_key="PUT API KEY HERE FOR TESTING OR USE ENV VARIABLE ETC", model_name="claude-3-haiku-20240307")

@app.route("/render", methods=["POST"])
@render_html_from_json()
def handle_json():
    pass

if __name__ == "__main__":
    socketio.run(app, debug=True)
