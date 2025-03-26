from flask import Flask, render_template, request, jsonify
from deepseek_api import generate_travel_plan, generate_search_results
import os
import hashlib
import random
import requests

app = Flask(__name__)

# Load API key from environment variable
DEEPSEEK_API_KEY = "sk-aabaf25b45ba456c87f8a899826c6e6b"

if not DEEPSEEK_API_KEY:
    print("Error: DEEPSEEK_API_KEY environment variable not set.  The application will not work.")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/architecture')
def architecture():
    return render_template('architecture.html')

@app.route('/calligraphy')
def calligraphy():
    return render_template('calligraphy.html')

@app.route('/compass')
def compass():
    return render_template('compass.html')

@app.route('/empires')
def empires():
    return render_template('empires.html')

@app.route('/gunpower')
def gunpowder():
    return render_template('gunpower.html')

@app.route('/han', methods=["GET", "POST"])
def han():
    return render_template('han.html')
@app.route('/inventions')
def inventions():
    return render_template('inventions.html')

@app.route('/jin')
def jin():
    return render_template('jin.html')

@app.route('/literature')
def literature():
    return render_template('literature.html')

@app.route('/medicine')
def medicine():
    return render_template('medicine.html')

@app.route('/ming')
def ming():
    return render_template('ming.html')

@app.route('/paper')
def paper():
    return render_template('paper.html')

@app.route('/philosophy')
def philosophy():
    return render_template('philosophy.html')

@app.route('/qin')
def qin():
    return render_template('qin.html')

@app.route('/qing')
def qing():
    return render_template('qing.html')

@app.route('/shang')
def shang():
    return render_template('shang.html')

@app.route('/song')
def song():
    return render_template('song.html')

@app.route('/sui')
def sui():
    return render_template('sui.html')

@app.route('/tang')
def tang():
    return render_template('tang.html')

@app.route('/xia')
def xia():
    return render_template('xia.html')

@app.route('/yuan')
def yuan():
    return render_template('yuan.html')

@app.route('/zhou')
def zhou():
    return render_template('zhou.html')

@app.route("/travel", methods=["GET", "POST"])
def travel():
    travel_plan = None
    error_message = None  # To display errors in the template

    if request.method == "POST":
        if not DEEPSEEK_API_KEY:
            error_message = "DeepSeek API key not configured.  Please set the DEEPSEEK_API_KEY environment variable."
        else:
            destination = request.form.get("destination")
            duration = request.form.get("duration")
            interests = request.form.get("interests")

            if not destination or not duration or not interests:
                error_message = "Please fill in all the fields."
            else:
                try:
                    travel_plan = generate_travel_plan(destination, duration, interests, DEEPSEEK_API_KEY)
                    if not travel_plan:  # Check if travel_plan is empty or None
                        travel_plan = "No travel plan generated. Please try again." # Message if travel plan fails
                except Exception as e:
                    error_message = f"An error occurred while generating the travel plan: {e}"
                    travel_plan = "An error occurred. Please try again."  # Display error message in popup


    return render_template("travel.html", travel_plan=travel_plan, error_message=error_message)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('searchInput')
    if not search_query:
        return render_template('search_results.html',
                               search_query=search_query,
                               error_message="Please enter a search term")

    try:
        # Get enhanced search results with images
        result = generate_search_results(search_query, DEEPSEEK_API_KEY)

        if not result:
            return render_template('search_results.html',
                                   search_query=search_query,
                                   error_message="No results found")

        return render_template('search_results.html',
                               search_query=search_query,
                               overview=result.get('overview'),
                               facts=result.get('facts', []),
                               image_urls=result.get('image_urls', []))

    except Exception as e:
        return render_template('search_results.html',
                               search_query=search_query,
                               error_message=f"Search error: {str(e)}")



if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for development