from dotenv import load_dotenv
load_dotenv()

import pytz

from flask import Flask, redirect, render_template

from craigsbot.boundary import create_boundaries, is_coordinate_in_boundary
from craigsbot.db import initialize_database
from craigsbot.models import Posting

initialize_database()

app = Flask(__name__)
PST_TZ = pytz.timezone('America/Los_Angeles')
boundaries = create_boundaries()

boundary_map = {
    0: "Cow Hollow",
    1: "Mission",
    2: "Hayes Valley",
}


@app.route("/")
def root():
    return redirect('/page/1')

@app.route('/page/<int:page_number>')
def page(page_number):
    if page_number == 0:
        return redirect('/page/1')

    # calculate the skip value based on the page number
    skip = (page_number - 1) * 50

    # query for the paginated data
    headings = (("URL"),("Neighborhood"),("Posted"))
    data = []
    postings = Posting.objects(is_in_boundary=True).order_by("-_id").skip(skip).limit(50)
    for posting in postings:
        created = posting.id.generation_time
        pst_created = created.astimezone(PST_TZ)
        pst_created_fmt = pst_created.strftime('%m/%d/%Y %I:%M %p')
        url = posting.url
        neighborhood = None
        for i in range(len(boundaries)):
            is_in_boundary = is_coordinate_in_boundary(posting.latitude, posting.longitude, boundaries[i])
            if is_in_boundary:
                neighborhood = boundary_map[i]
                break
        data.append([posting.url, neighborhood, pst_created_fmt])

    # calculate the next and previous page numbers
    next_page = page_number + 1 if len(postings) == 50 else None
    prev_page = page_number - 1 if page_number > 1 else None

    # render the template with the paginated data and navigation links
    return render_template('table.html', headings=headings, data=data, next_page=next_page, prev_page=prev_page)
