 ## Drug Interaction Tracker

## Overview

Drug Interaction Tracker is a web application designed to help healthcare professionals and patients identify potential interactions between different drugs. It provides a platform to input two drugs and determine if there are any known interactions based on predefined rules and data analysis.

## Features

- Drug Interaction Detection: Users can input two drugs and the system will analyze their properties to identify potential interactions.
  
- Rule-Based System: The application uses a rule-based system to define conditions under which drug interactions occur. These rules are predefined and based on factors such as drug classes, side effects, medical conditions, and pharmacological mechanisms.

- Database Integration: Drug information and interaction rules are stored in MSSQL database, allowing for efficient retrieval and analysis.

- API Integration: The application provides an API endpoint to programmatically check for drug interactions, enabling integration with other systems and applications.

## Installation

1. Clone the repository:

   git clone https://github.com/aradhisuresh/DrugInteractionTracker.git
   

2. Navigate to the project directory:

   cd DrugInteractionTracker
   

3. Install dependencies


4. Run migrations:

   python manage.py migrate
   
5. Start the development server:

   python manage.py runserver

6. Access the application at [http://localhost:8000](http://localhost:8000) in your web browser.


# API Endpoint

- GET /api/get_drug_interactions/
  - Parameters: `drug_a`, `drug_b`
  - Returns: JSON response containing potential drug interactions between the two drugs.

# Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a new Pull Request.
