# formi
Backend API for Retrieval of Locations within 50Km radius Using FastAPI

# Queries
  ''' 
    1. What was your initial thought process when you first read the problem statement, and how did you break it down into smaller, manageable parts?
    
    When I first encountered the problem, I immediately recognized that the core functionality required was geospatial—specifically, taking a user-provided location (which may not always be clean or accurate) and returning nearby predefined points of interest within a certain distance. However, the real challenge wasn’t just in calculating distances—it was in handling human error in the input: typos, alternative spellings, or even vague place names. 
    
    To tackle the problem systematically, I decomposed it into several clear, interdependent components:
    
    First i extracted location and its coordinate from PDF using an LLM in structured representation of Json and stored as a variable in file, for smooth distance calculation between query location coordinates.
    
    Handling ambiguous or incorrect user input
    Since users often submit locations with typos or varying formats (e.g., "rishiksh" instead of "Rishikesh"), I needed a robust normalization system. I combined two approaches:
    
    LLM-based correction using Gemini Pro, which could semantically understand and correct inputs by comparing them with known destinations, giving list of locations Moustache have makes LLMs more robust to Spelling mistake.
    
    Determining geographic coordinates for the query
    If the user input wasn’t found in the predefined list—even after normalization—I used the GeoPy library to geocode the location name into latitude and longitude. 
    
    Calculating physical distances between locations
    I implemented the Haversine formula to compute great-circle distances between two latitude-longitude pairs. 
    
    Error handling and suggestions
    I paid particular attention to user experience in failure modes. If no coordinates could be found, the API returns helpful error messages along with suggested nearby locations This way, the system always guides users toward a valid result rather than failing silently.
    
    Each of these parts was developed and tested independently before integrating them into the complete pipeline. The modular design made the codebase clean, maintainable, and easy to extend—for example, adding new locations or switching out the LLM provider in the future would require minimal changes.
  '''

  '''
    2. What specific tools, libraries, or online resources did you use to develop your solution, and why did you choose them over other options?
    
    FastAPI for building the web API due to its speed, modern Python support, easier to build upon.
    
    Google's Gemini API for misspelled queries and Extraction of Location data from PDF, as API is free to Use and fast for API Purpose.
    
    GeoPy for geolocation coordinates extraction as it is free to use without any Billing procedure.
  '''

  '''
    3. Describe a key challenge you faced while solving this problem and how you arrived at the final solution?
    
    A major challenge was handling user inputs that were either misspelled, ambiguous, or completely unknown. Initially, I relied solely on fuzzy matching with difflib, but it didn't always provide relevant corrections. To address this, I incorporated the Gemini API as a smarter correction. I then layered fallbacks in order: Gemini → fuzzy match → GeoPy → suggestions. This tiered strategy ensured robustness and improved the accuracy of results, especially for unusual or slightly wrong queries.
  '''

  '''
    4. If you had more time, what improvements or alternative approaches would you explore, and why do you think they might be valuable?
    
    If I had more time, I would:
    
    Integrate a RAG based module to extract Property from Moustache properties, as Property Pdf data can Scale or change frequently, RAG based framework would be robust to changes and we dont need to extract Location coordinates every time pdf changes.
    
    Develop a frontend UI Smooth experience.
  '''


# Output
Output of the API when queried on "Udaipur"
![Output of the API when queried on "Udaipur"](Correct%20Udaipur.png)

Output of the API when queried on Wrong Spelling of "Udaipur", It shows that our Program is Robust to Spelling errors
![Output of the API when queried on Wrong Spelling of "Udaipur", It shows that our Program is Robust to Spelling errors](Incorrect%20Udaipur.png)

To run API read this "github-readme.md" file
[API Execution workflow](github-readme.md)
