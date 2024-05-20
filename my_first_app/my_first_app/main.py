from dara.core import ConfigurationBuilder
from my_first_app.pages.eda import eda_page
from my_first_app.pages.classification import classification_page

# Create a configuration builder
config = ConfigurationBuilder()

# Register pages
config.add_page('EDA', eda_page())
config.add_page('Classification', classification_page())