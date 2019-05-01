#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String

import cv2
import logging
import rospy

REQUEST_KWARGS={
    'proxy_url': 'http://212.8.249.112:3128/'
}

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

image_topic = "/usb_cam/image_raw"
image_path = "/tmp/telegram_last_image.jpg"

class ImageReply(object):

    def __init__(self):
	rospy.loginfo("TOKEN Authentication...")
        token = rospy.get_param('/telegram/token', None)
        if token is None:
            rospy.loginfo("Authentication failed")
            exit(0)
        else:
            rospy.loginfo("Authentication is successful")

	self.str_pub = rospy.Publisher("~telegram_chat", String, queue_size=1)

        self.bridge = CvBridge()
        updater = Updater(token, request_kwargs = REQUEST_KWARGS)
        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.text, self.pub_received))
        dp.add_handler(CallbackQueryHandler(self.button))
        dp.add_error_handler(self.error)
        updater.start_polling()


    def get_image(self, image_topic=None):
        rospy.loginfo("Getting image...")
        if image_topic is None:
            image_topic = image_topic
        image_msg = rospy.wait_for_message(image_topic, Image)
        rospy.loginfo("Got image!")
        cv2_img = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
        img_file_path = image_path
        cv2.imwrite(img_file_path, cv2_img)
        rospy.loginfo("Saved to: " + img_file_path)
        return img_file_path

 
    def pub_received(self, bot, update):
        valid_necessary_words = ['picture']
        found_word = False
        for v in valid_necessary_words:
            if v in update.message.text.lower():
                self.do_image_stuff(update)
                found_word = True
                break
        if not found_word:
            update.message.reply_text("Try any of: " + str(valid_necessary_words))
	self.str_pub.publish(update.message.text)


    def do_image_stuff(self, update):
        # Get topics of type Image
        topics_and_types = rospy.get_published_topics()
        image_topics = []
        for top, typ in topics_and_types:
            if typ == 'sensor_msgs/Image':
                image_topics.append(top)

        keyboard = []
        for topicname in image_topics:
            keyboard.append([InlineKeyboardButton(
                topicname, callback_data=topicname)])

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Choose image topic:', reply_markup=reply_markup)


    def button(self, bot, update):

        query = update.callback_query
        bot.editMessageText(text="Capturing image of topic: %s" % query.data,
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id)

        img_file_path = self.get_image(image_topic=query.data)
        bot.editMessageText(text="Uploading captured image of topic: %s" % query.data,
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id)

        bot.send_photo(chat_id=query.message.chat_id,
                       photo=open(img_file_path, 'rb'),
                       caption="This is what I see on topic " +
                       query.data)


    def error(self, bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))


if __name__ == '__main__':
    rospy.init_node('telegram_chat_pub')
    cp = ImageReply()
    rospy.spin()
