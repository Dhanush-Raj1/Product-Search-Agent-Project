from flask import Flask, render_template, request
from agent_builder import ProductAgent
from exception import CustomException
import markdown

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    error = None
    
    if request.method == 'POST':
        try:
            task = request.form.get('query') 
            if not task:
                error = "Please enter a search query"
            else:
                product_agent = ProductAgent()
                agent_response = product_agent.perform_task(task)
                response_content = agent_response.content
                # Convert response to HTML for proper rendering
                response = markdown.markdown(str(response_content))
        except Exception as e:
            raise CustomException(e)
    
    return render_template('index1.html', response=response, error=error)

if __name__ == "__main__":
    app.run(debug=True)