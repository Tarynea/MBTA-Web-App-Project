Project Overview

This project is a Flask-based web application that helps users locate the nearest MBTA station to any entered place or address in the Greater Boston area. After the user submits a location, the app:

1. Converts the place name into coordinates using Mapbox
2. Finds the nearest MBTA station using the MBTA v3 API
3. Retrieves the station’s wheelchair accessibility status
4. Displays additional helpful “wow” features
5. Our final app includes four major wow features:
6. Real-time weather for the searched location
7. Estimated walking time to the nearest MBTA stop
8. A dynamic map preview showing the stop location
9. Real-time service alerts affecting that specific stop

This creates a user-friendly tool that combines multiple live data sources into one simple interface.

How The App Works-

User Experience Flow:
User enters a place → submits form
App geocodes the address
App finds the closest MBTA stop

App fetches:
Weather
Walking estimate
Station accessibility
Map image
Service alerts
Results are displayed on a clean, readable results page
If anything fails (missing location, bad API response, etc.), the user sees a friendly error page

APIs Used:
Mapbox Searchbox API – convert location → coordinates
Mapbox Static Maps API – map preview
MBTA API – station data + alerts
OpenWeather API – live weather

Wow Features-
1. Real-Time Weather: Shows temperature and weather conditions at the user’s searched location.
2. Estimated Walking Time:Uses geographic distance + average walking speed to make the result more useful.
3. Map Preview: Displays a static Mapbox map with the MBTA stop marked clearly.
4. MBTA Service Alerts:Shows relevant warnings or updates for the stop so the user can plan ahead.

Team Contributions-

We collaborated throughout the project, but the division of work reflects what each of us focused on most.

Tarynea’s Contributions-
-Built and refined all backend logic in mbta_helper.py
-Integrated all wow features (weather, walking time, map, alerts)
-Handled API troubleshooting, testing, and debugging
-Structured the backend–frontend connection
-Designed the deployment setup and configured PythonAnywhere
-Ensured data validation, error handling, and UX consistency
-Wrote documentation, organized the GitHub repo, and finalized the project

Tamanna’s Contributions-
-Set up the Flask app structure (app.py routing & framework)
-Created and refined HTML templates: index.html, error.html, and parts of mbta_station.html
-Helped test the overall flow and verify API outputs
-Contributed to visual layout choices and content formatting
-Assisted with README drafting and presentation-ready polishing

Joint Efforts-
-Brainstorming project direction and deciding on WOW features
-Debugging API issues together
-Pair-testing final user flows
-Reviewing and improving code clarity

Use of AI Tools-
AI assisted our process as a supportive tool, not a builder of the project.
We used AI for:
Suggesting potential WOW features and helping us select the strongest ones
Explaining API documentation and error messages
Helping structure the backend logic and understand proper routing patterns
Providing general guidance on how to deploy a Flask app on PythonAnywhere
Offering debugging suggestions when stuck
All code, decisions, integration, and testing were completed by us.

Deployment Notes (PythonAnywhere)-
The app is deployed through PythonAnywhere.
However, free-tier PythonAnywhere accounts block external API calls, which means:
The homepage loads
The form works
Templates render correctly
But APIs (Mapbox, MBTA, OpenWeather) will not return data due to outbound internet restrictions.Locally, the full app works as intended.