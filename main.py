from taipy.gui import Gui
from pages.schedule import schedule_md
from pages.visuals import visuals_md

pages = {
    'Schedule': schedule_md,
    'Visuals': visuals_md
}

Gui(pages=pages).run(use_reloader=True, port=5001)
