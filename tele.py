import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder
from datetime import datetime, timedelta
from pytz import timezone
from typing import Final
from telegram import Update
import asyncio

application = ApplicationBuilder().token('7207134585:AAHlQbdvhCgtrwq3ip9-myFSu8Jqx8Szghc').build()

# Set your bot token
TOKEN: Final = '7207134585:AAHlQbdvhCgtrwq3ip9-myFSu8Jqx8Szghc'
BOT_USERNAME: Final = '@CutieBubbleBot'

# Default timezone to Vietnam
DEFAULT_TIMEZONE = timezone('Asia/Ho_Chi_Minh')

# Dictionary to store reminders
reminders = {}

# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi cutie! How can I help you?')

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Commands:\n/setreminder - Set a new reminder\n/viewreminders - View all reminders')

# Custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command')

# Set reminder
async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the date for the reminder (YYYY-MM-DD):')
    context.user_data['step'] = 'date'

# Process reminder steps
async def process_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get('step')
    user_id = update.message.chat.id
    text = update.message.text

    if step == 'date':
        try:
            context.user_data['date'] = datetime.strptime(text, '%Y-%m-%d').date()
            await update.message.reply_text('Now enter the time for the reminder (HH:MM, 24-hour format):')
            context.user_data['step'] = 'time'
        except ValueError:
            await update.message.reply_text('Invalid date format. Please enter the date in YYYY-MM-DD format.')

    elif step == 'time':
        try:
            time_obj = datetime.strptime(text, '%H:%M').time()
            reminder_datetime = datetime.combine(context.user_data['date'], time_obj)
            context.user_data['datetime'] = DEFAULT_TIMEZONE.localize(reminder_datetime)
            await update.message.reply_text('Enter the custom message for this reminder:')
            context.user_data['step'] = 'message'
        except ValueError:
            await update.message.reply_text('Invalid time format. Please enter the time in HH:MM format.')

    elif step == 'message':
        message = text
        reminder_id = len(reminders) + 1
        reminders[reminder_id] = {
            'user_id': user_id,
            'datetime': context.user_data['datetime'],
            'message': message
        }
        
        # Calculate the seconds until the reminder is due
        when = (context.user_data['datetime'] - datetime.now(DEFAULT_TIMEZONE)).total_seconds()
        if when > 0:
            await update.message.reply_text(f"Reminder set for {context.user_data['datetime']} with message: '{message}'.")
            context.user_data.clear()
            context.job_queue.run_once(reminder_alert, when=when, data={'user_id': user_id, 'message': message})
        else:
            await update.message.reply_text("The reminder time must be in the future. Please set again.")
            context.user_data.clear()  # Clear any saved steps if the time is invalid

# View all reminders
async def view_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if reminders:
        reminder_texts = [f"ID: {reminder_id} | Date: {rem['datetime']} | Message: {rem['message']}" for reminder_id, rem in reminders.items()]
        await update.message.reply_text("\n".join(reminder_texts))
    else:
        await update.message.reply_text("You have no active reminders.")

# Trigger the reminder alert
async def reminder_alert(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    user_id = job_data['user_id']
    message = job_data['message']
    await context.bot.send_message(chat_id=user_id, text=f"Reminder: {message}")

# Main function
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('setreminder', set_reminder))
    app.add_handler(CommandHandler('viewreminders', view_reminders))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_reminder))
    app.add_handler(CommandHandler('custom', custom_command))

    # Poll the bot
    print('Polling...')
    app.run_polling(poll_interval=3)