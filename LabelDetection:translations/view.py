from flask import render_template
from flask.views import MethodView
import gbmodel

class View(MethodView):

    def get(self):
        model = gbmodel.get_model()
        entries = [dict(label1=row[0], label2=row[1], label3=row[2], label4=row[3], label5=row[4], translated1=row[5],translated2=row[6],translated3=row[7],translated4=row[8],translated5=row[9],image_public_url=row[10] ) for row in model.select()]
        return render_template('view.html', Entries=entries)
