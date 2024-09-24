import json
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import pandas as pd
from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go

def extract_after_tree(url, substring):
    # Find the position of "tree/" in the URL
    tree_index = url.find(f"{substring}/")

    # If "tree/" is found, return the substring after it
    if tree_index != -1 and substring == "tree":
        return url[tree_index + 5:]  # 5 is the length of "tree/"
    elif tree_index != -1 and substring == "commit":
        return url[tree_index + 7:]
    else:
        return "None"


dfBL = pd.read_excel(
    "C:/Users/miqui/OneDrive/Progressive Insurance/PL-DirectAcq/Flask/BL - Tracker.xlsx", sheet_name="Tracker")
dfBL["commit_url"] = dfBL["Commit"]
dfBL["branch_url"] = dfBL["Branch"]
dfBL["Branch"] = dfBL["Branch"].apply(extract_after_tree, substring="tree")
dfBL["Commit"] = dfBL["Commit"].apply(extract_after_tree, substring="commit")

def create_plot():
    fig =go.Figure(go.Icicle(
        labels=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
        values=[10, 14, 12, 10, 2, 6, 6, 4, 4],
        root_color="lightgrey"
    ))

    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    plot_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    return plot_json

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        if template.endswith("landing.html"):
            return render_template("home/landing.html")
        elif template.endswith("demo.html"):
            return render_template("home/demo.html", df=dfBL)
        elif template.endswith("models.html"):
            return render_template("home/models.html", df=dfBL)
        elif template.endswith("tree.html"):
            plot = create_plot()
            return render_template("home/tree.html", df=dfBL, plot=plot)
        else:
            return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
