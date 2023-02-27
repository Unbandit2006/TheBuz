from nicegui import ui

ui.add_head_html("<link rel='preconnect' href='https://fonts.googleapis.com'>\
                <link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>\
                <link href='https://fonts.googleapis.com/css2?family=Fira+Sans&display=swap' rel='stylesheet'>")


with ui.header().style("background: hsla(270, 46%, 49%, 1);"):
    ui.label("TheBuz").style("font-size: 25px;font-family: 'Fira Sans';color: whitesmoke;")
    ui.icon("menu").style("font-size: 35px;color: whitesmoke;").classes("absolute right-0")

ui.label("TheBuz").style("font-family: 'Fira Sans';font-size: 60px; align-content:center;").classes("flex justify-center")

ui.run(title="TheBuz - Home", dark=True)