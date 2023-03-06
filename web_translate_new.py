import os
from bs4 import BeautifulSoup
from google.cloud import translate_v2 as translate

# Define the source and target languages
source_lang = 'en'
target_lang = 'hi'

# Define the directory path to translate
dir_path = 'www.classcentral.com'

# Create a translation client
credentials_path = 'credentials.json'  # Replace with the path to your Google Cloud credentials file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
translate_client = translate.Client()

# Recursively walk through the directory and its subdirectories
for root, dirs, files in os.walk(dir_path):
    for file in files:
        # Check if the file is an HTML file
        if file.endswith('.html'):
            # Read the contents of the file
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                contents = f.read()

            # Parse the HTML contents using BeautifulSoup
            soup = BeautifulSoup(contents, 'html.parser')

            # Find all text elements in the HTML content and translate them
            for element in soup.find_all(string=True):
                if element.parent.name in ['script', 'style']:
                    # Skip script and style elements
                    continue

                # Translate the text element using the translation client
                translated = translate_client.translate(element.strip(), source_language=source_lang, target_language=target_lang)

                # Replace the original text with the translated text
                element.replace_with(translated['translatedText'])

            # Write the translated contents back to the file
            with open(os.path.join(root, file), 'w', encoding='utf-8') as f:
                f.write(str(soup))
