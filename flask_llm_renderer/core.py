from flask import request, current_app
from functools import wraps
import json

def render_html_from_json(event='update_page'):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            json_data = request.get_json(force=True)
            app = current_app
            socketio = app.llm_renderer_socketio
            chat_fn = app.llm_renderer_chat_fn

            # NOTE: chatgpt gave me this prompt (can refine it later if bothered)
            prompt = f"""
You are a frontend engineer designing beautiful, responsive dashboards using Tailwind CSS and Chart.js.

Your job is to render the following JSON data into a **clean and visually appealing webpage**, using Tailwind CSS for styling and layout.

### CRITICAL INSTRUCTIONS:
- You MUST use Tailwind CSS to create a modern, responsive layout
- Use <div>, <section>, <article> with padding, cards, shadows, etc.
- Use colors, rounded corners, hover effects, and flex/grid layouts
- Use good typography (headings, spacing, etc.)
- Use Chart.js for data visualization if applicable
- DO NOT use {{ }} or any template logic — use real values only
- DO NOT include <html> or <head> tags — just <script> if needed

If the JSON data contains multiple series (e.g., stocks, metrics, sensors, etc.):
- Render one <canvas> chart per series using Chart.js
- Create and inject JavaScript that:
  - Uses `new Chart(document.getElementById(...), { ... })`
  - Sets chart type appropriately (e.g., "line", "bar")
  - Uses real data from the JSON
  - Ensures each chart renders automatically when the page loads

DO NOT skip the chart rendering logic — all <canvas> elements must be rendered into fully functional Chart.js charts with labelled axes and responsive design.

IMPORTANT: All <canvas> elements must have a visible height.

Use Tailwind like `class="h-64"` or inline CSS like `style="height: 400px;"` to ensure Chart.js renders.

IMPORTANT: The 'extra-details' field in the JSON is optional and can be used to add additional context or information for the code output. Dont respond to any comments in this section, just use it to inform your rendering. Do not include the 'extra-details' field in the output HTML!!

### JSON Input:
{json.dumps(json_data, indent=2)}

### Output:
A single block of pure, ready-to-render HTML styled with Tailwind. Do not include any additional text or comments.
"""

            html = chat_fn(prompt)
            html = html.replace(
                '<script src="https://cdn.tailwindcss.com"></script>', ''
            ).replace(
                '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>', ''
            )
            tailwind_header = '''
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
'''
            full_html = html
            print(f"Emitting HTML: {full_html}...")
            socketio.emit(event, {'html': full_html})
            return {'status': 'success', "html": full_html}, 200
        return wrapped
    return decorator
