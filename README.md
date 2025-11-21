Project Overview

This project is a Flask-based web application that helps users find the nearest MBTA station to a given place in the Greater Boston area. When the user enters a place name or address, the app uses Mapbox’s geocoding API to convert the location into latitude and longitude. Those coordinates are then used to call the MBTA API to determine the closest transit stop and whether it is wheelchair accessible. The app displays the results through a clean interface built with Flask templates.

As our “wow” feature, we added real-time weather information. Using the OpenWeather API, the app retrieves the current weather near the user’s searched location. This gives users an additional layer of helpful context beyond the nearest station.

Reflection
Development Process

We split our work intentionally and worked on the project evenly. One of us focused on the backend logic: building mbta_helper.py, structuring the API requests, cleaning up JSON responses, and making sure the coordinates and station information were accurate. The other built the Flask framework, connected the routes, designed the templates, and made sure the frontend communicated smoothly with the backend.

Most of our debugging time happened during the API stage, especially when Mapbox returned different JSON shapes or MBTA returned no stations for certain queries. Testing each helper function in isolation helped us move from confusion to clarity pretty quickly. Once the backend was stable, integrating everything into Flask went smoothly. Adding the weather feature felt natural because our helper functions were already organized, and we just extended the structure we had built.

If we were to do this again, we would set up template placeholders earlier and test the error cases sooner. But overall, our step-by-step approach made the project feel manageable and structured.

Teamwork & Work Division

We worked together and split the work 50–50.

Backend 

Implemented API calls for Mapbox and MBTA

Wrote and tested helper functions (get_json, get_lat_lng, get_nearest_station)

Added weather logic in mbta_helper.py

Debugged JSON parsing and URL formatting

Flask + Frontend 

Built Flask routes and connected the backend to the frontend

Created the HTML templates (index.html, mbta_station.html, error.html)

Handled form submission, POST requests, and rendering data

Integrated the weather data into the results page

We collaborated whenever something broke or didn’t look right. Even though we divided the tasks, we reviewed everything together and made sure both sides understood the full flow of the project.

Learning & Use of AI Tools

We used AI as a support tool while still making sure the core logic and decisions were our own. AI helped us clarify API documentation, understand JSON structures, and troubleshoot specific errors we encountered with URL parameters or unusual API responses. It also helped us think through implementation approaches when we weren’t sure how to connect two parts of the app.

But we wrote and tested the real logic ourselves. We examined every API output manually, validated the structure of our helper functions, and confirmed the Flask flow through our own testing. AI never wrote large sections of the project for us; it mainly acted as a debugging and explanation resource.

ALL SCREENSHOTS OF ERRORS AND IMPORTANT STEPS HAVE BEEN ADDED TO SCREENSHOTS FOLDER IN THIS REPOSITORY 


