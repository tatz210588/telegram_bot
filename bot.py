import telebot
import nest_asyncio
import json
import requests

nest_asyncio.apply()

# Replace with your bot token
bot = telebot.TeleBot('7544849803:AAFdMsYsOPV3nh6eClso84A92dWhXGVODHQ')

# Admin password
admin_password = "admin12345"


# Load JSON data from a file
def load_json_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data

# Fetch follow-up text from JSON data
def fetch_follow_up_text():
    data = load_json_data()
    return data.get('follow_up_message', 'No follow-up message found.')

# Welcome message
@bot.message_handler(commands=['start'])
def welcome_message(message):
    welcome_text = '👋 Welcome to BlokZen! 🎥\nWe\'re revolutionizing real estate investment by allowing you to co-own premium properties through fractional ownership.'
    
    # Load the video file from a local path or URL
    video_path = 'C://Users/Shreyashi Mukherjee/Downloads/videoplayback.mp4'  # Replace with your actual video file path
    
    # Send the welcome message and video
    bot.send_message(message.chat.id, welcome_text)
    
    # with open(video_path, 'rb') as video_file:
    #     bot.send_video(message.chat.id, video_file)
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('START', callback_data='start_journey'))
    bot.send_message(message.chat.id, 'Ready to start your journey?', reply_markup=markup)

# Main menu
@bot.callback_query_handler(func=lambda call: call.data == 'start_journey')
def main_menu(call):
    main_menu_text = 'What would you like to do today?\n- Explore available properties 🏘️\n- Learn about fractional ownership 📖\n- Get market insights 📊\n- Use our investment calculator 🧮\n- Join the BlokZen community 🌍\n- Contact support for questions ❓'
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Explore Properties 🏘️', callback_data='explore_properties'))
    markup.add(telebot.types.InlineKeyboardButton('Learn About Fractional Ownership 📖', callback_data='learn_fo'))
    markup.add(telebot.types.InlineKeyboardButton('Get Market Insights 📊', callback_data='get_market_insights'))
    markup.add(telebot.types.InlineKeyboardButton('Use Investment Calculator 🧮', callback_data='use_calculator'))
    markup.add(telebot.types.InlineKeyboardButton('Join BlokZen Community 🌍', callback_data='join_community'))
    markup.add(telebot.types.InlineKeyboardButton('Contact Support ❓', callback_data='contact_support'))
    markup.add(telebot.types.InlineKeyboardButton('Get Follow-Up Message 👋', callback_data='fetch_follow_up'))

    bot.send_message(call.message.chat.id, main_menu_text, reply_markup=markup)


# Explore properties
@bot.callback_query_handler(func=lambda call: call.data == 'explore_properties')
def explore_properties(call):
    # with open('property.json', 'r', encoding='utf-8') as f:
    #     properties = json.load(f)
    url = 'https://server.blokzen.com/readfromdb'

        # Make a GET request to the API endpoint using requests.get()
    response = requests.get(url)
    properties= response.json()
    markup = telebot.types.InlineKeyboardMarkup()

    for property in properties:
        property_name = property['name']
        property_button = telebot.types.InlineKeyboardButton(property_name, callback_data=f'property_{property_name}')
        markup.add(property_button)

    bot.send_message(call.message.chat.id, 'Explore Properties:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('property_'))
def property_details(call):
    property_name = call.data.split('_')[1]
    url = 'https://server.blokzen.com/readfromdb'

        # Make a GET request to the API endpoint using requests.get()
    response = requests.get(url)
    properties= response.json()

    for property in properties:
        if property['name'] == property_name:
            property_description = f"**{property_name}**\n" \
                                   f"Investment: Starting at ₹{property['price']} lakhs\n" \
                                   f"Estimated ROI: {property['irr']}% annually\n" \
                                   f"Property Appreciation: {property['yield']}% per year\n" \
                                   f"\n📍 **Property Description**: {property['description']}"

            more_details_button = telebot.types.InlineKeyboardButton('More Details 🔍', callback_data=f'more_details_{property_name}')
            invest_now_button = telebot.types.InlineKeyboardButton('Invest Now 💰', url='https://blokzen.com/opportunity')
            explore_property = telebot.types.InlineKeyboardButton('Explore Properties 🏘️', callback_data='explore_properties')
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(more_details_button)
            markup.add(invest_now_button)
            markup.add(explore_property)

            bot.send_message(call.message.chat.id, property_description, reply_markup=markup)
            break


@bot.callback_query_handler(func=lambda call: call.data.startswith('more_details_'))
def more_details(call):
    property_name = call.data.split('_')[2]
    url = 'https://server.blokzen.com/readfromdb'

        # Make a GET request to the API endpoint using requests.get()
    response = requests.get(url)
    properties= response.json()

    for property in properties:
        if property['name'] == property_name:
            more_details_text = f"More Details about {property_name}\n" \
                                f"Location: {property['location']}\n" \
                                f"Possession: {property['possession']}\n" \
                                f"Amenities: {property['amenities']}\n" 
            bot.send_message(call.message.chat.id, more_details_text)
            break

# Learn about fractional ownership
@bot.callback_query_handler(func=lambda call: call.data == 'learn_fo')
def learn_fo(call):
    fo_text = '🤔 What is fractional ownership?\n It\'s a way for multiple investors to co-own a portion of a property and share the rental income and appreciation.\nYou can start with as little as ₹5 lakh and gain exposure to premium real estate without the full cost. 📈'

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Read FAQs 📖', callback_data='read_faqs'))
    markup.add(telebot.types.InlineKeyboardButton('See how it works 🔍', url='https://assets.blokzen.com/campaigns'))

    bot.send_message(call.message.chat.id, fo_text, reply_markup=markup)

# Load FAQ data from JSON file
def load_faqs():
     # Define the API endpoint URL
    url = 'https://server.blokzen.com/faqmain'

        # Make a GET request to the API endpoint using requests.get()
    response = requests.get(url)
    posts = response.json()
    return posts

# Read FAQs
@bot.callback_query_handler(func=lambda call: call.data == 'read_faqs')
def read_faqs(call):
    faqs = load_faqs()
    
    markup = telebot.types.InlineKeyboardMarkup()
    
    for faq in faqs:
        markup.add(telebot.types.InlineKeyboardButton(faq['question'], callback_data=f'faq_{faq["id"]}'))

    bot.send_message(call.message.chat.id, 'Select a question:', reply_markup=markup)

# Handle FAQ answers
@bot.callback_query_handler(func=lambda call: call.data.startswith('faq_'))
def answer_faq(call):
    faq_id = call.data.split('_')[1]
    
    faqs = load_faqs()
    
    for faq in faqs:
        if faq['id'] == faq_id:
            bot.send_message(call.message.chat.id, faq['answer'])
            break


@bot.callback_query_handler(func=lambda call: call.data == 'get_posts1')
def get_posts1(call):
    bot.send_message(call.message.chat.id, 'Shreyashi')

# Get market insights
@bot.callback_query_handler(func=lambda call: call.data == 'get_market_insights')
def get_market_insights(call):
    market_insights_text = '📊 *Mukteshwar, Nainital, Uttarakhand, India Real Estate Market Update*:\n- Residential properties appreciated by 10% last year.\n- Rental yields are around 8%.\n- Upcoming infrastructure projects: [Short description].'

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Explore Properties 🏘️', callback_data='get_posts1'))
    markup.add(telebot.types.InlineKeyboardButton('Get More Insights 📊', callback_data='use_calculator'))

    bot.send_message(call.message.chat.id, market_insights_text, reply_markup=markup)

# Use investment calculator
@bot.callback_query_handler(func=lambda call: call.data == 'use_calculator')
def use_calculator(call):
    calculator_text = '💰 How much would you like to invest? (Enter an amount):'
    
    bot.send_message(call.message.chat.id, calculator_text)

@bot.message_handler(func=lambda message: message.text.isdigit())
def calculate_investment(message):
   investment_amount = int(message.text)
   annual_rental_income = investment_amount * 0.08
   property_value_appreciation = investment_amount * 0.05
   
   bot_response = f'With an investment of ₹{investment_amount}, you can expect:\n- Annual Rental Income: ₹{annual_rental_income}\n- Property Value Appreciation: ₹{property_value_appreciation} (based on average growth of 5% annually)'

   markup = telebot.types.InlineKeyboardMarkup()
   markup.add(telebot.types.InlineKeyboardButton('Explore Properties 🏡', callback_data='explore_properties'))
   markup.add(telebot.types.InlineKeyboardButton('Learn More 📖', url='https://assets.blokzen.com/campaigns'))

   bot.send_message(message.chat.id, bot_response, reply_markup=markup)

# Join BlokZen community
@bot.callback_query_handler(func=lambda call: call.data == 'join_community')
def join_community(call):
   community_text = '🌍 Join our community to stay updated on market trends, new property listings, and exclusive offers!'

   markup = telebot.types.InlineKeyboardMarkup()
   markup.add(telebot.types.InlineKeyboardButton('Join WhatsApp Group 📲', url='https://t.ly/hyY-1'))
   markup.add(telebot.types.InlineKeyboardButton('Follow us on Our Page 🐦', url='https://blokzen.com/'))

   bot.send_message(call.message.chat.id, community_text, reply_markup=markup)

# Contact support
@bot.callback_query_handler(func=lambda call: call.data == 'contact_support')
def contact_support(call):
   support_text = 'Need help or have questions? Our support team is here to assist you.❓'

   markup = telebot.types.InlineKeyboardMarkup()
   markup.add(telebot.types.InlineKeyboardButton('Browse FAQs 📖', callback_data='read_faqs'))
   markup.add(telebot.types.InlineKeyboardButton('Contact Support 📞', callback_data='contact_support'))

   # Add additional support options here if needed

   bot.send_message(call.message.chat.id, support_text, reply_markup=markup)

# Fetch follow-up message
@bot.callback_query_handler(func=lambda call: call.data == 'fetch_follow_up')
def send_follow_up_message(call):
   follow_up_text = fetch_follow_up_text()

   markup = telebot.types.InlineKeyboardMarkup()
   markup.add(telebot.types.InlineKeyboardButton('Explore Properties 🏡', callback_data='explore_properties'))

   # Add additional options if needed

   bot.send_message(call.message.chat.id, follow_up_text, reply_markup=markup)

# Admin command to access admin panel
@bot.message_handler(commands=['admin'])
def admin_command(message):
   admin_prompt_text = f'Please enter the admin password to access the admin panel.'
   
   bot.send_message(message.chat.id, admin_prompt_text)

@bot.message_handler(func=lambda message: message.text == admin_password)
def access_admin_panel(message):
   admin_panel_text = 'Admin Panel:\n- Update Property Listings\n- Update Educational Content\n- Update Videos\n- Send Mass Updates'

   markup = telebot.types.InlineKeyboardMarkup()
   markup.add(telebot.types.InlineKeyboardButton('Update Property Listings', callback_data='update_properties'))
   markup.add(telebot.types.InlineKeyboardButton('Update Educational Content', callback_data='update_educational_content'))
   markup.add(telebot.types.InlineKeyboardButton('Update Videos', callback_data='update_videos'))
   markup.add(telebot.types.InlineKeyboardButton('Send Mass Updates', callback_data='send_mass_updates'))

   bot.send_message(message.chat.id, admin_panel_text, reply_markup=markup)

# Handle property updates
@bot.callback_query_handler(func=lambda call: call.data == 'update_properties')
def update_properties(call):
   update_text = 'Please enter the new property details in JSON format (e.g., {"name": "Property 1", "location": "Bangalore", ...}).'
   
   bot.send_message(call.message.chat.id, update_text)

@bot.message_handler(func=lambda message: message.text.startswith("{") and message.from_user.id in [user.id for user in bot.get_chat_administrators(message.chat.id)])
def handle_property_update(message):
   try:
       new_properties = json.loads(message.text)
       with open('property.json', 'w') as f:
           json.dump(new_properties, f)
       bot.send_message(message.chat.id, "Property details updated successfully!")
   
   except json.JSONDecodeError:
       bot.send_message(message.chat.id, "Invalid JSON format. Please try again.")

# Handle educational content updates
@bot.callback_query_handler(func=lambda call: call.data == 'update_educational_content')
def update_educational_content(call):
   update_text = 'Please enter the new educational content in JSON format (e.g., {"question": "What is fractional ownership?", "answer": "..." }).'
   
   bot.send_message(call.message.chat.id, update_text)

@bot.message_handler(func=lambda message: message.text.startswith("{") and message.from_user.id in [user.id for user in bot.get_chat_administrators(message.chat.id)])
def handle_educational_update(message):
   try:
       new_faqs = json.loads(message.text)
       with open('faq.json', 'w') as f:
           json.dump(new_faqs, f)
       bot.send_message(message.chat.id, "Educational content updated successfully!")
   
   except json.JSONDecodeError:
       bot.send_message(message.chat.id, "Invalid JSON format. Please try again.")

# Handle video updates
@bot.callback_query_handler(func=lambda call: call.data == 'update_videos')
def update_videos(call):
   update_text = 'Please enter the new video link in JSON format (e.g., {"video": "https://example.com/video"}).'
   
   bot.send_message(call.message.chat.id, update_text)

@bot.message_handler(func=lambda message: message.text.startswith("{") and message.from_user.id in [user.id for user in bot.get_chat_administrators(message.chat.id)])
def handle_video_update(message):
   try:
       new_video = json.loads(message.text)
       with open('video.json', 'w') as f:
           json.dump(new_video, f)
       bot.send_message(message.chat.id, "Video link updated successfully!")
   
   except json.JSONDecodeError:
       bot.send_message(message.chat.id, "Invalid JSON format. Please try again.")

# Send mass updates
@bot.callback_query_handler(func=lambda call: call.data == 'send_mass_updates')
def send_mass_updates(call):
   mass_update_text = 'Please enter the mass update message in JSON format (e.g., {"message": "Hello everyone!", "video": "https://example.com/video"}).'
   
   bot.send_message(call.message.chat.id, mass_update_text)

@bot.message_handler(func=lambda message: message.text.startswith("{") and message.from_user.id in [user.id for user in bot.get_chat_administrators(message.chat.id)])
def handle_mass_update(message):
   try:
       mass_update_data = json.loads(message.text)
       mass_update_message = mass_update_data.get('message')
       mass_update_video = mass_update_data.get('video')

       if mass_update_message and mass_update_video:
           for user in bot.get_chat_members(message.chat.id):
               if user.status != 'left':
                   bot.send_message(user.user_id(), mass_update_message)  # Corrected user ID access method.
                   bot.send_video(user.user_id(), mass_update_video)  # Corrected user ID access method.
           bot.send_message(message.chat.id, "Mass update sent successfully!")
       
       else:
           bot.send_message(message.chat.id, "Invalid JSON format. Please try again.")
   
   except json.JSONDecodeError:
       bot.send_message(message.chat.id,"Invalid JSON format. Please try again.")

# Start polling for updates
if __name__ == "__main__":
     bot.polling(none_stop=True)
     
